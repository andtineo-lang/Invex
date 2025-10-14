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

# ---- VISTA RESTAURADA ----
class CurrentEmpresaView(APIView):
    """
    Devuelve los datos de la empresa actual a la que pertenece el usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        relacion = UsuarioEmpresa.objects.filter(usuario=usuario).first()
        if not relacion:
            return Response(
                {"error": "El usuario no está asociado a ninguna empresa."},
                status=status.HTTP_404_NOT_FOUND
            )
        empresa = relacion.empresa
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)

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
    # ... (Lógica sin cambios)
    pass

def generar_password_temporal(longitud=12):
    # ... (Lógica sin cambios)
    pass

class CrearUsuarioEmpresaView(APIView):
    # ... (Lógica sin cambios)
    pass

# ----------------------------------------------------
# VISTA DE ACCIÓN PARA IMPORTAR INVENTARIO
# ----------------------------------------------------
class InventarioImportAPIView(APIView):
    # ... (Lógica sin cambios)
    pass

# ----------------------------------------------------
# MIXIN PARA FILTRAR POR EMPRESA
# ----------------------------------------------------
class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated]
    empresa_lookup_field = 'empresa_id__in'
    def get_queryset(self):
        user = self.request.user
        empresas_ids = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        queryset = super().get_queryset()
        return queryset.filter(**{self.empresa_lookup_field: empresas_ids})

# ----------------------------------------------------
# VIEWSETS DE DATOS (Refactorizados)
# ----------------------------------------------------

class EmpresaViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()
    empresa_lookup_field = 'id__in'
    def perform_create(self, serializer):
        empresa = serializer.save()
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')

class ProductoViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    def get_serializer_context(self):
        return {'request': self.request}

class SuscripcionViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    queryset = Suscripcion.objects.all()

class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()