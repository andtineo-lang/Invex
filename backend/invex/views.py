# invex/views.py

# ===============================================
# IMPORTS (COMBINADOS DE AMBAS VERSIONES)
# ===============================================
import os
import re
from unidecode import unidecode
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone 

from rest_framework import viewsets, generics, status, serializers
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
    Categoria,
    Proveedor, 
    Movimiento 
)
from .serializers import (
    RegistroSerializer,
    UsuarioSerializer,
    EmpresaSerializer,
    ProductoSerializer,
    SuscripcionSerializer,
    DiaImportanteSerializer,
    FullRegistrationSerializer,
    UserManagementSerializer, # Esto venía de tu versión (HEAD)
    InventarioImportSerializer  # Esto venía de main
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
            'refresh': str(refresh), 
            'access': str(refresh.access_token), 
            'rol': user_role,
            'empresa_id': empresa_id 
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
            "rol": result["rol"],
            "empresa_id": empresa_id 
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


# ===============================================
# VISTA DE REGISTRO COMPLETO (CON PAGO)
# ===============================================
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
            
            empresa = Empresa.objects.get(owner=user)
            empresa_id = empresa.id
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': '¡Usuario y suscripción creados exitosamente!',
                'token': str(refresh.access_token),
                'rol': 'admin',
                'empresa_id': empresa_id 
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===============================================
# VIEWSET DE GESTIÓN DE USUARIOS (VERSIÓN FINAL)
# ===============================================
class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Gestiona la creación, listado, actualización y eliminación de usuarios
    dentro de la empresa del usuario autenticado.
    """
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este método asegura que un usuario solo pueda ver y gestionar
        a los miembros de su propia empresa.
        """
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin:
            return UsuarioEmpresa.objects.none()
        return UsuarioEmpresa.objects.filter(empresa=relacion_admin.empresa).select_related('usuario')

    def perform_create(self, serializer):
        """
        Este método se ejecuta después de que el serializer valida los datos.
        Contiene toda la lógica para crear un nuevo usuario (si no existe),
        enviar el correo de bienvenida y asociarlo a la empresa.
        """
        # El serializer ya validó 'nombre_completo' y 'rol'.
        nombre = serializer.validated_data.get('nombre_completo')
        rol = serializer.validated_data.get('rol')
        
        # El email no es parte de la validación del serializer, lo tomamos del request.
        email = self.request.data.get('email')
        
        if not email:
             # Si el email no viene, lanzamos una excepción de validación.
             raise serializers.ValidationError({"error": "El campo email es obligatorio."})

        # --- Lógica para crear o encontrar el usuario por su email ---
        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={'nombre': nombre}
        )
        
        relacion_admin = self.request.user.relaciones.first()
        empresa_actual = relacion_admin.empresa

        # --- Lógica para enviar el correo si el usuario es nuevo ---
        if created:
            password_temporal = get_random_string(12)
            usuario.set_password(password_temporal)
            usuario.save()

            try:
                send_mail(
                    subject=f'¡Bienvenido a {empresa_actual.nombre}!',
                    message=(
                        f'Hola {nombre},\n\n'
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
                print(f"Error al enviar el correo: {e}")
        
        # --- Guardado final de la relación Usuario-Empresa ---
        # Pasamos los objetos 'usuario' y 'empresa' al método save()
        # para que el serializer pueda crear la instancia del modelo 'UsuarioEmpresa'.
        serializer.save(usuario=usuario, empresa=empresa_actual)


# ===============================================
# OTRAS VISTAS Y VIEWSETS
# ===============================================
class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, empresa_id):
        # ... (código sin cambios)
        pass

class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        empresas_ids = UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)
        queryset = super().get_queryset()
        return queryset.filter(**{self.empresa_lookup_field: empresas_ids})

# ----------------------------------------------------
# VIEWSETS DE DATOS
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

# ✅ CAMBIO: Actualizamos este ViewSet
class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()
    empresa_lookup_field = 'empresa_id__in'

    def perform_create(self, serializer):
        """Asigna automáticamente la empresa del usuario al crear un nuevo evento."""
        # Buscamos la primera relación de empresa del usuario que hace la petición
        relacion = self.request.user.relaciones.first()
        if relacion:
            # Guardamos el objeto asignando la empresa encontrada
            serializer.save(empresa=relacion.empresa)
        else:
            # Esto es una validación de seguridad por si el usuario no tiene empresa
            raise serializers.ValidationError("No tienes una empresa asignada para crear este evento.")