# invex/urls.py (ACTUALIZADO)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CustomAuthToken 
from .views import *

# --------------------------
# Router para ViewSets (CRUD)
# --------------------------
router = DefaultRouter()
# AÑADIR BASENAME a cada registro para evitar el AssertionError
router.register('empresas', EmpresaViewSet, basename='empresa')
router.register('productos', ProductoViewSet, basename='producto')
router.register('stock', StockViewSet, basename='stock')
router.register('suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register('dias-importantes', DiaImportanteViewSet, basename='dia-importante')

# --------------------------
# Definición de URLs
# --------------------------
urlpatterns = [
    # 1. Ruta de Registro
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    
    # 2. RUTA DE LOGIN ACTUALIZADA
    path('auth/login/', CustomAuthToken.as_view(), name='login-token'),
    
    # 3. Rutas de la API (CRUD)
    path('', include(router.urls)),
]