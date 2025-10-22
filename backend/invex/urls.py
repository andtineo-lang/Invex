# invex/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from .views import (
    # Se importan todas las vistas necesarias
    RegistroView,
    CustomLoginView,
    CurrentUserView,
    RegisterAndActivateView,
    MarcarTutorialVistoView,
    CurrentEmpresaView,
    InventarioImportAPIView,
    EmpresaViewSet,
    ProductoViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,
    UserManagementViewSet,
    VentasHistoricasView,
    VentasMensualesView,
    TopProductosVendidosView,
    EstadoInventarioView,
    ComprasPorProveedorView,
    LeadTimePorProveedorView,
    ProductoProyeccionesView # 👈 --- VISTA IMPORTANTE AÑADIDA ---
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
    path('auth/registro/', csrf_exempt(RegistroView.as_view()), name='registro'),
    path('auth/login/', csrf_exempt(CustomLoginView.as_view()), name='custom-login'),
    path('auth/register-and-activate/', csrf_exempt(RegisterAndActivateView.as_view()), name='register-and-activate'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # --- Rutas de Gestión de Usuarios y Empresa ---
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # --- Rutas de Acciones Específicas ---
    path('empresas/<int:empresa_id>/importar-inventario/', csrf_exempt(InventarioImportAPIView.as_view()), name='importar-inventario'),

    # --- RUTAS DE ANALÍTICAS Y PROYECCIONES ---
    path('analytics/ventas-historicas/', VentasHistoricasView.as_view(), name='ventas-historicas'),
    path('analytics/ventas-mensuales/', VentasMensualesView.as_view(), name='ventas-mensuales'),
    path('analytics/top-productos/', TopProductosVendidosView.as_view(), name='top-productos'),
    path('analytics/estado-inventario/', EstadoInventarioView.as_view(), name='estado-inventario'),
    path('analytics/compras-proveedor/', ComprasPorProveedorView.as_view(), name='compras-proveedor'),
    path('analytics/lead-time-proveedor/', LeadTimePorProveedorView.as_view(), name='lead-time-proveedor'),
    
    # 👇 --- RUTA CLAVE PARA LA TABLA DE PROYECCIONES ---
    path('productos/proyecciones/', ProductoProyeccionesView.as_view(), name='producto-proyecciones'),

    # --- Rutas CRUD gestionadas por el router ---
    path('', include(router.urls)),
]