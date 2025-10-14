# invex/views.py
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
# CORRECCIÓN: Se añaden los serializers que faltaban y se elimina StockSerializer.
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
# SECCIÓN DE AUTENTICACIÓN Y PERFIL (Sin cambios)
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

# ----------------------------------------------------
# VISTA PARA EL FLUJO DE PAGO Y REGISTRO (Sin cambios)
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
# VISTA DE ACCIÓN PARA IMPORTAR INVENTARIO (Corregida)
# ----------------------------------------------------
class InventarioImportAPIView(APIView):
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
                        empresa=empresa, nombre__iexact=nombre_producto.strip(),
                        defaults={'nombre': nombre_producto.strip(), 'unidad_medida': item.get('unidad_medida', 'unidades'), 'categoria': categoria_obj}
                    )
                    Stock.objects.update_or_create(
                        producto=producto,
                        defaults={'stock_actual': int(item.get('stock_actual', 0) or 0)}
                    )
                    productos_procesados += 1
                # CORRECCIÓN: El 'raise' debe ir después del bucle si hay errores.
                if errores:
                    raise ValueError("Se encontraron errores de validación durante la importación.")
        # CORRECCIÓN: El bloque 'except' debe estar fuera del 'with transaction.atomic()'.
        except Exception as e:
            # Si hay errores, devolvemos los detalles.
            return Response({
                "error": "No se pudo completar la importación.",
                "detalles": errores if errores else [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensaje": f"Se importaron y/o actualizaron {productos_procesados} productos exitosamente."}, status=status.HTTP_201_CREATED)

# ----------------------------------------------------
# MIXIN PARA FILTRAR POR EMPRESA (Refactorizado)
# ----------------------------------------------------
class EmpresaScopeMixin:
    """
    Un Mixin que filtra los resultados para que un usuario solo vea
    los objetos relacionados con las empresas a las que pertenece.
    """
    permission_classes = [IsAuthenticated]
    # Campo a usar para el filtro. Se puede sobreescribir en cada ViewSet.
    empresa_lookup_field = 'empresa_id__in'

    def get_queryset(self):
        user = self.request.user
        # Obtenemos los IDs de las empresas del usuario.
        empresas_ids = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        # Usamos super() para obtener el queryset base del ModelViewSet (ej. Producto.objects.all()).
        queryset = super().get_queryset()
        # Filtramos ese queryset por los IDs de las empresas del usuario.
        return queryset.filter(**{self.empresa_lookup_field: empresas_ids})

# ----------------------------------------------------
# VIEWSETS DE DATOS (Refactorizados y Corregidos)
# ----------------------------------------------------

# CORRECCIÓN: Se elimina la versión duplicada y se aplica el Mixin.
class EmpresaViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()
    # Sobreescribimos el campo de búsqueda para este modelo específico.
    empresa_lookup_field = 'id__in'

    def perform_create(self, serializer):
        # Al crear una empresa, se asigna al usuario como admin.
        empresa = serializer.save()
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')

# CORRECCIÓN: Se aplica el Mixin para filtrar automáticamente.
class ProductoViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()

    def get_serializer_context(self):
        """Pasa el 'request' al serializer para saber qué usuario está creando el producto."""
        return {'request': self.request}

# CORRECCIÓN: Se aplica el Mixin para filtrar automáticamente.
class SuscripcionViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    queryset = Suscripcion.objects.all()

# CORRECCIÓN: Se aplica el Mixin para filtrar automáticamente.
class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()

# CORRECCIÓN: Se elimina por completo el StockViewSet, ya que es redundante.