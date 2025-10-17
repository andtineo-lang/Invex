from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Se importan todas las vistas necesarias
    RegistroView,
    CustomLoginView,
    CurrentUserView,
    RegisterAndActivateView,
    MarcarTutorialVistoView,
    # CrearUsuarioEmpresaView,
    CurrentEmpresaView,
    InventarioImportAPIView,
    EmpresaViewSet,
    ProductoViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,
    UserManagementViewSet,
)

# Router para ViewSets (operaciones CRUD)
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register(r'dias-importantes', DiaImportanteViewSet, basename='dia-importante')
router.register(r'usuarios', UserManagementViewSet, basename='usuario-gestion') # 👈 AÑADE ESTA LÍNEA

# Definición de URLs de la API
urlpatterns = [
    # --- Rutas de Autenticación y Perfil ---
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    path('auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('auth/register-and-activate/', RegisterAndActivateView.as_view(), name='register-and-activate'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # --- Rutas de Gestión de Usuarios y Empresa ---
  #  path('usuarios/crear/', CrearUsuarioEmpresaView.as_view(), name='crear-usuario-empresa'),
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # --- Rutas de Acciones Específicas ---
    path('empresas/<int:empresa_id>/importar-inventario/', InventarioImportAPIView.as_view(), name='importar-inventario'),

    # --- Rutas CRUD gestionadas por el router ---
    path('', include(router.urls)),
]