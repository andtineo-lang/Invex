# invex/views.py
import csv
import io
from django.db import transaction
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante
from .serializers import *


# ----------------------------------------------------
# FUNCIÓN AUXILIAR DE FILTRADO
# ----------------------------------------------------

def get_user_companies_ids(user):
    """ Retorna una lista de IDs de las empresas a las que pertenece el usuario. """
    return UsuarioEmpresa.objects.filter(usuario=user).values_list('empresa_id', flat=True)


# ----------------------------------------------------
# AUTENTICACIÓN
# ----------------------------------------------------

class RegistroView(generics.CreateAPIView):
    """ Vista para el registro de nuevos usuarios y creación inicial de una empresa. """
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        return Response({
            "mensaje": "Registro exitoso",
            "usuario": UsuarioSerializer(result["usuario"]).data,
            "empresa": EmpresaSerializer(result["empresa"]).data,
            "rol": result["rol"]
        })

# ----------------------------------------------------
# VISTA DE ACCIÓN PERSONALIZADA
# ----------------------------------------------------

class InventarioImportAPIView(APIView):
    """
    Vista para la importación masiva de inventario, ya sea por archivo CSV o datos JSON.
    Valida que el usuario pertenezca a la empresa a la que intenta importar datos.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, empresa_id):
        # 1. Verificación de permisos
        user = request.user
        empresas_del_usuario = get_user_companies_ids(user)
        if empresa_id not in empresas_del_usuario:
            return Response({"error": "No tienes permiso para acceder a esta empresa."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            empresa = Empresa.objects.get(pk=empresa_id)
        except Empresa.DoesNotExist:
            return Response({"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Determinar el tipo de contenido y procesar
        content_type = request.content_type
        
        if 'multipart/form-data' in content_type:
            file = request.FILES.get('file')
            if not file:
                return Response({"error": "No se proporcionó ningún archivo."}, status=status.HTTP_400_BAD_REQUEST)
            return self._procesar_csv(file, empresa)

        elif 'application/json' in content_type:
            data = request.data
            if not isinstance(data, list) or not data:
                return Response({"error": "Los datos deben ser una lista de productos."}, status=status.HTTP_400_BAD_REQUEST)
            return self._procesar_json(data, empresa)
            
        return Response({"error": "Formato de contenido no soportado."}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def _procesar_csv(self, file, empresa):
        try:
            decoded_file = io.TextIOWrapper(file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)
            productos_a_crear = list(reader)
        except Exception as e:
            return Response({"error": f"Error al leer el archivo CSV: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return self._procesar_json(productos_a_crear, empresa)

    def _procesar_json(self, productos_data, empresa):
        errores = []
        productos_procesados = 0

        try:
            with transaction.atomic():
                for i, item in enumerate(productos_data):
                    nombre_producto = item.get('nombre')
                    stock_actual = item.get('stock_actual', '0')
                    
                    if not nombre_producto:
                        errores.append(f"Fila {i+1}: El nombre del producto es obligatorio.")
                        continue

                    try:
                        stock_actual_num = int(stock_actual)
                    except (ValueError, TypeError):
                        errores.append(f"Fila {i+1} ('{nombre_producto}'): 'stock_actual' debe ser un número.")
                        continue
                    
                    producto, created = Producto.objects.get_or_create(
                        empresa=empresa,
                        nombre__iexact=nombre_producto.strip(), # Búsqueda insensible a mayúsculas
                        defaults={'nombre': nombre_producto.strip(), 'unidad_medida': item.get('unidad_medida', 'unidades')}
                    )

                    Stock.objects.update_or_create(
                        producto=producto,
                        defaults={
                            'stock_actual': stock_actual_num,
                            'stock_transito': int(item.get('stock_transito', 0) or 0),
                            'ventas_proyectadas': int(item.get('ventas_proyectadas', 0) or 0),
                        }
                    )
                    productos_procesados += 1
            
                if errores:
                    raise ValueError("Se encontraron errores de validación.")

        except (ValueError, Exception) as e:
            return Response({
                "error": "No se pudo completar la importación debido a errores en los datos.",
                "detalles": errores if errores else [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "mensaje": f"Se importaron y/o actualizaron {productos_procesados} productos exitosamente."
        }, status=status.HTTP_201_CREATED)


# ----------------------------------------------------
# VIEWSETS DE DATOS (Requieren Autenticación y Filtrado)
# ----------------------------------------------------

class EmpresaViewSet(viewsets.ModelViewSet):
    """ CRUD para Empresas. Filtra para mostrar solo las empresas del usuario autenticado. """
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Empresa.objects.filter(id__in=empresas_ids)

    def perform_create(self, serializer):
        empresa = serializer.save(owner=self.request.user)
        UsuarioEmpresa.objects.create(usuario=self.request.user, empresa=empresa, rol='admin')


class ProductoViewSet(viewsets.ModelViewSet):
    """ CRUD para Productos. Filtra productos que pertenecen a las empresas del usuario. """
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Producto.objects.filter(empresa_id__in=empresas_ids)


class StockViewSet(viewsets.ModelViewSet):
    """ CRUD para Stock. Filtra el stock asociado a los productos de las empresas del usuario. """
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Stock.objects.filter(producto__empresa_id__in=empresas_ids)


class SuscripcionViewSet(viewsets.ModelViewSet):
    """ CRUD para Suscripción. Filtra por la suscripción de las empresas del usuario. """
    serializer_class = SuscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return Suscripcion.objects.filter(empresa_id__in=empresas_ids)


class DiaImportanteViewSet(viewsets.ModelViewSet):
    """ CRUD para Días Importantes. Filtra por la empresa del usuario. """
    serializer_class = DiaImportanteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresas_ids = get_user_companies_ids(user)
        return DiaImportante.objects.filter(empresa_id__in=empresas_ids)