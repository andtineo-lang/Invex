# invex/serializers.py (VERSIÓN FINAL CON HERENCIA DE PLAN)

from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from datetime import timedelta  
from .models import (
    Usuario, 
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

# ====================================================================
# SERIALIZER PARA GESTIÓN DE USUARIOS 
# ====================================================================

class UserManagementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='usuario.nombre', read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
    nombre_completo = serializers.CharField(write_only=True)

    class Meta:
        model = UsuarioEmpresa
        fields = ['id', 'name', 'email', 'rol', 'nombre_completo']
        read_only_fields = ['id', 'name', 'email']

    def create(self, validated_data):
        validated_data.pop('nombre_completo', None)
        instancia, creada = UsuarioEmpresa.objects.get_or_create(
            usuario=validated_data.get('usuario'),
            empresa=validated_data.get('empresa'),
            defaults={'rol': validated_data.get('rol')}
        )
        if not creada and instancia.rol != validated_data.get('rol'):
            instancia.rol = validated_data.get('rol')
            instancia.save()
        return instancia


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Tu contraseña antigua no es correcta.")
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(password=value, user=self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas nuevas no coinciden."})
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError({"new_password": "La nueva contraseña no puede ser igual a la antigua."})
        return data

# ====================================================================
# SERIALIZERS DE FLUJO Y DE IMPORTACIÓN
# ====================================================================

class RegistroSerializer(serializers.Serializer):
    empresa_nombre = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    subscription_status = serializers.CharField(required=False, default='free') 

    def create(self, validated_data):
        empresa_nombre = validated_data['empresa_nombre']
        email = validated_data['email']
        password = validated_data['password']
        sub_status = validated_data.get('subscription_status', 'free')

        usuario, created_u = Usuario.objects.get_or_create(email=email)
        if created_u:
            usuario.set_password(password)
            usuario.save()
        
        empresa, created_e = Empresa.objects.get_or_create(nombre=empresa_nombre)
        
        if empresa.owner is None:
            empresa.owner = usuario
            empresa.subscription_status = sub_status  # ← Asignar plan a la EMPRESA
            empresa.save()
            rol = 'admin'
        else:
            rol = 'viewer'
            
        UsuarioEmpresa.objects.get_or_create(usuario=usuario, empresa=empresa, defaults={'rol': rol})
        return {"usuario": usuario, "empresa": empresa, "rol": rol}


class FullRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    company = serializers.CharField(max_length=255)
    rut = serializers.CharField(max_length=20)
    industry = serializers.CharField(max_length=255)
    plan = serializers.CharField(max_length=50)

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo electrónico.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['name']
        )
        # Ya NO asignamos plan al usuario

        # Determinar el plan
        sub_status = 'pro' if 'free' not in validated_data['plan'].lower() else 'free'

        empresa = Empresa.objects.create(
            nombre=validated_data['company'],
            rut=validated_data['rut'],
            rubro=validated_data['industry'],
            owner=user,
            subscription_status=sub_status  # ← Asignar plan a la EMPRESA
        )
        UsuarioEmpresa.objects.create(usuario=user, empresa=empresa, rol='admin')
        
        plan_map = {'Plan Trimestral': '3m', 'Plan Semestral': '6m', 'Plan Anual': '1y'}
        plan_tipo = plan_map.get(validated_data['plan'], 'free') 
        
        if plan_tipo != 'free':
            fecha_inicio = timezone.now().date()
            if plan_tipo == '3m':
                fecha_fin = fecha_inicio + relativedelta(months=+3)
            elif plan_tipo == '6m':
                fecha_fin = fecha_inicio + relativedelta(months=+6)
            else:
                fecha_fin = fecha_inicio + relativedelta(years=+1)
                
            Suscripcion.objects.create(
                empresa=empresa,
                tipo=plan_tipo,
                fecha_fin=fecha_fin,
                pago_por=user
            )
        return user


# ---------------------------
# SERIALIZADOR DE IMPORTACIÓN MASIVA
# ---------------------------

class ProductoImportSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=255)
    stock_actual = serializers.IntegerField(required=False, default=0, allow_null=True)
    categoria = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    unidad_medida = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    cantidad_comprada = serializers.IntegerField(required=False, default=None, allow_null=True)
    cantidad_vendida = serializers.IntegerField(required=False, default=None, allow_null=True)
    proveedor = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    fecha_pedido = serializers.DateField(required=False, allow_null=True)
    fecha_recepcion = serializers.DateField(required=False, allow_null=True)
    fecha_vencimiento = serializers.DateField(required=False, allow_null=True)

class MasterImportSerializer(serializers.Serializer):
    productos = ProductoImportSerializer(many=True)
    historial_ventas = serializers.ListField(child=serializers.DictField(), required=False)
    historial_compras = serializers.ListField(child=serializers.DictField(), required=False)


# ---------------------------
# SERIALIZERS DE MODELOS (PARA CRUD)
# ---------------------------

class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()
    empresa_id = serializers.SerializerMethodField()
    empresa_nombre = serializers.SerializerMethodField()
    # 🔥 CAMBIO CLAVE: Método para heredar plan del dueño
    subscription_status = serializers.SerializerMethodField() 

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'rol', 'empresa_id', 'mostrar_tutorial', 'subscription_status', 'empresa_nombre']

    def get_rol(self, obj):
        relacion = obj.relaciones.first()
        return relacion.rol if relacion else 'viewer'

    def get_empresa_id(self, obj):
        relacion = obj.relaciones.first()
        return relacion.empresa.id if relacion else None

    def get_empresa_nombre(self, obj):
        relacion = obj.relaciones.first()
        return relacion.empresa.nombre if relacion else ""

    # 🔥 LA LÓGICA DE HERENCIA
    def get_subscription_status(self, obj):
        relacion = obj.relaciones.first()
        if not relacion:
            return 'free'
        # Ahora viene directo de la empresa
        return relacion.empresa.subscription_status


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'rut', 'rubro', 'owner', 'fecha_creacion']


class UsuarioEmpresaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    class Meta:
        model = UsuarioEmpresa
        fields = ['usuario', 'empresa', 'rol']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class StockWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_actual', 'stock_transito', 'ventas_proyectadas', 'demanda_estacional']


class ProductoSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    inTransit = serializers.SerializerMethodField()
    projectedSales = serializers.SerializerMethodField() 
    seasonal = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    proyeccion_status = serializers.SerializerMethodField()
    proyeccion_cantidad = serializers.SerializerMethodField()
    stock_data = StockWriteSerializer(write_only=True)
    
    # 🔥 CAMBIO 1: Habilitar escritura para este campo
    # Antes era SerializerMethodField (solo lectura), ahora es DateField (lectura y escritura)
    fecha_vencimiento = serializers.DateField(write_only=True, required=False, allow_null=True)
    
    demanda_calculada = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'sku', 'categoria',
            'stock', 'inTransit', 'projectedSales', 'seasonal', 'categoria_nombre',
            'stock_data',
            'proyeccion_status', 'proyeccion_cantidad',
            'fecha_vencimiento',
            'demanda_calculada'
        ]

    def get_first_stock(self, obj):
        return obj.stocks.first()

    def get_stock(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.stock_actual if stock_obj else 0
    
    def get_inTransit(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.stock_transito if stock_obj else 0
    
    def get_projectedSales(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.ventas_proyectadas if stock_obj else 0
    
    def get_demanda_calculada(self, obj):
        dias_analisis = obj.empresa.dias_analisis_demanda
        fecha_limite = timezone.now().date() - timedelta(days=dias_analisis)
        total_vendido = obj.movimientos.filter(tipo='venta', fecha_compra_producto__gte=fecha_limite).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        if total_vendido > 0:
            promedio_semanal = (total_vendido / dias_analisis) * 7
            return round(promedio_semanal, 1)
        return 0

    def get_seasonal(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.demanda_estacional if stock_obj else "Normal"
    
    def get_proyeccion_status(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_status if stock_obj else "N/A"
    
    def get_proyeccion_cantidad(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_cantidad_a_comprar if stock_obj else 0

    # Método para representar la fecha de vencimiento al leer datos (GET)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        stock_obj = self.get_first_stock(instance)
        fecha_mostrada = None
        
        if stock_obj and stock_obj.stock_actual > 0:
            # 1. Buscamos el vencimiento más próximo en el futuro
            proximo = instance.movimientos.filter(
                tipo__in=['compra', 'ajuste'], 
                fecha_vencimiento__isnull=False, 
                fecha_vencimiento__gte=timezone.now().date()
            ).order_by('fecha_vencimiento').first()
            
            if proximo:
                fecha_mostrada = proximo.fecha_vencimiento
            else:
                # 2. Si no hay futuros, mostramos el último registrado (aunque esté vencido)
                ultimo = instance.movimientos.filter(
                    tipo__in=['compra', 'ajuste'], 
                    fecha_vencimiento__isnull=False
                ).order_by('-fecha_vencimiento').first()
                if ultimo:
                    fecha_mostrada = ultimo.fecha_vencimiento

        representation['fecha_vencimiento'] = fecha_mostrada
        return representation

    def create(self, validated_data):
        # 1. Sacamos los datos especiales
        stock_data = validated_data.pop('stock_data')
        fecha_vencimiento = validated_data.pop('fecha_vencimiento', None) # <--- Aquí capturamos la fecha

        # 2. Limpieza de seguridad
        if 'empresa' in validated_data:
            validated_data.pop('empresa')

        # 3. Validaciones de usuario
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Contexto de request no encontrado.")
        
        relacion = request.user.relaciones.first()
        if not relacion:
            raise serializers.ValidationError("El usuario no está asociado a ninguna empresa.")
            
        # 4. Creamos Producto y Stock
        producto = Producto.objects.create(empresa=relacion.empresa, **validated_data)
        Stock.objects.create(producto=producto, **stock_data)
        
        # 5. CREAMOS EL MOVIMIENTO (Aquí es donde se guarda la fecha realmente)
        cantidad_inicial = stock_data.get('stock_actual', 0)
        
        if cantidad_inicial > 0:
            Movimiento.objects.create(
                producto=producto,
                tipo='ajuste',
                cantidad=cantidad_inicial,
                fecha_vencimiento=fecha_vencimiento, # <--- Guardamos la fecha en el movimiento
                fecha_compra_producto=timezone.now().date(),
                notas="Stock inicial al crear producto"
            )
        
        return producto

    def update(self, instance, validated_data):
        # 1. Capturamos la fecha si viene en la edición
        fecha_vencimiento = validated_data.pop('fecha_vencimiento', None)

        if 'stock_data' in validated_data:
            stock_data = validated_data.pop('stock_data')
            stock_instance = instance.stocks.first()
            
            if stock_instance:
                # Calculamos si el stock cambió
                stock_anterior = stock_instance.stock_actual
                stock_nuevo = stock_data.get('stock_actual', stock_anterior)
                diferencia = stock_nuevo - stock_anterior
                
                # Guardamos el stock
                stock_serializer = StockWriteSerializer(stock_instance, data=stock_data, partial=True)
                stock_serializer.is_valid(raise_exception=True)
                stock_serializer.save()

                # 2. Si cambió el stock O se mandó una fecha, creamos el movimiento
                if diferencia != 0 or fecha_vencimiento:
                     Movimiento.objects.create(
                        producto=instance,
                        tipo='ajuste',
                        cantidad=diferencia if diferencia > 0 else 0, # Registramos la diferencia positiva
                        fecha_vencimiento=fecha_vencimiento, # <--- Guardamos la fecha nueva
                        fecha_compra_producto=timezone.now().date(),
                        notas="Ajuste desde edición de producto"
                    )

        return super().update(instance, validated_data)


class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


class DiaImportanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaImportante
        fields = ['id', 'nombre_evento', 'fecha', 'descripcion']


class ProyeccionCalculadaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    producto_id = serializers.IntegerField(required=False)
    producto_nombre = serializers.CharField()
    stock_actual = serializers.IntegerField()
    demanda_semanal_proyectada = serializers.FloatField()
    semanas_cobertura = serializers.FloatField(allow_null=True)
    estado = serializers.CharField()
    cantidad_sugerida = serializers.IntegerField()
    lead_time_dias = serializers.IntegerField() 
    lead_time_semanas = serializers.FloatField()
    punto_reorden = serializers.IntegerField() 
    dias_para_comprar = serializers.IntegerField(allow_null=True) 


class EmpresaConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'semanas_seguridad', 'semanas_objetivo', 'dias_analisis_demanda',
            'max_lead_time_razonable', 'lead_time_defecto', 'buffer_venta_semanas',
            'umbral_demanda_minima', 'umbral_sobrestock_semanas'
        ]
        read_only_fields = ['id', 'nombre']
    
    def validate_semanas_seguridad(self, value):
        if value < 1: raise serializers.ValidationError("Las semanas de seguridad deben ser al menos 1.")
        if value > 12: raise serializers.ValidationError("Las semanas de seguridad no pueden exceder 12 semanas.")
        return value
    
    def validate_semanas_objetivo(self, value):
        if value < 1: raise serializers.ValidationError("Las semanas objetivo deben ser al menos 1.")
        if value > 52: raise serializers.ValidationError("Las semanas objetivo no pueden exceder 52 semanas.")
        return value
    
    def validate_umbral_sobrestock_semanas(self, value):
        if value < 4: raise serializers.ValidationError("El umbral de sobrestock debe ser de al menos 4 semanas.")
        return value

    def validate(self, data):
        semanas_seguridad = data.get('semanas_seguridad', self.instance.semanas_seguridad if self.instance else 2)
        semanas_objetivo = data.get('semanas_objetivo', self.instance.semanas_objetivo if self.instance else 4)
        if semanas_objetivo < semanas_seguridad:
            raise serializers.ValidationError({'semanas_objetivo': 'Las semanas objetivo deben ser mayores o iguales a las semanas de seguridad.'})
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField(min_length=8)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            self.user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError({"token": "Enlace inválido o usuario no encontrado."})
        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError({"token": "El enlace ha expirado o es inválido."})
        return data