from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.password_validation import validate_password
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
    """
    Serializador final que maneja la creación o actualización de una relación Usuario-Empresa.
    """
    # Campos para LEER (se muestran en la respuesta de la API)
    name = serializers.CharField(source='usuario.nombre', read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)

    # Campo para ESCRIBIR (viene en la petición para crear)
    nombre_completo = serializers.CharField(write_only=True)

    class Meta:
        model = UsuarioEmpresa
        fields = [
            'id',
            'name',
            'email',
            'rol',
            'nombre_completo'
        ]
        read_only_fields = ['id', 'name', 'email']

    def create(self, validated_data):
        """
        Este método ahora usa 'get_or_create' para buscar o crear la relación.
        """
        # Quitamos 'nombre_completo' porque no es parte del modelo UsuarioEmpresa
        validated_data.pop('nombre_completo', None)
        
        # Usamos get_or_create para buscar o crear la relación
        instancia, creada = UsuarioEmpresa.objects.get_or_create(
            usuario=validated_data.get('usuario'),
            empresa=validated_data.get('empresa'),
            defaults={'rol': validated_data.get('rol')}
        )

        # Si la relación no fue creada (ya existía) y el rol es diferente, lo actualizamos
        if not creada and instancia.rol != validated_data.get('rol'):
            instancia.rol = validated_data.get('rol')
            instancia.save()
            
        return instancia


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para el cambio de contraseña con validaciones de seguridad.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Tu contraseña antigua no es correcta.")
        return value
    
    # 👇 NUEVO: Método para validar la nueva contraseña
    def validate_new_password(self, value):
        # Usamos el sistema de validación de Django
        try:
            validate_password(password=value, user=self.context['request'].user)
        except serializers.ValidationError as e:
            # Capturamos los errores de Django y los relanzamos
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        # Comprueba que las contraseñas nuevas coincidan
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas nuevas no coinciden."})
        
        # 👇 NUEVO: Comprueba que la contraseña nueva no sea igual a la antigua
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
        UsuarioEmpresa.objects.create(
            usuario=user,
            empresa=empresa,
            rol='admin'
        )
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
# SERIALIZADOR DE IMPORTACIÓN MASIVA
# ---------------------------
class InventarioImportSerializer(serializers.Serializer):
    """
    Serializador para procesar la lista de objetos de importación
    desde Excel para Producto, Stock y Movimiento.
    """
    nombre = serializers.CharField(max_length=255)
    stock_actual = serializers.IntegerField(required=False, default=0, allow_null=True)
    categoria = serializers.CharField(max_length=255, required=False, allow_null=True)
    unidad_medida = serializers.CharField(max_length=50, required=False, allow_null=True)
    cantidad_comprada = serializers.IntegerField(required=False, default=None, allow_null=True)
    cantidad_vendida = serializers.IntegerField(required=False, default=None, allow_null=True)
    proveedor = serializers.CharField(max_length=255, required=False, allow_null=True)
    fecha_compra_producto = serializers.DateField(required=False, allow_null=True) 
    fecha_pedido = serializers.DateField(required=False, allow_null=True)
    fecha_recepcion = serializers.DateField(required=False, allow_null=True)

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
        fields = ['id', 'nombre_evento', 'fecha', 'descripcion']

# 👇 --- SERIALIZER AÑADIDO PARA CÁLCULOS DINÁMICOS --- 👇
class ProyeccionCalculadaSerializer(serializers.Serializer):
    """
    Este serializer no usa un modelo. Se utiliza para dar formato a los datos 
    de proyección que calculamos manualmente en la vista.
    """
    id = serializers.IntegerField()
    producto_nombre = serializers.CharField()
    stock_actual = serializers.IntegerField()
    demanda_semanal_proyectada = serializers.FloatField()
    semanas_cobertura = serializers.FloatField()
    estado = serializers.CharField()