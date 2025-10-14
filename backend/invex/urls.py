from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomLoginView,
    CurrentUserView,
    RegisterAndActivateView,
    EmpresaViewSet,
    ProductoViewSet,
    StockViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,
    InventarioImportAPIView,
    MarcarTutorialVistoView,
    CrearUsuarioEmpresaView,
    CurrentEmpresaView,  # <-- ✨ 1. IMPORTA LA NUEVA VISTA
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
    # --- Rutas de Autenticación y Perfil ---
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/register-and-activate/', RegisterAndActivateView.as_view(), name='register_and_activate'),
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),
    path('auth/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # --- Rutas de Gestión de Usuarios y Empresa ---
    path('usuarios/crear/', CrearUsuarioEmpresaView.as_view(), name='crear-usuario-empresa'),
    
    # 👇 2. AÑADE LA NUEVA RUTA AQUÍ
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # --- Rutas de Acciones Específicas ---
    path('empresas/<int:empresa_id>/importar-inventario/', InventarioImportAPIView.as_view(), name='importar-inventario'),

    # --- Rutas CRUD gestionadas por el router ---
    path('', include(router.urls)),
]