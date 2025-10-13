# invex/views.py
import csv
import io
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Empresa, 
    UsuarioEmpresa, 
    Producto, 
    Stock, 
    Suscripcion, 
    DiaImportante, 
    Categoria
)
from .serializers import (
    UsuarioSerializer, 
    EmpresaSerializer,
    ProductoSerializer,
    StockSerializer,
    SuscripcionSerializer,
    DiaImportanteSerializer,
    FullRegistrationSerializer 
)

Usuario = get_user_model()

# ----------------------------------------------------
# SECCIÓN DE AUTENTICACIÓN Y PERFIL
# ----------------------------------------------------

class CustomLoginView(APIView):
    """
    Gestiona el inicio de sesión del usuario validando email, contraseña y empresa.
    """
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
        except UsuarioEmpresa.DoesNotExist:
            return Response({"detail": f"El usuario no tiene acceso a la empresa '{empresa_nombre}'."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': user_role
        })


class CurrentUserView(APIView):
    """
    Devuelve los datos del usuario autenticado actualmente.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# ----------------------------------------------------
# VISTA PARA EL FLUJO DE PAGO Y REGISTRO
# ----------------------------------------------------
class RegisterAndActivateView(APIView):
    """
    Gestiona el registro final de un usuario después de un pago exitoso.
    Delega la lógica de creación al FullRegistrationSerializer.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        registration_data = request.data.get('registration')
        payment_data = request.data.get('payment')

        if not registration_data or not payment_data:
            return Response({"detail": "Faltan datos de registro o de pago."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FullRegistrationSerializer(data=registration_data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': '¡Usuario y suscripción creados exitosamente!',
                'token': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------
# VISTA DE ACCIÓN PARA IMPORTAR INVENTARIO
# ----------------------------------------------------

class InventarioImportAPIView(APIView):
    """
    Gestiona la importación de inventario desde datos JSON enviados por el frontend.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, empresa_id):
        user = request.user
        empresas_del_usuario = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        if empresa_id not in empresas_del_usuario:
            return Response({"error": "No tienes permiso para acceder a esta empresa."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
        except Empresa.DoesNotExist:
            return Response({"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if not isinstance(data, list) or not data:
            return Response({"error": "Los datos deben ser una lista de productos."}, status=status.HTTP_400_BAD_REQUEST)
        
        return self._procesar_json(data, empresa)

    def _procesar_json(self, productos_data, empresa):
        errores = []
        productos_procesados = 0
        try:
            with transaction.atomic():
                for i, item in enumerate(productos_data):
                    nombre_producto = item.get('nombre')
                    if not nombre_producto:
                        errores.append(f"Fila {i+1}: El nombre del producto es obligatorio.")
                        continue
                    
                    nombre_categoria = item.get('categoria')
                    categoria_obj = None
                    if nombre_categoria and nombre_categoria.strip():
                        categoria_obj, _ = Categoria.objects.get_or_create(
                            empresa=empresa,
                            nombre__iexact=nombre_categoria.strip(),
                            defaults={'nombre': nombre_categoria.strip()}
                        )

                    producto, _ = Producto.objects.update_or_create(
                        empresa=empresa,
                        nombre__iexact=nombre_producto.strip(),
                        defaults={
                            'nombre': nombre_producto.strip(),
                            'unidad_medida': item.get('unidad_medida', 'unidades'),
                            'categoria': categoria_obj
                        }
                    )

                    Stock.objects.update_or_create(
                        producto=producto,
                        defaults={ 'stock_actual': int(item.get('stock_actual', 0) or 0) }
                    )
                    productos_procesados += 1
                
                if errores:
                    raise ValueError("Se encontraron errores de validación.")

        except Exception as e:
            return Response({"error": "No se pudo completar la importación.", "detalles": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensaje": f"Se importaron y/o actualizaron {productos_procesados} productos exitosamente."}, status=status.HTTP_201_CREATED)

# ----------------------------------------------------
# FUNCIÓN AUXILIAR DE FILTRADO
# ----------------------------------------------------

def get_user_companies_ids(user):
    return UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)

# ----------------------------------------------------
# VIEWSETS DE DATOS (PARA OPERACIONES CRUD)
# ----------------------------------------------------

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Empresa.objects.filter(id__in=empresas_ids)
    
    def perform_create(self, serializer):
        empresa = serializer.save()
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')

class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Producto.objects.filter(empresa_id__in=empresas_ids)

class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Stock.objects.filter(producto__empresa_id__in=empresas_ids)

class SuscripcionViewSet(viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Suscripcion.objects.filter(empresa_id__in=empresas_ids)

class DiaImportanteViewSet(viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return DiaImportante.objects.filter(empresa_id__in=empresas_ids)