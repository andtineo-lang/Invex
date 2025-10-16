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
    Proveedor,  # Importado para la importación masiva
    Movimiento  # Importado para la importación masiva
)

# ---------------------------
# SERIALIZADOR DE REGISTRO SIMPLE
# ---------------------------
class RegistroSerializer(serializers.Serializer):
    """
    Maneja un registro simple de usuario y empresa. Útil para flujos rápidos.
    """
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

# ---------------------------
# SERIALIZADOR DE REGISTRO COMPLETO (DESPUÉS DEL PAGO)
# ---------------------------
class FullRegistrationSerializer(serializers.Serializer):
    """
    Gestiona la creación de un nuevo usuario, empresa y suscripción en una sola transacción.
    """
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
        # 1. Crear el Usuario
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['name']
        )
        # 2. Crear la Empresa
        empresa = Empresa.objects.create(
            nombre=validated_data['company'],
            rut=validated_data['rut'],
            rubro=validated_data['industry'],
            owner=user
        )
        # 3. Crear la relación Usuario-Empresa
        UsuarioEmpresa.objects.create(
            usuario=user,
            empresa=empresa,
            rol='admin'
        )
        # 4. Crear la Suscripción
        plan_map = {'Plan Trimestral': '3m', 'Plan Semestral': '6m', 'Plan Anual': '1y'}
        plan_tipo = plan_map.get(validated_data['plan'])
        if not plan_tipo:
            raise serializers.ValidationError("Tipo de plan no válido.")
        
        fecha_inicio = timezone.now().date()
        if plan_tipo == '3m':
            fecha_fin = fecha_inicio + relativedelta(months=+3)
        elif plan_tipo == '6m':
            fecha_fin = fecha_inicio + relativedelta(months=+6)
        else: # '1y'
            fecha_fin = fecha_inicio + relativedelta(years=+1)
            
        Suscripcion.objects.create(
            empresa=empresa,
            tipo=plan_tipo,
            fecha_fin=fecha_fin,
            pago_por=user
        )
        return user

# ---------------------------
# SERIALIZADOR DE IMPORTACIÓN MASIVA (NUEVO)
# ---------------------------
class InventarioImportSerializer(serializers.Serializer):
    """
    Serializador para procesar la lista de objetos de importación
    que incluyen datos de Producto, Stock y Movimiento desde Excel.
    """
    # Campos base de Producto/Stock
    nombre = serializers.CharField(max_length=255)
    stock_actual = serializers.IntegerField(required=False, default=0, allow_null=True)
    categoria = serializers.CharField(max_length=255, required=False, allow_null=True)
    unidad_medida = serializers.CharField(max_length=50, required=False, allow_null=True)
    
    # Nuevos campos de Movimiento (Opcionales)
    cantidad_comprada = serializers.IntegerField(required=False, default=None, allow_null=True)
    cantidad_vendida = serializers.IntegerField(required=False, default=None, allow_null=True)
    proveedor = serializers.CharField(max_length=255, required=False, allow_null=True)
    
    # 💥 MODIFICADO: Usamos fecha_compra_producto en lugar de fecha_transaccion
    fecha_compra_producto = serializers.DateField(required=False, allow_null=True) 
    
    fecha_pedido = serializers.DateField(required=False, allow_null=True)
    fecha_recepcion = serializers.DateField(required=False, allow_null=True)


# ---------------------------
# SERIALIZERS DE MODELOS (PARA CRUD)
# ---------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # 👇 AÑADE 'mostrar_tutorial' A LOS CAMPOS
        fields = ['id', 'email', 'nombre', 'mostrar_tutorial'] 


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        # Se incluyen los campos 'rut' y 'rubro'
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

# --- Serializer de Productos y Stock (La versión avanzada) ---
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
        stock_obj = self.get_first_stock(obj); return stock_obj.stock_actual if stock_obj else 0
    def get_inTransit(self, obj):
        stock_obj = self.get_first_stock(obj); return stock_obj.stock_transito if stock_obj else 0
    def get_projectedSales(self, obj):
        stock_obj = self.get_first_stock(obj); return stock_obj.ventas_proyectadas if stock_obj else 0
    def get_seasonal(self, obj):
        stock_obj = self.get_first_stock(obj); return stock_obj.demanda_estacional if stock_obj else "Normal"
    def get_proyeccion_status(self, obj):
        stock_obj = self.get_first_stock(obj); return stock_obj.proyeccion_status if stock_obj else "N/A"
    def get_proyeccion_cantidad(self, obj):
        stock_obj = self.get_first_stock(obj); return stock_obj.proyeccion_cantidad_a_comprar if stock_obj else 0

    def create(self, validated_data):
        stock_data = validated_data.pop('stock_data')
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'): raise serializers.ValidationError("Contexto de request no encontrado.")
        relacion = request.user.relaciones.first()
        if not relacion: raise serializers.ValidationError("El usuario no está asociado a ninguna empresa.")
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
        fields = '__all__'