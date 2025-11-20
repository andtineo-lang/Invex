# invex/serializers.py (VERSIÓN FINAL CORREGIDA)

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
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

# ====================================================================
# SERIALIZERS DE FLUJO Y DE IMPORTACIÓN
# ====================================================================

class RegistroSerializer(serializers.Serializer):
    empresa_nombre = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        empresa_nombre = validated_data['empresa_nombre']
        email = validated_data['email']
        password = validated_data['password']
        usuario, created_u = Usuario.objects.get_or_create(email=email)
        if created_u:
            usuario.set_password(password)
            usuario.save()
        empresa, created_e = Empresa.objects.get_or_create(nombre=empresa_nombre)
        if empresa.owner is None:
            empresa.owner = usuario
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
        empresa = Empresa.objects.create(
            nombre=validated_data['company'],
            rut=validated_data['rut'],
            rubro=validated_data['industry'],
            owner=user
        )
        UsuarioEmpresa.objects.create(usuario=user, empresa=empresa, rol='admin')
        
        plan_map = {'Plan Trimestral': '3m', 'Plan Semestral': '6m', 'Plan Anual': '1y'}
        plan_tipo = plan_map.get(validated_data['plan'])
        if not plan_tipo:
            raise serializers.ValidationError("Tipo de plan no válido.")
        
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


class MasterImportSerializer(serializers.Serializer):
    productos = ProductoImportSerializer(many=True)
    historial_ventas = serializers.ListField(child=serializers.DictField(), required=False)
    historial_compras = serializers.ListField(child=serializers.DictField(), required=False)


# ---------------------------
# SERIALIZERS DE MODELOS (PARA CRUD)
# ---------------------------

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'mostrar_tutorial'] 


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

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'sku', 'categoria',
            'stock', 'inTransit', 'projectedSales', 'seasonal', 'categoria_nombre',
            'stock_data',
            'proyeccion_status', 'proyeccion_cantidad'
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
    
    def get_seasonal(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.demanda_estacional if stock_obj else "Normal"
    
    def get_proyeccion_status(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_status if stock_obj else "N/A"
    
    def get_proyeccion_cantidad(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_cantidad_a_comprar if stock_obj else 0

    def create(self, validated_data):
        stock_data = validated_data.pop('stock_data')
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Contexto de request no encontrado.")
        relacion = request.user.relaciones.first()
        if not relacion:
            raise serializers.ValidationError("El usuario no está asociado a ninguna empresa.")
        producto = Producto.objects.create(empresa=relacion.empresa, **validated_data)
        Stock.objects.create(producto=producto, **stock_data)
        return producto

    def update(self, instance, validated_data):
        if 'stock_data' in validated_data:
            stock_data = validated_data.pop('stock_data')
            stock_instance = instance.stocks.first()
            if stock_instance:
                stock_serializer = StockWriteSerializer(stock_instance, data=stock_data, partial=True)
                stock_serializer.is_valid(raise_exception=True)
                stock_serializer.save()
        return super().update(instance, validated_data)


class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


class DiaImportanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaImportante
        fields = ['id', 'nombre_evento', 'fecha', 'descripcion']


# ====================================================================
# 🆕 SERIALIZER PARA PROYECCIONES CALCULADAS (CORREGIDO)
# ====================================================================

class ProyeccionCalculadaSerializer(serializers.Serializer):
    """
    Serializer para datos de proyección calculados dinámicamente.
    🆕 AÑADIDO: Campos para predicción inteligente de compras basada en lead time.
    """
    id = serializers.IntegerField()
    producto_id = serializers.IntegerField(required=False)
    producto_nombre = serializers.CharField()
    stock_actual = serializers.IntegerField()
    demanda_semanal_proyectada = serializers.FloatField()
    semanas_cobertura = serializers.FloatField(allow_null=True)
    estado = serializers.CharField()
    cantidad_sugerida = serializers.IntegerField()
    # 🆕 NUEVOS CAMPOS PARA PREDICCIÓN DE COMPRAS
    lead_time_dias = serializers.IntegerField()  # Tiempo de entrega del proveedor (días)
    lead_time_semanas = serializers.FloatField()  # Tiempo de entrega (semanas)
    punto_reorden = serializers.IntegerField()  # Stock mínimo antes de comprar
    dias_para_comprar = serializers.IntegerField(allow_null=True)  # En cuántos días debes comprar (null = no aplica)



class EmpresaConfiguracionSerializer(serializers.ModelSerializer):
    """
    Serializer para gestionar la configuración de inventario de la empresa.
    """
    class Meta:
        model = Empresa
        fields = [
            'id',
            'nombre',
            'semanas_seguridad',
            'semanas_objetivo', 
            'dias_analisis_demanda'
        ]
        read_only_fields = ['id', 'nombre']
    
    def validate_semanas_seguridad(self, value):
        """Validar que las semanas de seguridad sean razonables"""
        if value < 1:
            raise serializers.ValidationError("Las semanas de seguridad deben ser al menos 1.")
        if value > 12:
            raise serializers.ValidationError("Las semanas de seguridad no pueden exceder 12 semanas.")
        return value
    
    def validate_semanas_objetivo(self, value):
        """Validar que las semanas objetivo sean razonables"""
        if value < 1:
            raise serializers.ValidationError("Las semanas objetivo deben ser al menos 1.")
        if value > 52:
            raise serializers.ValidationError("Las semanas objetivo no pueden exceder 52 semanas.")
        return value
    
    def validate(self, data):
        """Validar que semanas_objetivo >= semanas_seguridad"""
        semanas_seguridad = data.get('semanas_seguridad', self.instance.semanas_seguridad if self.instance else 2)
        semanas_objetivo = data.get('semanas_objetivo', self.instance.semanas_objetivo if self.instance else 4)
        
        if semanas_objetivo < semanas_seguridad:
            raise serializers.ValidationError({
                'semanas_objetivo': 'Las semanas objetivo deben ser mayores o iguales a las semanas de seguridad.'
            })
        
        return data