from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroView,
    CustomLoginView,
    CurrentUserView,
    EmpresaViewSet,
    ProductoViewSet,
    # StockViewSet,  <-- CORRECCIÓN: Se elimina la importación.
    SuscripcionViewSet,
    DiaImportanteViewSet
)

# Router para ViewSets (operaciones CRUD)
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
# router.register(r'stock', StockViewSet, basename='stock') # <-- CORRECCIÓN: Se elimina esta ruta.
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register(r'dias-importantes', DiaImportanteViewSet, basename='dia-importante')

# Definición de URLs de la API
urlpatterns = [
    # Rutas de autenticación y perfil
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),

    # Rutas CRUD gestionadas por el router
    path('', include(router.urls)),
]