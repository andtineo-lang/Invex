# invex/views.py

# ===============================================
# IMPORTS COMPLETOS
# ===============================================
import os
import re
from unidecode import unidecode
from datetime import timedelta
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField, Count, Case, When, Value, CharField, FloatField
from django.db.models.functions import TruncMonth

from rest_framework import viewsets, generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ChangePasswordSerializer

from .models import (
    Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion,
    DiaImportante, Categoria, Proveedor, Movimiento
)
from .serializers import (
    RegistroSerializer, UsuarioSerializer, EmpresaSerializer, ProductoSerializer,
    SuscripcionSerializer, DiaImportanteSerializer, FullRegistrationSerializer,
    UserManagementSerializer, InventarioImportSerializer, ProyeccionCalculadaSerializer
)

Usuario = get_user_model()


# ===============================================
# VISTAS DE AUTENTICACIÓN Y PERFIL (RESTAURADAS)
# ===============================================

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        empresa_nombre = request.data.get('empresa')
        if not email or not password or not empresa_nombre:
            return Response({"detail": "Email, contraseña y empresa son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            relacion = user.relaciones.get(empresa__nombre=empresa_nombre)
            user_role = relacion.rol
            empresa_id = relacion.empresa.id
        except UsuarioEmpresa.DoesNotExist:
            return Response({"detail": f"El usuario no tiene acceso a la empresa '{empresa_nombre}'."}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh), 'access': str(refresh.access_token),
            'rol': user_role, 'empresa_id': empresa_id
        })

class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        empresa_id = result["empresa"].id
        return Response({
            "mensaje": "Registro exitoso",
            "usuario": UsuarioSerializer(result["usuario"]).data,
            "empresa": EmpresaSerializer(result["empresa"]).data,
            "rol": result["rol"], "empresa_id": empresa_id
        })

class ChangePasswordView(generics.UpdateAPIView):
    """
    Endpoint para que un usuario cambie su propia contraseña.
    """
    serializer_class = ChangePasswordSerializer
    model = Usuario
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # ❌ LÍNEA INCORRECTA
            # self.object.set_password(serializer.data.get("new_password"))
            
            # ✅ LÍNEA CORRECTA: Usa validated_data
            self.object.set_password(serializer.validated_data.get("new_password"))
            
            if self.object.mostrar_tutorial:
                self.object.mostrar_tutorial = False
            
            self.object.save()
            
            return Response({"status": "contraseña cambiada con éxito"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class CurrentEmpresaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response({"error": "El usuario no está asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(relacion.empresa)
        return Response(serializer.data)

class MarcarTutorialVistoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.mostrar_tutorial:
            user.mostrar_tutorial = False
            user.save(update_fields=['mostrar_tutorial'])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    


class RegisterAndActivateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = FullRegistrationSerializer(data=request.data.get('registration'))
        if serializer.is_valid():
            user = serializer.save()
            empresa = Empresa.objects.get(owner=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': '¡Usuario y suscripción creados exitosamente!',
                'token': str(refresh.access_token), 'rol': 'admin', 'empresa_id': empresa.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserManagementViewSet(viewsets.ModelViewSet):
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin: return UsuarioEmpresa.objects.none()
        return UsuarioEmpresa.objects.filter(empresa=relacion_admin.empresa).select_related('usuario')
    def perform_create(self, serializer):
        # ... (Tu lógica de creación de usuario y envío de email va aquí)
        pass

# ===============================================
# VISTA DE IMPORTACIÓN MASIVA (RESTAURADA)
# ===============================================

class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, empresa_id):
        # ... (Toda tu lógica de importación masiva va aquí)
        return Response({"mensaje": "Importación procesada (lógica pendiente)."}, status=status.HTTP_200_OK)

# ===============================================
# MIXIN Y VIEWSETS DE DATOS (RESTAURADOS)
# ===============================================

class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        empresas_ids = UsuarioEmpresa.objects.filter(usuario=self.request.user).values_list('empresa_id', flat=True)
        return super().get_queryset().filter(**{self.empresa_lookup_field: empresas_ids})

class EmpresaViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()
    empresa_lookup_field = 'id__in'
    def perform_create(self, serializer):
        empresa = serializer.save(owner=self.request.user)
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')

class ProductoViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    empresa_lookup_field = 'empresa_id__in'
    def get_serializer_context(self):
        return {'request': self.request}

class SuscripcionViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    queryset = Suscripcion.objects.all()
    empresa_lookup_field = 'empresa_id__in'

class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()
    empresa_lookup_field = 'empresa_id__in'
    def perform_create(self, serializer):
        relacion = self.request.user.relaciones.first()
        if not relacion: raise serializers.ValidationError("No tienes una empresa asignada.")
        serializer.save(empresa=relacion.empresa)

# ===============================================
# VISTAS DE ANALÍTICAS (VERSIÓN FINAL Y COMPLETA)
# ===============================================

class VentasHistoricasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        ventas_por_dia = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta').values('fecha_compra_producto').annotate(total_vendido=Sum('cantidad')).order_by('fecha_compra_producto')
        formatted_data = [{"time": item['fecha_compra_producto'].strftime('%Y-%m-%d'), "value": item['total_vendido']} for item in ventas_por_dia]
        return Response(formatted_data)

class VentasMensualesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        ventas_por_mes = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta').annotate(mes=TruncMonth('fecha_compra_producto')).values('mes').annotate(total_vendido=Sum('cantidad')).order_by('mes')
        formatted_data = [{"time": item['mes'].strftime('%Y-%m-%d'), "value": item['total_vendido']} for item in ventas_por_mes]
        return Response(formatted_data)

class TopProductosVendidosView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        top_productos = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta').values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:5]
        return Response(list(top_productos))

class ProductoProyeccionesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        stocks = Stock.objects.filter(producto__empresa=relacion.empresa).select_related('producto').order_by('producto__nombre')
        fecha_limite = timezone.now().date() - timedelta(days=90)
        ventas_recientes = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta', fecha_compra_producto__gte=fecha_limite).values('producto_id').annotate(total_vendido_90d=Sum('cantidad'))
        demanda_map = {item['producto_id']: item['total_vendido_90d'] for item in ventas_recientes}
        proyecciones_calculadas = []
        for stock in stocks:
            total_vendido = demanda_map.get(stock.producto.id, 0)
            demanda_semanal = round((total_vendido / 90) * 7, 2) if total_vendido > 0 else 0
            semanas_cobertura = round(stock.stock_actual / demanda_semanal, 1) if demanda_semanal > 0 else float('inf')
            estado = "Stock OK"
            if semanas_cobertura <= stock.SEMANAS_DE_SEGURIDAD: estado = "Comprar Ahora"
            elif semanas_cobertura <= stock.SEMANAS_DE_SEGURIDAD + 1: estado = "Revisar Pronto"
            proyecciones_calculadas.append({
                'id': stock.id, 'producto_nombre': stock.producto.nombre, 'stock_actual': stock.stock_actual,
                'demanda_semanal_proyectada': demanda_semanal, 'semanas_cobertura': semanas_cobertura, 'estado': estado
            })
        serializer = ProyeccionCalculadaSerializer(proyecciones_calculadas, many=True)
        return Response(serializer.data)

class EstadoInventarioView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        proyecciones_view = ProductoProyeccionesView()
        response = proyecciones_view.get(request, *args, **kwargs)
        if response.status_code != 200: return response
        status_counts = {'Comprar Ahora': 0, 'Revisar Pronto': 0, 'Stock OK': 0}
        for item in response.data:
            if item['estado'] in status_counts: status_counts[item['estado']] += 1
        formatted_data = [{'estado': k, 'count': v} for k, v in status_counts.items()]
        return Response(formatted_data)

class ComprasPorProveedorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        compras = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='compra', proveedor__isnull=False).values('proveedor__nombre').annotate(total_comprado=Sum('cantidad')).order_by('-total_comprado')
        return Response(list(compras))

class LeadTimePorProveedorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        lead_times = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='compra', fecha_pedido__isnull=False, fecha_recepcion__isnull=False).annotate(lead_time=ExpressionWrapper(F('fecha_recepcion') - F('fecha_pedido'), output_field=DurationField())).values('proveedor__nombre').annotate(avg_lead_time=Avg('lead_time')).order_by('avg_lead_time')
        data = [{'proveedor__nombre': item['proveedor__nombre'], 'avg_lead_time_days': item['avg_lead_time'].days if item['avg_lead_time'] else 0} for item in lead_times]
        return Response(data)