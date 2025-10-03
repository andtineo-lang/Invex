from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante

Usuario = get_user_model()

# ---------------------------
# REGISTRO
# ---------------------------
class RegistroSerializer(serializers.Serializer):
    empresa_nombre = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        empresa_nombre = validated_data['empresa_nombre']
        email = validated_data['email']
        password = validated_data['password']

        # Crear o recuperar usuario
        usuario, created_u = Usuario.objects.get_or_create(email=email)
        if created_u:
            usuario.set_password(password)
            usuario.save()

        # Crear o recuperar empresa
        empresa, created_e = Empresa.objects.get_or_create(nombre=empresa_nombre)

        # Si la empresa no tenía dueño, este usuario será owner y admin
        if empresa.owner is None:
            empresa.owner = usuario
            empresa.save()
            rol = 'admin'
        else:
            # Usuario se agrega como viewer por defecto
            rol = 'viewer'

        # Crear relación si no existe
        UsuarioEmpresa.objects.get_or_create(usuario=usuario, empresa=empresa, defaults={'rol': rol})

        return {
            "usuario": usuario,
            "empresa": empresa,
            "rol": rol
        }

# ---------------------------
# OTROS SERIALIZERS
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

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

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
