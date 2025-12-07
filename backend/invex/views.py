# invex/views.py (VERSIÓN FINAL ACTUALIZADA)

import os
import re
from unidecode import unidecode
import logging
from datetime import timedelta
from django.utils.html import strip_tags 
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField, Count, Case, When, Value, CharField, FloatField, Q, Min
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404

# 👇 --- IMPORTS DE TRANSBANK ---
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions          # <--- NUEVO
from transbank.common.integration_type import IntegrationType # <--- NUEVO

# 👇 --- IMPORTS PARA RESETEO ---
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
# ---------------------------

from rest_framework import viewsets, generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError 

from .permissions import HasRole
from .models import (
    Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion,
    DiaImportante, Categoria, Proveedor, Movimiento
)
from .serializers import (
    UsuarioSerializer, EmpresaSerializer, ProductoSerializer,
    SuscripcionSerializer, DiaImportanteSerializer, FullRegistrationSerializer,
    UserManagementSerializer, RegistroSerializer,
    MasterImportSerializer,
    ProyeccionCalculadaSerializer,
    EmpresaConfiguracionSerializer,
    ChangePasswordSerializer 
)

Usuario = get_user_model()
logger = logging.getLogger(__name__)

# ===============================================
# CONFIGURACIÓN DE UMBRALES
# ===============================================

class InventarioConfig:
    """Configuración centralizada para cálculos de inventario"""
    SEMANAS_DE_SEGURIDAD = 2
    SEMANAS_OBJETIVO_COMPRA = 4
    DIAS_ANALISIS_DEMANDA = 90
    UMBRAL_SOBRESTOCK_SEMANAS = 12 
    UMBRAL_DEMANDA_MINIMA = 0.5 


# ===============================================
# VISTA DE CAMBIO DE CONTRASEÑA
# ===============================================

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Contraseña actualizada exitosamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ===============================================
# VISTAS DE AUTENTICACIÓN Y PERFIL
# ===============================================

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        empresa_nombre = request.data.get('empresa') 
        
        if not email or not password:
            return Response({"detail": "Email y contraseña son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if empresa_nombre:
            try:
                relacion = user.relaciones.get(empresa__nombre=empresa_nombre)
            except UsuarioEmpresa.DoesNotExist:
                return Response({"detail": "No tienes acceso a esa empresa."}, status=status.HTTP_403_FORBIDDEN)
        else:
            relacion = user.relaciones.first()
            if not relacion:
                return Response({"detail": "Usuario no asociado a ninguna empresa."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': relacion.rol,
            'empresa_id': relacion.empresa.id
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
        # El serializer ahora calcula el 'subscription_status' heredado
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class CurrentEmpresaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response({"error": "El usuario no está asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(relacion.empresa)
        return Response(serializer.data)


class EmpresaConfiguracionView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager']
    
    def get(self, request):
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response({"error": "El usuario no está asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaConfiguracionSerializer(relacion.empresa)
        return Response(serializer.data)
    
    def patch(self, request):
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response({"error": "El usuario no está asociado a ninguna empresa."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaConfiguracionSerializer(relacion.empresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Configuración actualizada.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarcarTutorialVistoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if hasattr(user, 'mostrar_tutorial') and user.mostrar_tutorial:
            user.mostrar_tutorial = False
            user.save(update_fields=['mostrar_tutorial'])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class RegisterAndActivateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = FullRegistrationSerializer(data=request.data.get('registration'))
        if serializer.is_valid():
            user = serializer.save()
            empresa = Empresa.objects.get(owner=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': '¡Usuario y suscripción creados exitosamente!',
                'token': str(refresh.access_token),
                'rol': 'admin',
                'empresa_id': empresa.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementViewSet(viewsets.ModelViewSet):
    serializer_class = UserManagementSerializer
    permission_classes = [HasRole]
    allowed_roles = [] 
    
    def get_queryset(self):
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin:
             return UsuarioEmpresa.objects.none()
        return UsuarioEmpresa.objects.filter(empresa=relacion_admin.empresa).select_related('usuario')
    
    def perform_create(self, serializer):
        # 1. Validación de datos
        nombre = serializer.validated_data.get('nombre_completo')
        rol = serializer.validated_data.get('rol')
        email = self.request.data.get('email')
        
        if not email:
             raise serializers.ValidationError({"error": "El campo email es obligatorio."})
        
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin:
             raise serializers.ValidationError({"error": "No tienes una empresa asignada para invitar usuarios."})
        empresa_actual = relacion_admin.empresa

        # 2. Gestión del Usuario
        usuario, created = Usuario.objects.get_or_create(
            email=email,
            defaults={'nombre': nombre}
        )

        # Evitar duplicados en la misma empresa
        if not created:
            if UsuarioEmpresa.objects.filter(usuario=usuario, empresa=empresa_actual).exists():
                raise serializers.ValidationError({"error": f"El usuario {email} ya pertenece a esta empresa."})

        # 3. Envío de Correo HTML
        try:
            FRONTEND_URL = "http://localhost:8080" # Ajusta si tu puerto cambia
            login_link = f"{FRONTEND_URL}/login"
            
            # Estilos base para reutilizar
            style_container = "font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;"
            style_header = "background-color: #0f766e; padding: 20px; text-align: center;"
            style_h1 = "color: #ffffff; margin: 0; font-size: 24px; letter-spacing: 1px;"
            style_body = "padding: 30px; color: #374151; font-size: 16px; line-height: 1.6;"
            style_btn = "display: inline-block; background-color: #0f766e; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 20px;"
            style_footer = "background-color: #f9fafb; padding: 15px; text-align: center; border-top: 1px solid #e5e7eb; font-size: 12px; color: #9ca3af;"

            if created:
                # === USUARIO NUEVO (Con Contraseña) ===
                password_temporal = get_random_string(12)
                usuario.set_password(password_temporal)
                usuario.save()

                asunto = f'Bienvenido a {empresa_actual.nombre} - Credenciales de Acceso'
                
                html_message = f"""
                <div style="{style_container}">
                    <div style="{style_header}">
                        <h1 style="{style_h1}">INVEX</h1>
                    </div>
                    <div style="{style_body}">
                        <h2 style="color: #111827; margin-top: 0;">¡Bienvenido al equipo, {nombre}!</h2>
                        <p>Has sido invitado a formar parte de la empresa <strong>"{empresa_actual.nombre}"</strong> en INVEX con el rol de <strong>{rol}</strong>.</p>
                        
                        <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; border-left: 4px solid #0f766e; margin: 20px 0;">
                            <p style="margin: 0 0 10px 0; font-weight: bold; color: #0f766e;">Tus credenciales temporales:</p>
                            <p style="margin: 5px 0;"><strong>Usuario:</strong> {email}</p>
                            <p style="margin: 5px 0;"><strong>Contraseña:</strong> <span style="font-family: monospace; background: #fff; padding: 2px 6px; border-radius: 4px;">{password_temporal}</span></p>
                        </div>

                        <p style="font-size: 14px; color: #6b7280;">Por seguridad, te pedimos que cambies tu contraseña al ingresar por primera vez.</p>
                        
                        <div style="text-align: center;">
                            <a href="{login_link}" style="{style_btn}">Iniciar Sesión</a>
                        </div>
                    </div>
                    <div style="{style_footer}">
                        &copy; 2025 Invex. Todos los derechos reservados.
                    </div>
                </div>
                """
            else:
                # === USUARIO EXISTENTE (Sin Contraseña) ===
                asunto = f'Nueva invitación: Te uniste a {empresa_actual.nombre}'
                
                html_message = f"""
                <div style="{style_container}">
                    <div style="{style_header}">
                        <h1 style="{style_h1}">INVEX</h1>
                    </div>
                    <div style="{style_body}">
                        <h2 style="color: #111827; margin-top: 0;">¡Hola de nuevo, {usuario.nombre}!</h2>
                        <p>Te informamos que se te ha concedido acceso a la empresa <strong>"{empresa_actual.nombre}"</strong> con el rol de <strong>{rol}</strong>.</p>
                        
                        <div style="background-color: #ecfdf5; padding: 15px; border-radius: 8px; margin: 20px 0; color: #065f46;">
                            <strong>✨ No necesitas una nueva contraseña.</strong><br>
                            Como ya tienes una cuenta en INVEX, puedes acceder utilizando tus credenciales habituales.
                        </div>

                        <div style="text-align: center;">
                            <a href="{login_link}" style="{style_btn}">Ir al Dashboard</a>
                        </div>
                    </div>
                    <div style="{style_footer}">
                        &copy; 2025 Invex. Todos los derechos reservados.
                    </div>
                </div>
                """

            # Generar versión texto plano para clientes de correo antiguos
            plain_message = strip_tags(html_message)

            send_mail(
                subject=asunto,
                message=plain_message,
                from_email=os.environ.get('EMAIL_HOST_USER'),
                recipient_list=[email],
                html_message=html_message, # <--- Aquí va el HTML
                fail_silently=False,
            )

        except Exception as e:
            print(f"❌ Error enviando correo: {str(e)}")

        serializer.save(usuario=usuario, empresa=empresa_actual)

# ===============================================
# RECUPERACIÓN DE CONTRASEÑA
# ===============================================
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        # Tu lógica original (directa y funcional)
        email = request.data.get('email')
        if not email:
             return Response({"error": "Email requerido"}, status=status.HTTP_400_BAD_REQUEST)
             
        user = Usuario.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            FRONTEND_URL = "http://localhost:8080" 
            reset_link = f"{FRONTEND_URL}/reset-password?uid={uid}&token={token}"

            # --- AQUÍ EMPIEZA EL DISEÑO BONITO ---
            subject = 'Recupera tu acceso a INVEX'
            
            # Plantilla HTML con estilos en línea (para que funcione en Gmail/Outlook)
            html_message = f"""
            <div style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #0f766e; padding: 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; letter-spacing: 1px;">INVEX</h1>
                </div>
                <div style="padding: 30px;">
                    <h2 style="color: #111827; margin-top: 0; font-size: 20px;">¿Olvidaste tu contraseña?</h2>
                    <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">
                        Hola <strong>{user.nombre}</strong>,<br><br>
                        Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. 
                        Haz clic en el siguiente botón para crear una nueva clave:
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" style="background-color: #0f766e; color: #ffffff; padding: 14px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            Restablecer Contraseña
                        </a>
                    </div>
                    <p style="color: #6b7280; font-size: 14px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        Si no solicitaste este cambio, puedes ignorar este correo de forma segura. El enlace expirará en 24 horas.
                    </p>
                </div>
                <div style="background-color: #f9fafb; padding: 15px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                        &copy; 2025 Invex. Todos los derechos reservados.
                    </p>
                </div>
            </div>
            """
            
            # Generamos versión texto plano por si el gestor de correo no lee HTML
            plain_message = strip_tags(html_message) 

            try:
                send_mail(
                    subject=subject,
                    message=plain_message, # Mensaje plano obligatorio
                    from_email=os.environ.get('EMAIL_HOST_USER'),
                    recipient_list=[email],
                    html_message=html_message, # <--- AQUÍ VA EL HTML
                    fail_silently=False,
                )
            except Exception as e:
                # Opcional: Imprimir error en consola para depurar
                print(f"Error enviando correo: {e}")
                return Response({"error": "Error al enviar el correo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Si el correo existe, se ha enviado un enlace."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Se asume uso del serializer PasswordResetConfirmSerializer definido en serializers.py
        from .serializers import PasswordResetConfirmSerializer
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ===============================================
# VISTA DE IMPORTACIÓN MASIVA (CON HERENCIA DE PLAN)
# ===============================================

class InventarioImportAPIView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager'] 

    def _find_key_value(self, item_dict, possible_keys):
        normalized_dict = {
            unidecode(str(k).lower().replace('_', '').replace(' ', '')): v 
            for k, v in item_dict.items()
        }
        for key in possible_keys:
            normalized_key = unidecode(key.lower().replace('_', '').replace(' ', ''))
            if normalized_key in normalized_dict:
                return normalized_dict[normalized_key]
        return None

    def post(self, request, empresa_id):
        empresa = get_object_or_404(Empresa, id=empresa_id)
        user = request.user
        
        serializer = MasterImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        data_productos = validated_data.get('productos', [])
        data_historial_ventas = validated_data.get('historial_ventas', [])
        data_historial_compras = validated_data.get('historial_compras', [])

        # 🔥 BLOQUEO DE SEGURIDAD (HERENCIA): VERIFICAR EL PLAN DEL DUEÑO 🔥
        # No importa quién sube el archivo, importa qué plan paga el dueño de la empresa.
        plan_actual = empresa.subscription_status

        if plan_actual == 'free':
            cant_productos_actuales = Producto.objects.filter(empresa=empresa).count()
            cant_nuevos = len(data_productos)
            LIMITE_FREE = 50

            if (cant_productos_actuales + cant_nuevos) > LIMITE_FREE:
                return Response({
                    "error": f"El plan Gratuito de la empresa solo permite {LIMITE_FREE} productos. "
                             f"Actualmente hay {cant_productos_actuales} y se intentan añadir {cant_nuevos}. "
                             f"El dueño debe actualizar a PRO."
                }, status=status.HTTP_400_BAD_REQUEST)
        # -------------------------------------

        try:
            with transaction.atomic():
                productos_cache = {}
                categorias_cache = {}
                proveedores_cache = {}

                # PASO 1: Procesar PRODUCTOS
                for item_prod in data_productos:
                    prod_nombre = item_prod.get('nombre')
                    if not prod_nombre: continue

                    cat_nombre = item_prod.get('categoria')
                    categoria_obj = None
                    if cat_nombre and str(cat_nombre).strip():
                        cat_nombre_limpio = str(cat_nombre).strip()
                        cat_nombre_lower = cat_nombre_limpio.lower()
                        
                        if cat_nombre_lower not in categorias_cache:
                            categorias_cache[cat_nombre_lower], _ = Categoria.objects.get_or_create(
                                empresa=empresa, 
                                nombre__iexact=cat_nombre_limpio,
                                defaults={'nombre': cat_nombre_limpio}
                            )
                        categoria_obj = categorias_cache[cat_nombre_lower]

                    producto_obj, _ = Producto.objects.update_or_create(
                        empresa=empresa,
                        nombre__iexact=prod_nombre,
                        defaults={
                            'nombre': prod_nombre,
                            'categoria': categoria_obj,
                            'unidad_medida': item_prod.get('unidad_medida', 'unidades')
                        }
                    )
                    productos_cache[prod_nombre.lower()] = producto_obj

                    stock_actual = item_prod.get('stock_actual', 0)
                    Stock.objects.update_or_create(
                        producto=producto_obj,
                        defaults={'stock_actual': stock_actual}
                    )
                    
                    Movimiento.objects.update_or_create(
                        producto=producto_obj,
                        tipo='ajuste',
                        notas='Importación inicial de inventario.',
                        defaults={
                            'cantidad': stock_actual,
                            'fecha_compra_producto': timezone.now().date()
                        }
                    )

                # PASO 2: Procesar HISTORIAL DE VENTAS
                movimientos_ventas_a_crear = []
                for item_venta in data_historial_ventas:
                    nombre_prod = self._find_key_value(item_venta, ['producto', 'nombre', 'item', 'articulo'])
                    cantidad_str = self._find_key_value(item_venta, ['cantidad_vendida', 'vendida', 'cantidad', 'unidades'])
                    fecha = self._find_key_value(item_venta, ['fecha_compra_producto', 'fecha', 'date'])

                    if not nombre_prod or not cantidad_str or not fecha: continue
                    
                    producto_obj = productos_cache.get(str(nombre_prod).lower())
                    if not producto_obj: continue
                    
                    try:
                        cantidad_num = int(float(cantidad_str))
                    except (ValueError, TypeError): continue

                    movimientos_ventas_a_crear.append(
                        Movimiento(
                            producto=producto_obj,
                            tipo='venta',
                            cantidad=cantidad_num,
                            fecha_compra_producto=fecha
                        )
                    )

                # PASO 3: Procesar HISTORIAL DE COMPRAS
                movimientos_compras_a_crear = []
                for item_compra in data_historial_compras:
                    nombre_prod = self._find_key_value(item_compra, ['producto', 'nombre', 'item', 'articulo'])
                    cantidad_str = self._find_key_value(item_compra, ['cantidad_comprada', 'comprada', 'cantidad', 'unidades'])
                    fecha_ped = self._find_key_value(item_compra, ['fecha_pedido', 'f_pedido', 'fechaorden'])
                    fecha_rec = self._find_key_value(item_compra, ['fecha_recepcion', 'f_recepcion', 'fecharecibida'])
                    nombre_prov = self._find_key_value(item_compra, ['proveedor', 'suplidor', 'vendor'])
                    fecha_venc = self._find_key_value(item_compra, ['fecha_vencimiento', 'vencimiento', 'caducidad', 'f_venc'])
                    
                    if not nombre_prod or not cantidad_str: continue
                    
                    producto_obj = productos_cache.get(str(nombre_prod).lower())
                    if not producto_obj: continue

                    proveedor_obj = None
                    if nombre_prov and str(nombre_prov).strip():
                        nombre_prov_limpio = str(nombre_prov).strip()
                        prov_nombre_lower = nombre_prov_limpio.lower()
                        if prov_nombre_lower not in proveedores_cache:
                            proveedores_cache[prov_nombre_lower], _ = Proveedor.objects.get_or_create(
                                empresa=empresa, 
                                nombre__iexact=nombre_prov_limpio,
                                defaults={'nombre': nombre_prov_limpio}
                            )
                        proveedor_obj = proveedores_cache[prov_nombre_lower]
                    
                    try:
                        cantidad_num = int(float(cantidad_str))
                    except (ValueError, TypeError): continue

                    movimientos_compras_a_crear.append(
                        Movimiento(
                            producto=producto_obj,
                            tipo='compra',
                            cantidad=cantidad_num,
                            fecha_pedido=fecha_ped,
                            fecha_recepcion=fecha_rec,
                            fecha_vencimiento=fecha_venc,
                            fecha_compra_producto=fecha_rec or fecha_ped or timezone.now().date(),
                            proveedor=proveedor_obj
                        )
                    )

                Movimiento.objects.bulk_create(movimientos_ventas_a_crear)
                Movimiento.objects.bulk_create(movimientos_compras_a_crear)

        except Exception as e:
            logger.error(f"[Importación] Error: {str(e)}", exc_info=True)
            return Response(
                {"error": f"Error durante la importación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"mensaje": f"Importación exitosa. {len(data_productos)} productos procesados."},
            status=status.HTTP_201_CREATED
        )


# ===============================================
# MIXIN Y VIEWSETS DE DATOS
# ===============================================

class EmpresaScopeMixin:
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        empresas_ids = UsuarioEmpresa.objects.filter(
            usuario=self.request.user
        ).values_list('empresa_id', flat=True)
        return super().get_queryset().filter(**{self.empresa_lookup_field: empresas_ids})


class EmpresaViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()
    empresa_lookup_field = 'id__in'
    
    def perform_create(self, serializer):
        empresa = serializer.save(owner=self.request.user)
        UsuarioEmpresa.objects.create(
            usuario=self.request.user, 
            empresa=empresa, 
            rol='admin'
        )


class ProductoViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all().prefetch_related('stocks') 
    empresa_lookup_field = 'empresa_id__in'

    # Activamos el permiso dinámico
    permission_classes = [HasRole]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        permission = HasRole()
        if self.action == 'create':
            self.allowed_roles = ['manager']
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.allowed_roles = ['worker']
        else:
            self.allowed_roles = ['manager', 'worker']
        return [permission]

    # 🔥 BLOQUEO DE SEGURIDAD (HERENCIA): PLAN FREE 🔥
    def perform_create(self, serializer):
        user = self.request.user
        relacion = user.relaciones.first()
        
        if not relacion:
            raise ValidationError({"detail": "No tienes una empresa asignada para crear productos."})

        # Verificamos el plan del DUEÑO
        plan_actual = relacion.empresa.owner.subscription_status

        if plan_actual == 'free':
            cantidad_actual = Producto.objects.filter(empresa=relacion.empresa).count()
            if cantidad_actual >= 50:
                raise ValidationError({"detail": "La empresa ha alcanzado el límite de 50 productos del plan gratuito."})

        serializer.save(empresa=relacion.empresa)

class SuscripcionViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = SuscripcionSerializer
    queryset = Suscripcion.objects.all()
    empresa_lookup_field = 'empresa_id__in'
    permission_classes = [HasRole]
    allowed_roles = ['manager']


class DiaImportanteViewSet(EmpresaScopeMixin, viewsets.ModelViewSet):
    serializer_class = DiaImportanteSerializer
    queryset = DiaImportante.objects.all()
    empresa_lookup_field = 'empresa_id__in'
    permission_classes = [HasRole]
    allowed_roles = ['manager']
    
    def perform_create(self, serializer):
        relacion = self.request.user.relaciones.first()
        if not relacion:
            raise serializers.ValidationError("No tienes una empresa asignada.")
        serializer.save(empresa=relacion.empresa)

# ===============================================
# FUNCIÓN HELPER PARA CALCULAR PROYECCIONES
# ===============================================

def calcular_proyecciones_inventario(empresa, dias_analisis=None):
    config_semanas_seguridad = empresa.semanas_seguridad
    config_semanas_objetivo = empresa.semanas_objetivo
    config_dias_analisis = dias_analisis if dias_analisis is not None else empresa.dias_analisis_demanda
    
    MAX_LEAD_TIME_RAZONABLE = empresa.max_lead_time_razonable or 60
    LEAD_TIME_DEFECTO = empresa.lead_time_defecto or 7
    BUFFER_VENTA_SEMANAS = empresa.buffer_venta_semanas or 2
    UMBRAL_DEMANDA_MINIMA = empresa.umbral_demanda_minima if empresa.umbral_demanda_minima is not None else 0.5
    UMBRAL_SOBRESTOCK_SEMANAS = empresa.umbral_sobrestock_semanas or 12
    
    fecha_limite = timezone.now().date() - timedelta(days=config_dias_analisis)
    hoy = timezone.now().date()

    stocks = Stock.objects.filter(
        producto__empresa=empresa
    ).select_related('producto').order_by('producto__nombre')
    
    ventas_recientes = Movimiento.objects.filter(
        producto__empresa=empresa, 
        tipo='venta', 
        fecha_compra_producto__gte=fecha_limite
    ).values('producto_id').annotate(total_vendido=Sum('cantidad'))
    
    demanda_map = {item['producto_id']: item['total_vendido'] for item in ventas_recientes}
    
    compras_historicas = Movimiento.objects.filter(
        producto__empresa=empresa,
        tipo='compra',
        fecha_pedido__isnull=False,
        fecha_recepcion__isnull=False
    ).values('producto_id', 'fecha_pedido', 'fecha_recepcion')

    lead_time_map = {}
    tiempos_por_producto = {}

    for compra in compras_historicas:
        pid = compra['producto_id']
        dias = (compra['fecha_recepcion'] - compra['fecha_pedido']).days
        if 0 <= dias <= MAX_LEAD_TIME_RAZONABLE:
            if pid not in tiempos_por_producto: tiempos_por_producto[pid] = []
            tiempos_por_producto[pid].append(dias)

    for pid, tiempos in tiempos_por_producto.items():
        if tiempos: lead_time_map[pid] = int(sum(tiempos) / len(tiempos))
        else: lead_time_map[pid] = LEAD_TIME_DEFECTO

    vencimientos_query = Movimiento.objects.filter(
        producto__empresa=empresa,
        tipo__in=['compra', 'ajuste'],
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__gte=hoy
    ).values('producto_id').annotate(
        proximo_vencimiento=Min('fecha_vencimiento') 
    )
    vencimientos_map = {v['producto_id']: v['proximo_vencimiento'] for v in vencimientos_query}

    proyecciones = []
    
    for stock in stocks:
        total_vendido = demanda_map.get(stock.producto.id, 0)
        
        if total_vendido > 0:
            demanda_semanal = (total_vendido / config_dias_analisis) * 7
        else:
            demanda_semanal = 0
        demanda_semanal = round(demanda_semanal, 2)
        
        lead_time_dias = lead_time_map.get(stock.producto.id, LEAD_TIME_DEFECTO)
        lead_time_semanas = round(lead_time_dias / 7, 1)
        
        semanas_cobertura = None
        estado = "Stock OK"
        cantidad_sugerida = 0
        punto_reorden = 0
        dias_para_comprar = None
        
        if demanda_semanal < UMBRAL_DEMANDA_MINIMA:
            semanas_cobertura = None
            # Nuevo estado: Inactivo (sin stock Y sin demanda)
            if stock.stock_actual == 0:
                estado = "Inactivo"
            elif stock.stock_actual < 10:
                estado = "Stock OK"
            else:
                estado = "Sobrestock"
        else:
            semanas_cobertura = round(stock.stock_actual / demanda_semanal, 1)
            
            semanas_objetivo_final = config_semanas_objetivo
            fecha_venc = vencimientos_map.get(stock.producto.id)
            
            if fecha_venc:
                dias_vida_util = (fecha_venc - hoy).days
                semanas_vida_util = dias_vida_util / 7
                techo_seguro = max(0, semanas_vida_util - BUFFER_VENTA_SEMANAS)
                
                if techo_seguro < semanas_objetivo_final:
                    semanas_objetivo_final = techo_seguro

            stock_durante_lead_time = demanda_semanal * lead_time_semanas
            stock_seguridad = demanda_semanal * config_semanas_seguridad
            punto_reorden = int(stock_durante_lead_time + stock_seguridad)
            
            if stock.stock_actual <= punto_reorden:
                estado = "Comprar Ahora"
                dias_para_comprar = 0
                stock_maximo_deseado = (demanda_semanal * semanas_objetivo_final) + punto_reorden
                cantidad_necesaria = stock_maximo_deseado - stock.stock_actual
                cantidad_sugerida = max(0, int(cantidad_necesaria))
            else:
                exceso_sobre_reorden = stock.stock_actual - punto_reorden
                demanda_diaria = demanda_semanal / 7
                if demanda_diaria > 0:
                    dias_para_comprar = int(exceso_sobre_reorden / demanda_diaria)
                
                if dias_para_comprar is not None and dias_para_comprar <= 7:
                    estado = "Revisar Pronto"
                elif semanas_cobertura > UMBRAL_SOBRESTOCK_SEMANAS:
                    estado = "Sobrestock"
                else:
                    estado = "Stock OK"
        
        proyecciones.append({
            'id': stock.id,
            'producto_id': stock.producto.id,
            'producto_nombre': stock.producto.nombre,
            'stock_actual': stock.stock_actual,
            'demanda_semanal_proyectada': demanda_semanal,
            'semanas_cobertura': semanas_cobertura,
            'estado': estado,
            'cantidad_sugerida': cantidad_sugerida, 
            'lead_time_dias': lead_time_dias,
            'lead_time_semanas': lead_time_semanas,
            'punto_reorden': punto_reorden,
            'dias_para_comprar': dias_para_comprar,
        })
    
    return proyecciones

# ===============================================
# VISTAS DE ANALÍTICAS
# ===============================================

class VentasHistoricasView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        ventas_por_dia = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).values('fecha_compra_producto').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('fecha_compra_producto')
        
        formatted_data = [
            {"time": item['fecha_compra_producto'].strftime('%Y-%m-%d'), "value": item['total_vendido']} 
            for item in ventas_por_dia
        ]
        return Response(formatted_data)


class VentasMensualesView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        ventas_por_mes = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).annotate(
            mes=TruncMonth('fecha_compra_producto')
        ).values('mes').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('mes')
        
        formatted_data = [
            {"time": item['mes'].strftime('%Y-%m-%d'), "value": item['total_vendido']} 
            for item in ventas_por_mes
        ]
        return Response(formatted_data)


class TopProductosVendidosView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        top_productos = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).values('producto__nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:5]
        
        return Response(list(top_productos))


class ProductoProyeccionesView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        proyecciones = calcular_proyecciones_inventario(relacion.empresa)
        serializer = ProyeccionCalculadaSerializer(proyecciones, many=True)
        return Response(serializer.data)

class EstadoInventarioView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        proyecciones = calcular_proyecciones_inventario(relacion.empresa)
        
        status_counts = {'Comprar Ahora': 0, 'Revisar Pronto': 0, 'Stock OK': 0, 'Sobrestock': 0}
        for item in proyecciones:
            if item['estado'] in status_counts:
                status_counts[item['estado']] += 1
        
        formatted_data = [{'estado': k, 'count': v} for k, v in status_counts.items()]
        return Response(formatted_data)


class ComprasPorProveedorView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        compras = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='compra', 
            proveedor__isnull=False
        ).values('proveedor__nombre').annotate(
            total_comprado=Sum('cantidad')
        ).order_by('-total_comprado')
        
        return Response(list(compras))

# ===============================================
# VISTAS DE PAGO Y UPGRADE (TRANSBANK)
# ===============================================

class IniciarPagoUpgradeView(APIView):
    """
    Vista EXCLUSIVA para usuarios que ya existen y quieren subir a PRO.
    Crea una transacción en Transbank con URL de retorno diferenciada.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("🟢 [DEBUG] Intentando iniciar pago...") 
        try:
            buy_order = f"upg_{get_random_string(12)}"
            session_id = str(request.user.id)
            amount = 15000
            return_url = 'http://localhost:8080/pago/confirmacion-upgrade'

            print(f"🟢 [DEBUG] Configurando orden: {buy_order}")

            # --- CORRECCIÓN AQUÍ: CONFIGURACIÓN EXPLÍCITA ---
            # Estas son las credenciales OFICIALES de prueba de Transbank
            options = WebpayOptions(
                commerce_code='597055555532', 
                api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C', 
                integration_type=IntegrationType.TEST
            )
            
            tx = Transaction(options) # <--- Ahora pasamos 'options'
            # ------------------------------------------------

            print("🟢 [DEBUG] Conectando con Transbank...")
            response = tx.create(buy_order, session_id, amount, return_url)
            
            print(f"🟢 [DEBUG] ¡Éxito! Token: {response['token']}")
            
            return Response({
                'url': response['url'],
                'token': response['token'],
                'amount': amount
            })
            
        except Exception as e:
            print("\n" + "🔴" * 20)
            print(f"ERROR CRÍTICO: {type(e).__name__}")
            print(f"DETALLE: {str(e)}")
            print("🔴" * 20 + "\n")
            return Response(
                {"error": "Error interno al conectar con el banco."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpgradePlanView(APIView):
    """
    Vista que recibe la confirmación (después de Transbank) y actualiza el plan a PRO en BD.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        relacion = user.relaciones.first()
        
        if relacion and relacion.empresa:
            empresa = relacion.empresa
            
            # Actualizamos el plan de la EMPRESA a PRO
            empresa.subscription_status = 'pro'
            empresa.save()
            
            return Response({"message": "Plan actualizado a PRO correctamente."}, status=status.HTTP_200_OK)
            
        return Response({"error": "No se pudo identificar la empresa."}, status=status.HTTP_400_BAD_REQUEST)

# ===============================================
# VISTAS DE DASHBOARD Y KPIS FINALES
# ===============================================

class LeadTimePorProveedorView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        lead_times = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='compra', 
            fecha_pedido__isnull=False, 
            fecha_recepcion__isnull=False
        ).annotate(
            lead_time=ExpressionWrapper(
                F('fecha_recepcion') - F('fecha_pedido'), 
                output_field=DurationField()
            )
        ).values('proveedor__nombre').annotate(
            avg_lead_time=Avg('lead_time')
        ).order_by('avg_lead_time')
        
        data = [
            {'proveedor__nombre': item['proveedor__nombre'] or 'Sin Proveedor', 'avg_lead_time_days': item['avg_lead_time'].days if item['avg_lead_time'] else 0} 
            for item in lead_times
        ]
        return Response(data)


class KpisGeneralesView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']

    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: 
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)

        empresa = relacion.empresa
        proyecciones = calcular_proyecciones_inventario(empresa)
        
        total_productos = len(proyecciones)
        productos_ok = len([p for p in proyecciones if p['estado'] == 'Stock OK'])
        eficiencia_stock = round((productos_ok / total_productos) * 100, 1) if total_productos > 0 else 0
        
        productos_criticos = len([p for p in proyecciones if p['estado'] == 'Comprar Ahora'])
        tasa_cumplimiento = round(((total_productos - productos_criticos) / total_productos) * 100, 1) if total_productos > 0 else 100.0

        data = {
            "tasa_cumplimiento": tasa_cumplimiento,
            "eficiencia_stock": eficiencia_stock
        }
        return Response(data)

class DashboardConsolidadoView(APIView):
    permission_classes = [HasRole]
    allowed_roles = ['manager', 'viewer']
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response({"error": "Usuario no asociado a una empresa."}, status=status.HTTP_400_BAD_REQUEST)
        
        empresa = relacion.empresa
        
        try:
            proyecciones = calcular_proyecciones_inventario(empresa)
            
            estado_counts = {'Comprar Ahora': 0, 'Revisar Pronto': 0, 'Stock OK': 0, 'Sobrestock': 0, 'Inactivo': 0}
            total_stock = 0
            
            for p in proyecciones:
                estado_counts[p['estado']] += 1
                total_stock += p['stock_actual']
            
            ventas_por_mes = Movimiento.objects.filter(
                producto__empresa=empresa, 
                tipo='venta'
            ).annotate(
                mes=TruncMonth('fecha_compra_producto')
            ).values('mes').annotate(
                total_vendido=Sum('cantidad')
            ).order_by('mes')
            
            ventas_mensuales = [
                {"time": item['mes'].strftime('%Y-%m-%d'), "value": item['total_vendido']} 
                for item in ventas_por_mes
            ]
            total_ventas = sum(item['value'] for item in ventas_mensuales)
            
            lead_times_query = Movimiento.objects.filter(
                producto__empresa=empresa, 
                tipo='compra', 
                fecha_pedido__isnull=False, 
                fecha_recepcion__isnull=False
            ).annotate(
                lead_time=ExpressionWrapper(
                    F('fecha_recepcion') - F('fecha_pedido'), 
                    output_field=DurationField()
                )
            ).values('proveedor__nombre').annotate(
                avg_lead_time=Avg('lead_time')
            ).order_by('avg_lead_time')
            
            lead_times = [
                {'proveedor__nombre': item['proveedor__nombre'] or 'Sin Proveedor', 'avg_lead_time_days': item['avg_lead_time'].days if item['avg_lead_time'] else 0} 
                for item in lead_times_query
            ]
            
            total_productos = len(proyecciones)
            productos_criticos = estado_counts.get('Comprar Ahora', 0)
            tasa_cumplimiento = round(((total_productos - productos_criticos) / total_productos) * 100, 1) if total_productos > 0 else 100.0
            
            productos_ok = estado_counts.get('Stock OK', 0)
            eficiencia_stock = round((productos_ok / total_productos) * 100, 1) if total_productos > 0 else 0
            
            unidades_sobrestock = sum(
                p['stock_actual'] for p in proyecciones 
                if p['estado'] == 'Sobrestock'
            )
            
            coberturas_validas = [
                p['semanas_cobertura'] for p in proyecciones 
                if p['semanas_cobertura'] is not None
            ]
            dias_cobertura_promedio = 0
            if coberturas_validas:
                coberturas_limitadas = [min(c, 52) for c in coberturas_validas]
                promedio_semanas = sum(coberturas_limitadas) / len(coberturas_limitadas)
                dias_cobertura_promedio = int(promedio_semanas * 7)
            
            kpis = {
                "tasa_cumplimiento": tasa_cumplimiento,
                "eficiencia_stock": eficiencia_stock,
                "dias_cobertura_promedio": dias_cobertura_promedio,
                "unidades_sobrestock": unidades_sobrestock,
                "total_ventas_unidades": total_ventas,
                "unidades_totales_stock": total_stock,
                "productos_criticos": productos_criticos
            }
            
            # ==========================================
            # 📅 DÍAS IMPORTANTES PRÓXIMOS (45 días)
            # ==========================================
            hoy = timezone.now().date()
            fecha_limite_eventos = hoy + timedelta(days=30)
            
            dias_importantes = DiaImportante.objects.filter(
                empresa=empresa,
                fecha__gte=hoy,
                fecha__lte=fecha_limite_eventos
            ).order_by('fecha').values('nombre_evento', 'fecha', 'descripcion')
            
            dias_importantes_lista = [
                {
                    'nombre': d['nombre_evento'],
                    'fecha': d['fecha'].strftime('%Y-%m-%d'),
                    'dias_restantes': (d['fecha'] - hoy).days,
                    'descripcion': d['descripcion'] or ''
                }
                for d in dias_importantes
            ]
            
            return Response({
                "proyecciones": proyecciones,
                "ventas_mensuales": ventas_mensuales,
                "lead_times": lead_times,
                "estado_inventario": [
                    {"estado": k, "count": v} 
                    for k, v in estado_counts.items()
                ],
                "kpis": kpis,
                "configuracion": EmpresaConfiguracionSerializer(empresa).data,
                "dias_importantes": dias_importantes_lista
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error en DashboardConsolidadoView: {str(e)}", exc_info=True)
            return Response(
                {"error": "Error al cargar los datos del dashboard."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )