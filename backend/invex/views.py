import os
import re
from unidecode import unidecode
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
# 👇 --- IMPORTS PARA RESETEO ---
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
# ---------------------------
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import HasRole
from .models import (
    Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion,
    DiaImportante, Categoria, Proveedor, Movimiento
)
from .serializers import (
    UsuarioSerializer, EmpresaSerializer, ProductoSerializer,
    SuscripcionSerializer, DiaImportanteSerializer, FullRegistrationSerializer,
    UserManagementSerializer, ProyeccionCalculadaSerializer, ChangePasswordSerializer,
    InventarioImportSerializer  # Asegúrate de que este serializer exista y esté correcto
)

Usuario = get_user_model()

# ===============================================
# VISTAS DE AUTENTICACIÓN Y PERFIL
# ===============================================

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        empresa_nombre = request.data.get('empresa')
        if not all([email, password, empresa_nombre]):
            return Response({"detail": "Email, contraseña y empresa son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Usuario.objects.get(email=email)
            if not user.check_password(password):
                raise Usuario.DoesNotExist
            relacion = user.relaciones.get(empresa__nombre=empresa_nombre)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'rol': relacion.rol, 'empresa_id': relacion.empresa.id})
        except Usuario.DoesNotExist:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        except UsuarioEmpresa.DoesNotExist:
            return Response({"detail": f"Acceso denegado a la empresa '{empresa_nombre}'."}, status=status.HTTP_403_FORBIDDEN)

class RegisterAndActivateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = FullRegistrationSerializer(data=request.data.get('registration'))
        if serializer.is_valid():
            user = serializer.save()
            empresa = user.relaciones.first().empresa
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': '¡Usuario y suscripción creados exitosamente!',
                'token': str(refresh.access_token),
                'rol': 'admin',
                'empresa_id': empresa.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- VISTA PARA SOLICITUD DE RESETEO ---
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Busca al usuario
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # 2. Si no existe, no lo reveles (seguridad)
            return Response(
                {'message': 'Si una cuenta con este email existe, se ha enviado un enlace de recuperación.'}, 
                status=status.HTTP_200_OK
            )

        # 3. Genera token y UID
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # 4. Construye el enlace (usa FRONTEND_URL de settings.py)
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:8080')
        reset_link = f'{frontend_url}/reset-password?uidb64={uidb64}&token={token}'

        # 5. Envía el email
        try:
            send_mail(
                subject='Restablece tu contraseña de INVEX',
                message=(
                    f'Hola {user.nombre},\n\n'
                    'Recibimos una solicitud para restablecer tu contraseña para tu cuenta de INVEX.\n'
                    'Por favor, haz clic en el siguiente enlace para establecer una nueva contraseña:\n\n'
                    f'{reset_link}\n\n'
                    'Si no solicitaste esto, puedes ignorar este correo de forma segura.\n'
                    f'Este enlace expirará (revisa tu config de settings.py).\n\n'
                    'El equipo de INVEX.'
                ),
                from_email=os.environ.get('EMAIL_HOST_USER'),
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error al enviar email de reseteo a {email}: {e}")
        
        # 6. Envía respuesta genérica de éxito
        return Response(
            {'message': 'Si una cuenta con este email existe, se ha enviado un enlace de recuperación.'}, 
            status=status.HTTP_200_OK
        )

# --- VISTA PARA CONFIRMAR EL RESETEO ---
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Obtener los datos del frontend
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        # 2. Validar que todos los datos estén
        if not all([uidb64, token, new_password]):
            return Response(
                {'error': 'Se requieren todos los campos (uid, token, contraseña).'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Decodificar el UID y obtener el usuario
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            user = None

        # 4. Validar el usuario y el token (si el token expiró, esto dará False)
        if user is not None and default_token_generator.check_token(user, token):
            
            # 5. El token es válido, establecer la nueva contraseña
            user.set_password(new_password)
            
            if hasattr(user, 'mostrar_tutorial') and user.mostrar_tutorial:
                user.mostrar_tutorial = False
                
            user.save()
            
            # 6. Enviar respuesta de éxito
            return Response({'message': '¡Contraseña actualizada con éxito!'}, status=status.HTTP_200_OK)
        else:
            # 7. El token es inválido o el usuario no existe
            return Response(
                {'error': 'El enlace de reseteo no es válido o ha expirado. Por favor, solicita uno nuevo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
# -----------------------------------------------------

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Usuario
    permission_classes = [IsAuthenticated]
    def get_object(self, queryset=None):
        return self.request.user
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.object.set_password(serializer.validated_data.get("new_password"))
            if hasattr(self.object, 'mostrar_tutorial') and self.object.mostrar_tutorial:
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
            return Response({"error": "Usuario no asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(relacion.empresa)
        return Response(serializer.data)

class MarcarTutorialVistoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if hasattr(user, 'mostrar_tutorial') and user.mostrar_tutorial:
            user.mostrar_tutorial = False
            user.save(update_fields=['mostrar_tutorial'])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

# ===============================================
# SECCIÓN DE GESTIÓN DE USUARIOS
# ===============================================

class UserManagementViewSet(viewsets.ModelViewSet):
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['admin']

    def get_queryset(self):
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin:
            return UsuarioEmpresa.objects.none()
        return UsuarioEmpresa.objects.filter(empresa=relacion_admin.empresa).select_related('usuario')

    def perform_create(self, serializer):
        nombre_completo = serializer.validated_data.get('nombre_completo')
        rol = serializer.validated_data.get('rol')
        email = self.request.data.get('email')

        if not email:
            raise serializers.ValidationError({"error": "El campo email es obligatorio."})

        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={'nombre': nombre_completo}
        )
        
        relacion_admin = self.request.user.relaciones.first()
        empresa_actual = relacion_admin.empresa

        if created:
            password_temporal = get_random_string(12)
            usuario.set_password(password_temporal)
            usuario.save()

            try:
                send_mail(
                    subject=f'¡Bienvenido a {empresa_actual.nombre}!',
                    message=(
                        f'Hola {nombre_completo},\n\n'
                        f'Has sido invitado a unirte a la empresa "{empresa_actual.nombre}".\n\n'
                        f'Puedes iniciar sesión con:\n'
                        f'Email: {email}\n'
                        f'Contraseña Temporal: {password_temporal}'
                    ),
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar el correo de bienvenida a {email}: {e}")
        
        serializer.save(usuario=usuario, empresa=empresa_actual, rol=rol)

# ===============================================
# VISTA DE IMPORTACIÓN MASIVA
# ===============================================

class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, empresa_id):
        user = request.user
        
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
            if not UsuarioEmpresa.objects.filter(usuario=user, empresa=empresa).exists():
                return Response({"error": "No tienes permiso para acceder a esta empresa."}, status=status.HTTP_403_FORBIDDEN)
        except Empresa.DoesNotExist:
            return Response({"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if not isinstance(data, list) or not data:
            return Response({"error": "Los datos deben ser una lista de productos."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = InventarioImportSerializer(data=data, many=True)
        if not serializer.is_valid():
            return Response({"error": "Errores de validación en los datos.", "detalles": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        movimientos_a_crear = []
        
        try:
            with transaction.atomic():
                for item in serializer.validated_data:
                    nombre_producto = item.pop('nombre').strip()
                    stock_actual = item.pop('stock_actual', 0)
                    nombre_categoria = item.pop('categoria')
                    unidad_medida = item.pop('unidad_medida')
                    cantidad_comprada = item.pop('cantidad_comprada', None)
                    cantidad_vendida = item.pop('cantidad_vendida', None)
                    nombre_proveedor = item.pop('proveedor')
                    fecha_compra_producto = item.pop('fecha_compra_producto', timezone.now().date())
                    
                    categoria_obj, _ = Categoria.objects.get_or_create(
                        empresa=empresa, nombre__iexact=nombre_categoria.strip(),
                        defaults={'nombre': nombre_categoria.strip()}
                    )

                    producto, _ = Producto.objects.update_or_create(
                        empresa=empresa, nombre__iexact=nombre_producto,
                        defaults={'nombre': nombre_producto, 'unidad_medida': unidad_medida or 'unidades', 'categoria': categoria_obj}
                    )

                    Stock.objects.update_or_create(
                        producto=producto, defaults={'stock_actual': int(stock_actual or 0)}
                    )
                    
                    proveedor_obj = None
                    if nombre_proveedor:
                        proveedor_obj, _ = Proveedor.objects.get_or_create(
                            empresa=empresa, nombre__iexact=nombre_proveedor.strip(),
                            defaults={'nombre': nombre_proveedor.strip()}
                        )
                        
                    if cantidad_comprada is not None and int(cantidad_comprada) > 0:
                        movimientos_a_crear.append(Movimiento(
                            producto=producto, tipo='compra', cantidad=int(cantidad_comprada),
                            unidad_medida=unidad_medida, fecha_compra_producto=fecha_compra_producto, proveedor=proveedor_obj
                        ))
                    
                    if cantidad_vendida is not None and int(cantidad_vendida) > 0:
                        movimientos_a_crear.append(Movimiento(
                            producto=producto, tipo='venta', cantidad=int(cantidad_vendida),
                            unidad_medida=unidad_medida, fecha_compra_producto=fecha_compra_producto
                        ))
                
                Movimiento.objects.bulk_create(movimientos_a_crear)
                
        except Exception as e:
            return Response({"error": f"Error de base de datos durante el procesamiento.", "detalles": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "mensaje": f"Se procesaron {len(serializer.validated_data)} filas. Productos actualizados y {len(movimientos_a_crear)} movimientos creados exitosamente."
        }, status=status.HTTP_201_CREATED)

# ===============================================
# MIXIN Y VIEWSETS DE DATOS
# ===============================================

class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['viewer']

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

class SuscripcionViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    queryset = Suscripcion.objects.all()
    empresa_lookup_field = 'empresa_id__in'

class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()
    empresa_lookup_field = 'empresa_id__in'
    required_roles = ['admin', 'manager']
    
    def perform_create(self, serializer):
        relacion = self.request.user.relaciones.first()
        if not relacion:
            raise serializers.ValidationError("No tienes una empresa asignada.")
        serializer.save(empresa=relacion.empresa)

# ===============================================
# VISTAS DE ANALÍTICAS
# ===============================================

class VentasMensualesView(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['admin', 'manager']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        # <-- CORREGIDO: Se cambió 'fecha' por 'fecha_compra_producto'
        ventas_por_mes = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta').annotate(mes=TruncMonth('fecha_compra_producto')).values('mes').annotate(total_vendido=Sum('cantidad')).order_by('mes')
        
        formatted_data = [{"time": item['mes'].strftime('%Y-%m-%d'), "value": item['total_vendido']} for item in ventas_por_mes]
        return Response(formatted_data)

class TopProductosVendidosView(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['admin', 'manager']

    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        top_productos = Movimiento.objects.filter(producto__empresa=relacion.empresa, tipo='venta').values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:5]
        return Response(list(top_productos))

class ProductoProyeccionesView(APIView):
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['admin', 'manager']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        stocks = Stock.objects.filter(producto__empresa=relacion.empresa).select_related('producto').order_by('producto__nombre')
        fecha_limite = timezone.now().date() - timedelta(days=90)
        
        # <-- CORREGIDO: Se cambió 'fecha__gte' por 'fecha_compra_producto__gte'
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
    permission_classes = [IsAuthenticated, HasRole]
    required_roles = ['admin', 'manager']

    def get(self, request, *args, **kwargs):
        proyecciones_view = ProductoProyeccionesView()
        response = proyecciones_view.get(request, *args, **kwargs)
        if response.status_code != 200: return response
        status_counts = {'Comprar Ahora': 0, 'Revisar Pronto': 0, 'Stock OK': 0}
        for item in response.data:
            if item['estado'] in status_counts: status_counts[item['estado']] += 1
        formatted_data = [{'estado': k, 'count': v} for k, v in status_counts.items()]
        return Response(formatted_data)