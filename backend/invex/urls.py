# invex/urls.py (ACTUALIZADO CON ENDPOINT CONSOLIDADO)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from .views import (
    # Vistas de Autenticación y Perfil
    RegistroView,
    CustomLoginView,
    CurrentUserView,
    RegisterAndActivateView,
    MarcarTutorialVistoView,
    CurrentEmpresaView,
    
    # Vista de Importación
    InventarioImportAPIView,
    
    # ViewSets
    EmpresaViewSet,
    ProductoViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,
    UserManagementViewSet,
    
    # Vistas de Analíticas (Legacy - Mantener para compatibilidad)
    VentasHistoricasView,
    VentasMensualesView,
    TopProductosVendidosView,
    EstadoInventarioView,
    ComprasPorProveedorView,
    LeadTimePorProveedorView,
    ProductoProyeccionesView,
    KpisGeneralesView,
    
    # 🆕 Nueva Vista Consolidada (RECOMENDADA)
    DashboardConsolidadoView,
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
    # ========================================
    # AUTENTICACIÓN Y PERFIL
    # ========================================
    path('auth/registro/', csrf_exempt(RegistroView.as_view()), name='registro'),
    path('auth/login/', csrf_exempt(CustomLoginView.as_view()), name='custom-login'),
    path('auth/register-and-activate/', csrf_exempt(RegisterAndActivateView.as_view()), name='register-and-activate'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # ========================================
    # GESTIÓN DE EMPRESA
    # ========================================
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # ========================================
    # IMPORTACIÓN MASIVA
    # ========================================
    path('empresas/<int:empresa_id>/importar-inventario/', csrf_exempt(InventarioImportAPIView.as_view()), name='importar-inventario'),

    # ========================================
    # ENDPOINT CONSOLIDADO (RECOMENDADO)
    # ========================================
    # Este endpoint devuelve todos los datos del dashboard en UNA SOLA llamada
    # Incluye: proyecciones, ventas mensuales, lead times, estado inventario y KPIs
    # ✅ Úsalo en lugar de los endpoints individuales para mejor rendimiento
    path('analytics/dashboard-consolidado/', DashboardConsolidadoView.as_view(), name='dashboard-consolidado'),

    # ========================================
    # ANALÍTICAS INDIVIDUALES (LEGACY)
    # ========================================
    # Estos endpoints se mantienen para compatibilidad con código existente
    # pero se recomienda usar el endpoint consolidado arriba
    path('analytics/ventas-historicas/', VentasHistoricasView.as_view(), name='ventas-historicas'),
    path('analytics/ventas-mensuales/', VentasMensualesView.as_view(), name='ventas-mensuales'),
    path('analytics/top-productos/', TopProductosVendidosView.as_view(), name='top-productos'),
    path('analytics/estado-inventario/', EstadoInventarioView.as_view(), name='estado-inventario'),
    path('analytics/compras-proveedor/', ComprasPorProveedorView.as_view(), name='compras-proveedor'),
    path('analytics/lead-time-proveedor/', LeadTimePorProveedorView.as_view(), name='lead-time-proveedor'),
    path('analytics/kpis-generales/', KpisGeneralesView.as_view(), name='kpis-generales'),

    # ========================================
    # PROYECCIONES DE PRODUCTOS
    # ========================================
    path('productos/proyecciones/', ProductoProyeccionesView.as_view(), name='producto-proyecciones'),

    # ========================================
    # CRUD (Router)
    # ========================================
    path('', include(router.urls)),
]



