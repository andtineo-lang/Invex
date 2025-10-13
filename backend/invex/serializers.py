from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Usuario, Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante, Categoria

# ---------------------------
# SERIALIZADOR DE REGISTRO COMPLETO
# ---------------------------
class FullRegistrationSerializer(serializers.Serializer):
    # ---------------------------
   # Gestiona la validación y creación de un nuevo usuario, empresa y suscripción
   # en una sola transacción después de un pago exitoso.
   # ---------------------------
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    company = serializers.CharField(max_length=255)
    rut = serializers.CharField(max_length=20)
    industry = serializers.CharField(max_length=255)
    plan = serializers.CharField(max_length=50)

    def validate_email(self, value):
         # ---------------------------
       #  """ Valida que el email no esté ya en uso. """
         # ---------------------------
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo electrónico.")
        return value

    @transaction.atomic
    def create(self, validated_data):
         # ---------------------------
        # Crea el Usuario, la Empresa, la relación y la Suscripción de forma segura.
         # ---------------------------
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
        plan_map = {
            'Plan Trimestral': '3m',
            'Plan Semestral': '6m',
            'Plan Anual': '1y',
        }
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
# SERIALIZERS DE MODELOS (PARA CRUD)
# ---------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre']

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        # Se añaden los nuevos campos 'rut' y 'rubro'
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

class ProductoSerializer(serializers.ModelSerializer):
    # Opcional: Mostrar el nombre de la categoría en lugar de solo su ID
    categoria = serializers.StringRelatedField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'unidad_medida', 'categoria', 'empresa']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class DiaImportanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaImportante
        fields = '__all__'