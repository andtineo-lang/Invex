from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt # 👈 NUEVA IMPORTACIÓN
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
    ChangePasswordView,
)

# Router para ViewSets (operaciones CRUD)
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register(r'dias-importantes', DiaImportanteViewSet, basename='dia-importante')
router.register(r'usuarios', UserManagementViewSet, basename='usuario-gestion') 

# Definición de URLs de la API
urlpatterns = [
    # --- Rutas de Autenticación y Perfil ---
    # El registro (POST) también podría requerir csrf_exempt si el frontend es Vue.
    path('auth/registro/', csrf_exempt(RegistroView.as_view()), name='registro'), # 👈 Aplicar csrf_exempt
    
    # El LOGIN (POST) NECESITA csrf_exempt para evitar el 401 en CORS
    path('auth/login/', csrf_exempt(CustomLoginView.as_view()), name='custom-login'), # 👈 Aplicar csrf_exempt
    
    path('auth/register-and-activate/', csrf_exempt(RegisterAndActivateView.as_view()), name='register-and-activate'), # 👈 Aplicar csrf_exempt
    
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # --- Rutas de Gestión de Usuarios y Empresa ---
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # --- Rutas de Acciones Específicas ---
    # Esta ruta acepta POST/PUT, también podría necesitar csrf_exempt
    path('empresas/<int:empresa_id>/importar-inventario/', csrf_exempt(InventarioImportAPIView.as_view()), name='importar-inventario'),

    # --- Rutas CRUD gestionadas por el router ---
    path('', include(router.urls)),
]