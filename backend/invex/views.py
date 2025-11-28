# invex/views.py (VERSIÓN CORREGIDA FINAL)

import os
import re
from unidecode import unidecode
import logging
from datetime import timedelta
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField, Count, Case, When, Value, CharField, FloatField, Q, Min
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404

from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
# 👇 --- IMPORTS PARA RESETEO ---
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
# ---------------------------
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import HasRole
from .models import (
    Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion,
    DiaImportante, Categoria, Proveedor, Movimiento
)
from .serializers import (
    UsuarioSerializer, EmpresaSerializer, ProductoSerializer,
    SuscripcionSerializer, DiaImportanteSerializer, FullRegistrationSerializer,
    UserManagementSerializer, 
    MasterImportSerializer,
    ProyeccionCalculadaSerializer,
    EmpresaConfiguracionSerializer 
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
    UMBRAL_SOBRESTOCK_SEMANAS = 12  # Más de 12 semanas = sobrestock
    UMBRAL_DEMANDA_MINIMA = 0.5  # Si vende menos de 0.5 u/semana, considerar "sin demanda"

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
            return Response(
                {"detail": "Email, contraseña y empresa son requeridos."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = Usuario.objects.get(email=email)
            if not user.check_password(password):
                raise Usuario.DoesNotExist
            relacion = user.relaciones.get(empresa__nombre=empresa_nombre)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'rol': relacion.rol, 'empresa_id': relacion.empresa.id})
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
            empresa_id = relacion.empresa.id
        except UsuarioEmpresa.DoesNotExist:
            return Response(
                {"detail": f"El usuario no tiene acceso a la empresa '{empresa_nombre}'."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response(
                {"error": "El usuario no está asociado a ninguna empresa."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmpresaSerializer(relacion.empresa)
        return Response(serializer.data)



class EmpresaConfiguracionView(APIView):
    """
    Vista para obtener y actualizar la configuración de inventario de la empresa.
    
    GET: Obtiene la configuración actual
    PATCH: Actualiza la configuración
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener configuración actual de la empresa"""
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response(
                {"error": "El usuario no está asociado a ninguna empresa."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = EmpresaConfiguracionSerializer(relacion.empresa)
        return Response(serializer.data)
    
    def patch(self, request):
        """Actualizar configuración de la empresa"""
        relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
        if not relacion:
            return Response(
                {"error": "El usuario no está asociado a ninguna empresa."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validar que el usuario tenga permisos de admin
        if relacion.rol not in ['admin', 'manager']:
            return Response(
                {"error": "No tienes permisos para modificar la configuración."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = EmpresaConfiguracionSerializer(
            relacion.empresa, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Configuración actualizada exitosamente.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        relacion_admin = self.request.user.relaciones.first()
        if not relacion_admin:
            return UsuarioEmpresa.objects.none()
        return UsuarioEmpresa.objects.filter(
            empresa=relacion_admin.empresa
        ).select_related('usuario')
    
    def perform_create(self, serializer):
        pass


# ===============================================
# VISTA DE IMPORTACIÓN MASIVA
# ===============================================

class InventarioImportAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
        
        serializer = MasterImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        data_productos = validated_data.get('productos', [])
        data_historial_ventas = validated_data.get('historial_ventas', [])
        data_historial_compras = validated_data.get('historial_compras', [])

        try:
            with transaction.atomic():
                productos_cache = {}
                categorias_cache = {}
                proveedores_cache = {}

                # PASO 1: Procesar PRODUCTOS
                for item_prod in data_productos:
                    prod_nombre = item_prod.get('nombre')
                    if not prod_nombre:
                        continue

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

                    if not nombre_prod or not cantidad_str or not fecha:
                        logger.warning(f"[Importación] Fila de Venta Omitida: {item_venta}")
                        continue
                    
                    producto_obj = productos_cache.get(str(nombre_prod).lower())
                    if not producto_obj:
                        logger.warning(f"[Importación] Producto '{nombre_prod}' no encontrado. Omitiendo.")
                        continue
                    
                    try:
                        cantidad_num = int(float(cantidad_str))
                    except (ValueError, TypeError):
                        logger.warning(f"[Importación] Cantidad inválida '{cantidad_str}'. Omitiendo.")
                        continue

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
                    
                    # --- NUEVO: Buscar fecha de vencimiento ---
                    fecha_venc = self._find_key_value(item_compra, ['fecha_vencimiento', 'vencimiento', 'caducidad', 'f_venc'])
                    # ------------------------------------------
                    
                    if not nombre_prod or not cantidad_str:
                        continue # Omitir si faltan datos clave
                    
                    producto_obj = productos_cache.get(str(nombre_prod).lower())
                    if not producto_obj: 
                        continue

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
                    except (ValueError, TypeError): 
                        continue

                    movimientos_compras_a_crear.append(
                        Movimiento(
                            producto=producto_obj,
                            tipo='compra',
                            cantidad=cantidad_num,
                            fecha_pedido=fecha_ped,
                            fecha_recepcion=fecha_rec,
                            
                            # --- NUEVO: Asignar fecha de vencimiento ---
                            fecha_vencimiento=fecha_venc, 
                            # ------------------------------------------

                            fecha_compra_producto=fecha_rec or fecha_ped or timezone.now().date(),
                            proveedor=proveedor_obj
                        )
                    )

                # PASO 4: Creación Masiva
                Movimiento.objects.bulk_create(movimientos_ventas_a_crear)
                Movimiento.objects.bulk_create(movimientos_compras_a_crear)

        except Exception as e:
            logger.error(f"[Importación] Error: {str(e)}", exc_info=True)
            return Response(
                {"error": f"Error durante la importación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"mensaje": f"Importación exitosa. {len(data_productos)} productos, {len(movimientos_ventas_a_crear)} ventas, {len(movimientos_compras_a_crear)} compras."},
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
        relacion = self.request.user.relaciones.first()
        if not relacion:
            raise serializers.ValidationError("No tienes una empresa asignada.")
        serializer.save(empresa=relacion.empresa)


# ===============================================
# 🆕 FUNCIÓN HELPER PARA CALCULAR PROYECCIONES
# ===============================================
# invex/views.py

def calcular_proyecciones_inventario(empresa, dias_analisis=None):
    """
    Función centralizada para calcular proyecciones de inventario.
    🔥 AHORA CON TECHO DINÁMICO POR VENCIMIENTO Y CONFIGURACIÓN DE BASE DE DATOS
    """
    
    # 1. Configuración Global (AHORA DINÁMICA DESDE LA BD)
    config_semanas_seguridad = empresa.semanas_seguridad
    config_semanas_objetivo = empresa.semanas_objetivo
    config_dias_analisis = dias_analisis if dias_analisis is not None else empresa.dias_analisis_demanda
    
    # 🔥 USAMOS LOS VALORES DE LA BD (Si son nulos, usamos defaults seguros)
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
    
    # 2. Demanda (Ventas)
    ventas_recientes = Movimiento.objects.filter(
        producto__empresa=empresa, 
        tipo='venta', 
        fecha_compra_producto__gte=fecha_limite
    ).values('producto_id').annotate(total_vendido=Sum('cantidad'))
    
    demanda_map = {item['producto_id']: item['total_vendido'] for item in ventas_recientes}
    
    # 3. Lead Time (Sanitizado con MAX_LEAD_TIME_RAZONABLE)
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
        # Filtro de calidad de datos
        if 0 <= dias <= MAX_LEAD_TIME_RAZONABLE:
            if pid not in tiempos_por_producto: tiempos_por_producto[pid] = []
            tiempos_por_producto[pid].append(dias)

    for pid, tiempos in tiempos_por_producto.items():
        if tiempos: lead_time_map[pid] = int(sum(tiempos) / len(tiempos))
        else: lead_time_map[pid] = LEAD_TIME_DEFECTO

    # 🔥 4. Mapa de Vencimientos Próximos (FEFO)
    # Obtenemos la fecha de vencimiento futura más cercana para cada producto
    # Requiere: from django.db.models import Min
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
        
        # Calcular Demanda Semanal
        if total_vendido > 0:
            demanda_semanal = (total_vendido / config_dias_analisis) * 7
        else:
            demanda_semanal = 0
        demanda_semanal = round(demanda_semanal, 2)
        
        # Lead Time
        lead_time_dias = lead_time_map.get(stock.producto.id, LEAD_TIME_DEFECTO)
        lead_time_semanas = round(lead_time_dias / 7, 1)
        
        # Inicializar
        semanas_cobertura = None
        estado = "Stock OK"
        cantidad_sugerida = 0
        punto_reorden = 0
        dias_para_comprar = None
        
        # Lógica de Umbrales
        if demanda_semanal < UMBRAL_DEMANDA_MINIMA:
            semanas_cobertura = None
            # Si vende muy poco, solo es Sobrestock si tiene mucho acumulado
            estado = "Stock OK" if stock.stock_actual < 10 else "Sobrestock"
            
        else:
            # Calcular cobertura
            semanas_cobertura = round(stock.stock_actual / demanda_semanal, 1)
            
            # --- 🔥 LÓGICA DEL TECHO DINÁMICO (VENCIMIENTO) ---
            
            # 1. Objetivo Global Base
            semanas_objetivo_final = config_semanas_objetivo
            
            # 2. Ajuste por Vencimiento
            fecha_venc = vencimientos_map.get(stock.producto.id)
            
            if fecha_venc:
                dias_vida_util = (fecha_venc - hoy).days
                semanas_vida_util = dias_vida_util / 7
                
                # Techo seguro = Vida útil - Buffer de seguridad (configurable)
                techo_seguro = max(0, semanas_vida_util - BUFFER_VENTA_SEMANAS)
                
                # Si el techo es menor que el objetivo global, bajamos el objetivo
                if techo_seguro < semanas_objetivo_final:
                    semanas_objetivo_final = techo_seguro

            # ------------------------------------

            # Calcular Punto de Reorden
            stock_durante_lead_time = demanda_semanal * lead_time_semanas
            stock_seguridad = demanda_semanal * config_semanas_seguridad
            punto_reorden = int(stock_durante_lead_time + stock_seguridad)
            
            # Evaluación de Estado
            if stock.stock_actual <= punto_reorden:
                estado = "Comprar Ahora"
                dias_para_comprar = 0
                
                # Calcular compra usando el OBJETIVO AJUSTADO (dinámico)
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
#
# ===============================================
# VISTAS DE ANALÍTICAS (CORREGIDAS)
# ===============================================

class VentasHistoricasView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ventas_por_dia = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).values('fecha_compra_producto').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('fecha_compra_producto')
        
        formatted_data = [
            {
                "time": item['fecha_compra_producto'].strftime('%Y-%m-%d'), 
                "value": item['total_vendido']
            } 
            for item in ventas_por_dia
        ]
        return Response(formatted_data)


class VentasMensualesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ventas_por_mes = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).annotate(
            mes=TruncMonth('fecha_compra_producto')
        ).values('mes').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('mes')
        
        formatted_data = [
            {
                "time": item['mes'].strftime('%Y-%m-%d'), 
                "value": item['total_vendido']
            } 
            for item in ventas_por_mes
        ]
        return Response(formatted_data)


class TopProductosVendidosView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        top_productos = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='venta'
        ).values('producto__nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:5]
        
        return Response(list(top_productos))


class ProductoProyeccionesView(APIView):
    """
    🆕 VERSIÓN CORREGIDA: Usa la función helper centralizada
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proyecciones = calcular_proyecciones_inventario(relacion.empresa)
        serializer = ProyeccionCalculadaSerializer(proyecciones, many=True)
        return Response(serializer.data)


class EstadoInventarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proyecciones = calcular_proyecciones_inventario(relacion.empresa)
        
        status_counts = {
            'Comprar Ahora': 0, 
            'Revisar Pronto': 0, 
            'Stock OK': 0,
            'Sobrestock': 0
        }
        
        for item in proyecciones:
            if item['estado'] in status_counts:
                status_counts[item['estado']] += 1
        
        formatted_data = [
            {'estado': k, 'count': v} 
            for k, v in status_counts.items()
        ]
        return Response(formatted_data)


class ComprasPorProveedorView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compras = Movimiento.objects.filter(
            producto__empresa=relacion.empresa, 
            tipo='compra', 
            proveedor__isnull=False
        ).values('proveedor__nombre').annotate(
            total_comprado=Sum('cantidad')
        ).order_by('-total_comprado')
        
        return Response(list(compras))


class LeadTimePorProveedorView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
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
            {
                'proveedor__nombre': item['proveedor__nombre'] or 'Sin Proveedor', 
                'avg_lead_time_days': item['avg_lead_time'].days if item['avg_lead_time'] else 0
            } 
            for item in lead_times
        ]
        return Response(data)


class KpisGeneralesView(APIView):
    """
    🆕 VERSIÓN CORREGIDA: Calcula la tasa de cumplimiento REAL
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion: 
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        empresa = relacion.empresa
        proyecciones = calcular_proyecciones_inventario(empresa)
        
        # Calcular Eficiencia de Stock
        total_productos = len(proyecciones)
        productos_ok = len([p for p in proyecciones if p['estado'] == 'Stock OK'])
        eficiencia_stock = round((productos_ok / total_productos) * 100, 1) if total_productos > 0 else 0
        
        # 🔥 CALCULAR TASA DE CUMPLIMIENTO REAL
        # Tasa de cumplimiento = % de productos que NO están en "Comprar Ahora"
        productos_criticos = len([p for p in proyecciones if p['estado'] == 'Comprar Ahora'])
        tasa_cumplimiento = round(((total_productos - productos_criticos) / total_productos) * 100, 1) if total_productos > 0 else 100.0

        data = {
            "tasa_cumplimiento": tasa_cumplimiento,
            "eficiencia_stock": eficiencia_stock
        }
        return Response(data)


# ===============================================
# 🆕 ENDPOINT CONSOLIDADO PARA DASHBOARD (CORREGIDO)
# ===============================================

class DashboardConsolidadoView(APIView):
    """
    Endpoint optimizado que devuelve todos los datos del dashboard en una sola llamada.
    🆕 VERSIÓN CORREGIDA con cálculos precisos de cobertura y tasa de cumplimiento real.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        relacion = request.user.relaciones.first()
        if not relacion:
            return Response(
                {"error": "Usuario no asociado a una empresa."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        empresa = relacion.empresa
        
        try:
            # 1. PROYECCIONES DE PRODUCTOS (usa función helper corregida)
            proyecciones = calcular_proyecciones_inventario(empresa)
            
            # Contar estados
            estado_counts = {'Comprar Ahora': 0, 'Revisar Pronto': 0, 'Stock OK': 0, 'Sobrestock': 0}
            total_stock = 0
            
            for p in proyecciones:
                estado_counts[p['estado']] += 1
                total_stock += p['stock_actual']
            
            # 2. VENTAS MENSUALES
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
            
            # 3. LEAD TIME POR PROVEEDOR
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
                {
                    'proveedor__nombre': item['proveedor__nombre'] or 'Sin Proveedor', 
                    'avg_lead_time_days': item['avg_lead_time'].days if item['avg_lead_time'] else 0
                } 
                for item in lead_times_query
            ]
            
            # 4. KPIs GENERALES (CORREGIDOS)
            total_productos = len(proyecciones)
            productos_criticos = estado_counts.get('Comprar Ahora', 0)
            
            # 🔥 TASA DE CUMPLIMIENTO REAL
            tasa_cumplimiento = round(((total_productos - productos_criticos) / total_productos) * 100, 1) if total_productos > 0 else 100.0
            
            # Eficiencia de stock
            productos_ok = estado_counts.get('Stock OK', 0)
            eficiencia_stock = round((productos_ok / total_productos) * 100, 1) if total_productos > 0 else 0
            
            # Unidades en sobrestock
            unidades_sobrestock = sum(
                p['stock_actual'] for p in proyecciones 
                if p['estado'] == 'Sobrestock'
            )
            
            # 🔥 DÍAS PROMEDIO DE COBERTURA (CORREGIDO)
            # Solo consideramos productos CON demanda significativa
            coberturas_validas = [
                p['semanas_cobertura'] for p in proyecciones 
                if p['semanas_cobertura'] is not None
            ]
            
            dias_cobertura_promedio = 0
            if coberturas_validas:
                # Limitar coberturas a un máximo razonable (ej: 52 semanas = 1 año)
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
            
            # 5. RESPUESTA CONSOLIDADA
            return Response({
                "proyecciones": proyecciones,
                "ventas_mensuales": ventas_mensuales,
                "lead_times": lead_times,
                "estado_inventario": [
                    {"estado": k, "count": v} 
                    for k, v in estado_counts.items()
                ],
                "kpis": kpis
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error en DashboardConsolidadoView: {str(e)}", exc_info=True)
            return Response(
                {"error": "Error al cargar los datos del dashboard."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
