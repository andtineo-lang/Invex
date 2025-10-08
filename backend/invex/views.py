# invex/views.py
from rest_framework import viewsets, generics
from rest_framework.response import Response
# Importamos los permisos necesarios
from rest_framework.permissions import AllowAny, IsAuthenticated 
from .models import Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante
from .serializers import *


# ----------------------------------------------------
# FUNCIÓN AUXILIAR DE FILTRADO
# ----------------------------------------------------

def get_user_companies_ids(user):
    """ Retorna una lista de IDs de las empresas a las que pertenece el usuario. """
    # Busca todas las relaciones donde el usuario es miembro y extrae solo los IDs de las empresas.
    return UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)


# ----------------------------------------------------
# AUTENTICACIÓN
# ----------------------------------------------------

class RegistroView(generics.CreateAPIView):
    """ Vista para el registro de nuevos usuarios y creación inicial de una empresa. """
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny] # El registro debe estar disponible para cualquiera

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        # En el registro, solo se devuelve la información necesaria para el frontend
        return Response({
            "mensaje": "Registro exitoso",
            "usuario": UsuarioSerializer(result["usuario"]).data,
            "empresa": EmpresaSerializer(result["empresa"]).data,
            "rol": result["rol"]
        })


# ----------------------------------------------------
# VIEWSETS DE DATOS (Requieren Autenticación y Filtrado)
# ----------------------------------------------------

class EmpresaViewSet(viewsets.ModelViewSet):
    """ CRUD para Empresas. Filtra para mostrar solo las empresas del usuario autenticado. """
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios logueados pueden acceder

    def get_queryset(self):
        # Sobreescribe el queryset para filtrar por las empresas donde el usuario es miembro
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Empresa.objects.filter(id__in=empresas_ids)

    def perform_create(self, serializer):
        # Asegura que el usuario autenticado sea el dueño y crea la relación admin.
        empresa = serializer.save(owner=self.request.user)
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')


class ProductoViewSet(viewsets.ModelViewSet):
    """ CRUD para Productos. Filtra productos que pertenecen a las empresas del usuario. """
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        # Filtra productos cuya empresa_id está en la lista de empresas del usuario
        return Producto.objects.filter(empresa_id__in=empresas_ids)


class StockViewSet(viewsets.ModelViewSet):
    """ CRUD para Stock. Filtra el stock asociado a los productos de las empresas del usuario. """
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        # Filtra el stock basado en los productos de las empresas del usuario
        return Stock.objects.filter(producto__empresa_id__in=empresas_ids)


class SuscripcionViewSet(viewsets.ModelViewSet):
    """ CRUD para Suscripción. Filtra por la suscripción de las empresas del usuario. """
    serializer_class = SuscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        # Filtra la suscripción cuya empresa_id está en la lista de empresas del usuario
        return Suscripcion.objects.filter(empresa_id__in=empresas_ids)


class DiaImportanteViewSet(viewsets.ModelViewSet):
    """ CRUD para Días Importantes. Filtra por la empresa del usuario. """
    serializer_class = DiaImportanteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        # Filtra los días importantes cuya empresa_id está en la lista de empresas del usuario
        return DiaImportante.objects.filter(empresa_id__in=empresas_ids)