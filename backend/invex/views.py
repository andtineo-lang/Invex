from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante
from .serializers import *

class RegistroView(generics.CreateAPIView):
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

# CRUD básicos
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = SuscripcionSerializer

class DiaImportanteViewSet(viewsets.ModelViewSet):
    queryset = DiaImportante.objects.all()
    serializer_class = DiaImportanteSerializer
