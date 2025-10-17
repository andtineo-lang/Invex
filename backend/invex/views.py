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
from .serializers import ChangePasswordSerializer

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
    UserManagementSerializer,
    InventarioImportSerializer 
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
# VIEWSET DE GESTIÓN DE USUARIOS
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
        nombre = serializer.validated_data.get('nombre_completo')
        rol = serializer.validated_data.get('rol')
        
        email = self.request.data.get('email')
        
        if not email:
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
        serializer.save(usuario=usuario, empresa=empresa_actual)


# ===============================================
# VISTA DE IMPORTACIÓN MASIVA (COMPLETA)
# ===============================================
class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, empresa_id):
        user = request.user
        
        # 1. Permisos y Contexto de Empresa
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
            if not UsuarioEmpresa.objects.filter(usuario=user, empresa=empresa).exists():
                return Response({"error": "No tienes permiso para acceder a esta empresa."}, status=status.HTTP_403_FORBIDDEN)
        except Empresa.DoesNotExist:
            return Response({"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if not isinstance(data, list) or not data:
            return Response({"error": "Los datos deben ser una lista de productos."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Validación de datos masiva
        serializer = InventarioImportSerializer(data=data, many=True)
        if not serializer.is_valid():
            return Response({"error": "Errores de validación en los datos.", "detalles": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        movimientos_a_crear = []
        proveedores_existentes = {} 

        try:
            with transaction.atomic():
                # 3. Procesamiento de datos validados
                for item in serializer.validated_data:
                    # Extracción de campos de Producto/Stock
                    nombre_producto = item.pop('nombre').strip()
                    stock_actual = item.pop('stock_actual', 0)
                    nombre_categoria = item.pop('categoria')
                    unidad_medida = item.pop('unidad_medida')
                    
                    # Extracción de campos de Movimiento (datos transaccionales)
                    cantidad_comprada = item.pop('cantidad_comprada', None)
                    cantidad_vendida = item.pop('cantidad_vendida', None)
                    nombre_proveedor = item.pop('proveedor')
                    
                    # Usando el campo corregido: fecha_compra_producto
                    fecha_compra_producto = item.pop('fecha_compra_producto', timezone.now().date()) 
                    
                    fecha_pedido = item.pop('fecha_pedido', None)
                    fecha_recepcion = item.pop('fecha_recepcion', None)
                    
                    # Categoria (Crear/Obtener)
                    categoria_obj = None
                    if nombre_categoria:
                        categoria_obj, _ = Categoria.objects.get_or_create(
                            empresa=empresa,
                            nombre__iexact=nombre_categoria.strip(),
                            defaults={'nombre': nombre_categoria.strip()}
                        )

                    # Producto (Crear/Actualizar - Usando nombre como clave única)
                    producto, _ = Producto.objects.update_or_create(
                        empresa=empresa,
                        nombre__iexact=nombre_producto,
                        defaults={
                            'nombre': nombre_producto,
                            'unidad_medida': unidad_medida or 'unidades',
                            'categoria': categoria_obj
                        }
                    )

                    # Stock (Actualizar el stock actual)
                    Stock.objects.update_or_create(
                        producto=producto,
                        defaults={'stock_actual': int(stock_actual or 0)}
                    )
                    
                    # Proveedor (Crear/Obtener)
                    proveedor_obj = None
                    if nombre_proveedor:
                        if nombre_proveedor not in proveedores_existentes:
                            proveedor_obj, _ = Proveedor.objects.get_or_create(
                                empresa=empresa,
                                nombre__iexact=nombre_proveedor.strip(),
                                defaults={'nombre': nombre_proveedor.strip()}
                            )
                            proveedores_existentes[nombre_proveedor] = proveedor_obj
                        proveedor_obj = proveedores_existentes[nombre_proveedor]
                        
                    # 4. Creación de Movimientos (Transacciones)
                    
                    # A. Movimiento de Compra
                    if cantidad_comprada is not None and int(cantidad_comprada) > 0:
                        movimientos_a_crear.append(Movimiento(
                            producto=producto,
                            tipo='compra',
                            cantidad=int(cantidad_comprada),
                            unidad_medida=unidad_medida,
                            fecha_compra_producto=fecha_compra_producto, 
                            proveedor=proveedor_obj,
                            fecha_pedido=fecha_pedido,
                            fecha_recepcion=fecha_recepcion,
                        ))
                    
                    # B. Movimiento de Venta
                    if cantidad_vendida is not None and int(cantidad_vendida) > 0:
                        movimientos_a_crear.append(Movimiento(
                            producto=producto,
                            tipo='venta',
                            cantidad=int(cantidad_vendida),
                            unidad_medida=unidad_medida,
                            fecha_compra_producto=fecha_compra_producto, 
                            # Las ventas no tienen proveedor
                        ))
                
                # Creación masiva de movimientos
                Movimiento.objects.bulk_create(movimientos_a_crear)
                
        except Exception as e:
            # Revertir transacción si falla cualquier paso
            return Response({"error": f"Error de base de datos durante el procesamiento.", "detalles": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        productos_procesados = len(serializer.validated_data)
        movimientos_creados = len(movimientos_a_crear)

        return Response({
            "mensaje": f"Se procesaron {productos_procesados} filas. Productos actualizados y {movimientos_creados} movimientos creados exitosamente.",
            "productos_actualizados": productos_procesados,
            "movimientos_creados": movimientos_creados
        }, status=status.HTTP_201_CREATED)


# ===============================================
# MIXIN Y VIEWSETS DE DATOS
# ===============================================
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

class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()
    empresa_lookup_field = 'empresa_id__in'

    def perform_create(self, serializer):
        """Asigna automáticamente la empresa del usuario al crear un nuevo evento."""
        relacion = self.request.user.relaciones.first()
        if relacion:
            serializer.save(empresa=relacion.empresa)
        else:
            raise serializers.ValidationError("No tienes una empresa asignada para crear este evento.")