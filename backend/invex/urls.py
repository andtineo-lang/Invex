from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('empresas', EmpresaViewSet)
router.register('productos', ProductoViewSet)
router.register('stock', StockViewSet)
router.register('suscripciones', SuscripcionViewSet)
router.register('dias-importantes', DiaImportanteViewSet)

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('', include(router.urls)),
]
