from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Empresa,
    UsuarioEmpresa,
    Producto,
    Stock,
    Suscripcion,
    DiaImportante,
    Categoria
)

Usuario = get_user_model()

# ---------------------------
# REGISTRO (Sin cambios)
# ---------------------------
class RegistroSerializer(serializers.Serializer):
    """
    Maneja el registro de un nuevo usuario y su asociación a una empresa.
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
# SERIALIZERS BÁSICOS (Sin cambios)
# ---------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'date_joined']

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'owner', 'fecha_creacion']

class UsuarioEmpresaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    empresa = EmpresaSerializer()
    class Meta:
        model = UsuarioEmpresa
        fields = ['usuario', 'empresa', 'rol']

# ---------------------------
# PRODUCTOS Y STOCK (VERSIÓN FINAL Y COMPLETA)
# ---------------------------

class StockWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_actual', 'stock_transito', 'ventas_proyectadas', 'demanda_estacional']

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer principal para productos. Maneja lectura, creación y actualización.
    """
    # --- Campos para LEER datos ---
    stock = serializers.SerializerMethodField()
    inTransit = serializers.SerializerMethodField()
    projectedSales = serializers.SerializerMethodField()
    seasonal = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    # --- CAMPOS AÑADIDOS PARA LA PROYECCIÓN DE COMPRA ---
    proyeccion_status = serializers.SerializerMethodField()
    proyeccion_cantidad = serializers.SerializerMethodField()

    # --- Campo para ESCRIBIR datos de stock ---
    stock_data = StockWriteSerializer(write_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'sku', 'categoria',
            'stock', 'inTransit', 'projectedSales', 'seasonal', 'categoria_nombre',
            'stock_data',
            'proyeccion_status', 'proyeccion_cantidad' # <-- Se añaden a la lista
        ]

    # --- Métodos para LEER datos ---
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

    # --- MÉTODOS AÑADIDOS PARA OBTENER LOS DATOS DE PROYECCIÓN ---
    def get_proyeccion_status(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_status if stock_obj else "N/A"

    def get_proyeccion_cantidad(self, obj):
        stock_obj = self.get_first_stock(obj)
        return stock_obj.proyeccion_cantidad_a_comprar if stock_obj else 0

    # --- Lógica para CREAR y ACTUALIZAR (Sin cambios) ---
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

# ---------------------------
# OTROS SERIALIZERS (Sin cambios)
# ---------------------------
class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class DiaImportanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaImportante
        fields = '__all__'