# invex/urls.py (VERSIÓN FINAL CON RUTAS DE PAGO)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from .views import (
    # Vistas de Pago y Upgrade
    UpgradePlanView,
    IniciarPagoUpgradeView,  # <--- IMPORTANTE: Agregado aquí

    # Vistas de Autenticación y Perfil
    RegistroView,
    CustomLoginView,
    RegisterAndActivateView,
    CurrentUserView,
    MarcarTutorialVistoView,
    CurrentEmpresaView,
    EmpresaConfiguracionView, 
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    
    # Vista de Importación
    InventarioImportAPIView,
    
    # ViewSets
    EmpresaViewSet,
    ProductoViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,
    UserManagementViewSet,
    
    # Vistas de Analíticas (Legacy)
    VentasHistoricasView,
    VentasMensualesView,
    TopProductosVendidosView,
    EstadoInventarioView,
    ComprasPorProveedorView,
    LeadTimePorProveedorView,
    ProductoProyeccionesView,
    KpisGeneralesView,
    
    # Nueva Vista Consolidada
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

    # --- Rutas de Reseteo de Contraseña ---
    path('auth/request-password-reset/', csrf_exempt(PasswordResetRequestView.as_view()), name='password-reset-request'),
    path('auth/reset-password-confirm/', csrf_exempt(PasswordResetConfirmView.as_view()), name='password-reset-confirm'),
    
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # ========================================
    # GESTIÓN DE EMPRESA
    # ========================================
    path('empresa/actual/', CurrentEmpresaView.as_view(), name='current-empresa'),
    path('empresa/configuracion/', EmpresaConfiguracionView.as_view(), name='empresa-configuracion'),

    # ========================================
    # IMPORTACIÓN MASIVA
    # ========================================
    path('empresas/<int:empresa_id>/importar-inventario/', csrf_exempt(InventarioImportAPIView.as_view()), name='importar-inventario'),

    # ========================================
    # ENDPOINT CONSOLIDADO (DASHBOARD)
    # ========================================
    path('analytics/dashboard-consolidado/', DashboardConsolidadoView.as_view(), name='dashboard-consolidado'),

    # ========================================
    # ANALÍTICAS INDIVIDUALES (LEGACY)
    # ========================================
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
    # PAGOS Y UPGRADE (TRANSBANK)
    # ========================================
    # 1. Inicia el pago (Devuelve URL y Token de TB)
    path('pagos/iniciar-upgrade/', IniciarPagoUpgradeView.as_view(), name='iniciar-upgrade'),
    
    # 2. Confirma el pago y actualiza la BD (Se llama al volver de TB)
    path('users/upgrade-plan/', UpgradePlanView.as_view(), name='upgrade-plan'),

    # ========================================
    # CRUD (Router)
    # ========================================
    path('', include(router.urls)),
]