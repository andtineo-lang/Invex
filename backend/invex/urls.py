from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # Auth / usuario
    RegistroView,
    CustomLoginView,
    CurrentUserView,
    CurrentEmpresaView,
    MarcarTutorialVistoView,
    RegisterAndActivateView,
    ChangePasswordView,

    # ViewSets
    UserManagementViewSet,
    EmpresaViewSet,
    ProductoViewSet,
    SuscripcionViewSet,
    DiaImportanteViewSet,

    # Importación / dashboard / reportes
    InventarioImportAPIView,
    DashboardConsolidadoView,
    VentasHistoricasView,
    VentasMensualesView,
    TopProductosVendidosView,
    ProductoProyeccionesView,
    EstadoInventarioView,
    ComprasPorProveedorView,
    LeadTimePorProveedorView,
    KpisGeneralesView,
)

router = DefaultRouter()
router.register(r'usuarios', UserManagementViewSet, basename='usuario-empresa')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripcion')
router.register(r'dias-importantes', DiaImportanteViewSet, basename='dia-importante')

urlpatterns = [
    # AUTH / REGISTRO
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    # si usas el registro full (RegisterAndActivateView) puedes exponerlo en otra ruta:
    path('auth/registro-full/', RegisterAndActivateView.as_view(), name='registro-full'),

    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/cambiar-password/', ChangePasswordView.as_view(), name='cambiar-password'),
    path('auth/marcar-tutorial-visto/', MarcarTutorialVistoView.as_view(), name='marcar-tutorial-visto'),

    # USUARIO Y EMPRESA ACTUAL
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('empresas/current/', CurrentEmpresaView.as_view(), name='current-empresa'),

    # INVENTARIO / IMPORTACIÓN
    path('inventario/importar/', InventarioImportAPIView.as_view(), name='inventario-import'),

    # DASHBOARD / REPORTES
    path('dashboard/consolidado/', DashboardConsolidadoView.as_view(), name='dashboard-consolidado'),
    path('reportes/ventas-historicas/', VentasHistoricasView.as_view(), name='ventas-historicas'),
    path('reportes/ventas-mensuales/', VentasMensualesView.as_view(), name='ventas-mensuales'),
    path('reportes/proyecciones-productos/', ProductoProyeccionesView.as_view(), name='producto-proyecciones'),
    path('reportes/estado-inventario/', EstadoInventarioView.as_view(), name='estado-inventario'),
    path('reportes/top-productos-vendidos/', TopProductosVendidosView.as_view(), name='top-productos-vendidos'),
    path('reportes/compras-por-proveedor/', ComprasPorProveedorView.as_view(), name='compras-por-proveedor'),
    path('reportes/leadtime-por-proveedor/', LeadTimePorProveedorView.as_view(), name='leadtime-por-proveedor'),
    path('reportes/kpis-generales/', KpisGeneralesView.as_view(), name='kpis-generales'),

    # CRUDs vía router
    path('', include(router.urls)),
]
