from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # 'RegistroView' ha sido eliminado de esta lista
    CustomLoginView,
    CurrentUserView,
    RegisterAndActivateView,
    EmpresaViewSet, 
    ProductoViewSet, 
    StockViewSet, 
    SuscripcionViewSet, 
    DiaImportanteViewSet,
    InventarioImportAPIView
)

# Router para ViewSets (operaciones CRUD)
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'stock', StockViewSet, basename='stock')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register(r'dias-importantes', DiaImportanteViewSet, basename='dia-importante')

# Definición de URLs de la API
urlpatterns = [
    # La ruta para 'auth/registro/' ha sido eliminada
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/register-and-activate/', RegisterAndActivateView.as_view(), name='register_and_activate'),
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),
    
    # Ruta para importar inventario
    path('empresas/<int:empresa_id>/importar-inventario/', InventarioImportAPIView.as_view(), name='importar-inventario'),
    
    # Rutas CRUD gestionadas por el router
    path('', include(router.urls)),
]