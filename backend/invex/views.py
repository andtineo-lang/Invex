# invex/views.py
import csv
import io
import re  # <-- NUEVO: Importado para expresiones regulares
from unidecode import unidecode  # <-- NUEVO: Importado para limpiar texto (quitar acentos)
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string  # <-- NUEVO: Para generar contraseñas
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
# VISTA PARA MARCAR TUTORIAL COMO VISTO
# ----------------------------------------------------
class MarcarTutorialVistoView(APIView):
    """
    Actualiza el flag 'mostrar_tutorial' del usuario a False.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.mostrar_tutorial:
            user.mostrar_tutorial = False
            user.save(update_fields=['mostrar_tutorial'])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

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
            return Response(
                {"detail": "Faltan datos de registro o de pago."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
# <-- NUEVA SECCIÓN: GESTIÓN DE USUARIOS
# ----------------------------------------------------

class CrearUsuarioEmpresaView(APIView):
    """
    Crea un nuevo usuario dentro de la empresa del administrador que realiza la solicitud.
    El correo se genera automáticamente a partir del nombre del usuario y la empresa.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        nombre_nuevo_usuario = request.data.get('name')
        rol_nuevo_usuario = request.data.get('role')

        if not nombre_nuevo_usuario or not rol_nuevo_usuario:
            return Response(
                {"error": "El nombre y el rol son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        admin_usuario = request.user
        
        # Asume que el admin pertenece a al menos una empresa.
        relacion_admin = UsuarioEmpresa.objects.filter(usuario=admin_usuario).first()
        
        if not relacion_admin:
            return Response(
                {"error": "No estás asociado a ninguna empresa para poder añadir usuarios."},
                status=status.HTTP_403_FORBIDDEN
            )

        empresa = relacion_admin.empresa
        
        # Generar correo y contraseña usando las funciones auxiliares
        nuevo_email = generar_email_unico(nombre_nuevo_usuario, empresa.nombre)
        nueva_password = generar_password_temporal()

        try:
            with transaction.atomic():
                # Crear el nuevo objeto Usuario
                nuevo_usuario = Usuario.objects.create_user(
                    email=nuevo_email,
                    password=nueva_password,
                    nombre=nombre_nuevo_usuario
                )

                # Vincular el nuevo usuario a la empresa
                UsuarioEmpresa.objects.create(
                    usuario=nuevo_usuario,
                    empresa=empresa,
                    rol=rol_nuevo_usuario
                )

            # Idealmente, aquí se enviaría un email de bienvenida al nuevo_usuario
            # con su correo y contraseña temporal.

            return Response({
                'id': nuevo_usuario.id,
                'name': nuevo_usuario.nombre,
                'email': nuevo_usuario.email,
                'role': rol_nuevo_usuario
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error inesperado al crear el usuario: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ----------------------------------------------------
# VISTA DE ACCIÓN PARA IMPORTAR INVENTARIO
# ----------------------------------------------------

class InventarioImportAPIView(APIView):
    # ... (el resto de esta vista no cambia) ...
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
# <-- NUEVA SECCIÓN: FUNCIONES AUXILIARES
# ----------------------------------------------------

class CurrentEmpresaView(APIView):
    """
    Devuelve los datos de la empresa actual a la que pertenece el usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        
        # Buscamos la primera relación empresa-usuario que tenga
        relacion = UsuarioEmpresa.objects.filter(usuario=usuario).first()
        
        if not relacion:
            return Response(
                {"error": "El usuario no está asociado a ninguna empresa."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        empresa = relacion.empresa
        # Usamos el EmpresaSerializer que ya tienes para devolver los datos
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)



def generar_email_unico(nombre_completo, nombre_empresa):
    """
    Genera una dirección de correo electrónico única a partir de un nombre y una empresa.
    Ej: "Juan Pérez", "Mi Empresa" -> "juan.perez@miempresa.com"
    """
    # 1. Limpia y formatea el nombre de usuario
    base_usuario = unidecode(nombre_completo).lower()
    base_usuario = re.sub(r'\s+', '.', base_usuario)
    base_usuario = re.sub(r'[^a-z0-9.]', '', base_usuario)

    # 2. Limpia y formatea el nombre de la empresa para el dominio
    base_dominio = unidecode(nombre_empresa).lower()
    base_dominio = re.sub(r'\s+', '', base_dominio)
    base_dominio = re.sub(r'[^a-z0-9]', '', base_dominio)

    # 3. Construye el correo y verifica su unicidad
    email = f"{base_usuario}@{base_dominio}.com"
    contador = 1
    while Usuario.objects.filter(email=email).exists():
        email = f"{base_usuario}{contador}@{base_dominio}.com"
        contador += 1
    return email

def generar_password_temporal(longitud=12):
    """Genera una contraseña aleatoria y segura."""
    return get_random_string(longitud)

def get_user_companies_ids(user):
    return UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)

# ----------------------------------------------------
# VIEWSETS DE DATOS (PARA OPERACIONES CRUD)
# ----------------------------------------------------

class EmpresaViewSet(viewsets.ModelViewSet):
    # ... (sin cambios)
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
    # ... (sin cambios)
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Producto.objects.filter(empresa_id__in=empresas_ids)

class StockViewSet(viewsets.ModelViewSet):
    # ... (sin cambios)
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Stock.objects.filter(producto__empresa_id__in=empresas_ids)

class SuscripcionViewSet(viewsets.ModelViewSet):
    # ... (sin cambios)
    serializer_class = SuscripcionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Suscripcion.objects.filter(empresa_id__in=empresas_ids)

class DiaImportanteViewSet(viewsets.ModelViewSet):
    # ... (sin cambios)
    serializer_class = DiaImportanteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return DiaImportante.objects.filter(empresa_id__in=empresas_ids)