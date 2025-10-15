# invex/views.py
import re
from unidecode import unidecode
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
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
    RegistroSerializer,
    UsuarioSerializer,
    EmpresaSerializer,
    ProductoSerializer,
    SuscripcionSerializer,
    DiaImportanteSerializer,
    FullRegistrationSerializer
)

Usuario = get_user_model()

# ----------------------------------------------------
# SECCIÓN DE AUTENTICACIÓN Y PERFIL
# ----------------------------------------------------
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
        except UsuarioEmpresa.DoesNotExist:
            return Response({"detail": f"El usuario no tiene acceso a la empresa '{empresa_nombre}'."}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'rol': user_role})

class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({
            "mensaje": "Registro exitoso",
            "usuario": UsuarioSerializer(result["usuario"]).data,
            "empresa": EmpresaSerializer(result["empresa"]).data,
            "rol": result["rol"]
        })

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class CurrentEmpresaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuario = request.user
        relacion = UsuarioEmpresa.objects.filter(usuario=usuario).first()
        if not relacion:
            return Response({"error": "El usuario no está asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        empresa = relacion.empresa
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)

class MarcarTutorialVistoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.mostrar_tutorial:
            user.mostrar_tutorial = False
            user.save(update_fields=['mostrar_tutorial'])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

# ----------------------------------------------------
# VISTA PARA EL FLUJO DE PAGO Y REGISTRO COMPLETO
# ----------------------------------------------------
class RegisterAndActivateView(APIView):
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
                'token': str(refresh.access_token),
                'rol': 'admin'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------
# SECCIÓN DE GESTIÓN DE USUARIOS
# ----------------------------------------------------
def generar_email_unico(nombre_completo, nombre_empresa):
    base_usuario = unidecode(nombre_completo).lower()
    base_usuario = re.sub(r'\s+', '.', base_usuario)
    base_usuario = re.sub(r'[^a-z0-9.]', '', base_usuario)
    base_dominio = unidecode(nombre_empresa).lower()
    base_dominio = re.sub(r'\s+', '', base_dominio)
    base_dominio = re.sub(r'[^a-z0-9]', '', base_dominio)
    email = f"{base_usuario}@{base_dominio}.com"
    contador = 1
    while Usuario.objects.filter(email=email).exists():
        email = f"{base_usuario}{contador}@{base_dominio}.com"
        contador += 1
    return email

def generar_password_temporal(longitud=12):
    return get_random_string(longitud)

class CrearUsuarioEmpresaView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        nombre_nuevo_usuario = request.data.get('name')
        rol_nuevo_usuario = request.data.get('role')
        if not nombre_nuevo_usuario or not rol_nuevo_usuario:
            return Response({"error": "El nombre y el rol son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)
        
        admin_usuario = request.user
        relacion_admin = UsuarioEmpresa.objects.filter(usuario=admin_usuario).first()
        if not relacion_admin:
            return Response({"error": "No estás asociado a ninguna empresa para poder añadir usuarios."}, status=status.HTTP_403_FORBIDDEN)

        empresa = relacion_admin.empresa
        nuevo_email = generar_email_unico(nombre_nuevo_usuario, empresa.nombre)
        nueva_password = generar_password_temporal()

        try:
            with transaction.atomic():
                nuevo_usuario = Usuario.objects.create_user(
                    email=nuevo_email,
                    password=nueva_password,
                    nombre=nombre_nuevo_usuario
                )
                UsuarioEmpresa.objects.create(
                    usuario=nuevo_usuario,
                    empresa=empresa,
                    rol=rol_nuevo_usuario
                )
            return Response({
                'id': nuevo_usuario.id,
                'name': nuevo_usuario.nombre,
                'email': nuevo_usuario.email,
                'role': rol_nuevo_usuario
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------------------------------
# VISTA DE ACCIÓN PARA IMPORTAR INVENTARIO
# ----------------------------------------------------
class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, empresa_id):
        user = request.user
        empresas_del_usuario = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        if empresa_id not in empresas_del_usuario:
            return Response({"error": "No tienes permiso para acceder a esta empresa."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        if not isinstance(data, list) or not data:
            return Response({"error": "Los datos deben ser una lista de productos."}, status=status.HTTP_400_BAD_REQUEST)
        
        errores = []
        productos_procesados = 0
        try:
            with transaction.atomic():
                empresa = Empresa.objects.get(pk=empresa_id)
                for i, item in enumerate(data):
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
                        defaults={'stock_actual': int(item.get('stock_actual', 0) or 0)}
                    )
                    productos_procesados += 1
                
                if errores:
                    raise ValueError("Se encontraron errores de validación.")

        except Empresa.DoesNotExist:
            return Response({"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "No se pudo completar la importación.", "detalles": errores or [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensaje": f"Se importaron y/o actualizaron {productos_procesados} productos exitosamente."}, status=status.HTTP_201_CREATED)

# ----------------------------------------------------
# MIXIN PARA FILTRAR POR EMPRESA
# ----------------------------------------------------
class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        empresas_ids = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        queryset = super().get_queryset()
        return queryset.filter(**{self.empresa_lookup_field: empresas_ids})

# ----------------------------------------------------
# VIEWSETS DE DATOS (REFACTORIZADOS USANDO EL MIXIN)
# ----------------------------------------------------
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