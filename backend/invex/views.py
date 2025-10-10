# invex/views.py

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante
from .serializers import *

Usuario = get_user_model()


# ----------------------------------------------------
# SECCIÓN DE AUTENTICACIÓN Y PERFIL
# ----------------------------------------------------

class CustomLoginView(APIView):
    """
    Vista de login que requiere email, password y nombre de la empresa.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        empresa_nombre = request.data.get('empresa')

        if not email or not password or not empresa_nombre:
            return Response(
                {"detail": "Email, contraseña y empresa son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            relacion = user.relaciones.get(empresa__nombre=empresa_nombre)
            user_role = relacion.rol
        except UsuarioEmpresa.DoesNotExist:
            return Response(
                {"detail": f"El usuario no tiene acceso a la empresa '{empresa_nombre}'."},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': user_role
        })


class RegistroView(generics.CreateAPIView):
    """
    Vista para el registro de nuevos usuarios y creación inicial de una empresa.
    """
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
    """
    Vista para obtener los datos del usuario actualmente autenticado.
    Responde a la petición de DashboardLayout.vue.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # DRF se encarga de obtener el usuario a través del token
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# ----------------------------------------------------
# FUNCIÓN AUXILIAR DE FILTRADO
# ----------------------------------------------------

def get_user_companies_ids(user):
    """ Retorna una lista de IDs de las empresas a las que pertenece el usuario. """
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
        empresa = serializer.save() # Guardamos la empresa primero
        # Creamos la relación entre el usuario y la nueva empresa con rol de admin
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