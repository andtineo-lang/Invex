import { createRouter, createWebHistory } from 'vue-router'

// --- Vistas Públicas ---
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import ConfirmacionPago from '../components/ConfirmacionPago.vue' // Asegúrate de que el path sea correcto

// --- Layout y Vistas Privadas (Dashboard) ---
import DashboardLayout from '../components/DashboardLayout.vue'
import Inventario from '../components/inventario.vue'
import ImportarInventario from '../components/ImportarInventario.vue' // Añadido del segundo fragmento
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'

const routes = [
  // --- RUTAS PÚBLICAS ---
  { path: '/', name: 'Principal', component: Principal },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registro', name: 'Registro', component: Registro },
  
  // Ruta de confirmación de pago
  { 
    path: '/pago/confirmacion', 
    name: 'ConfirmacionPago', 
    component: ConfirmacionPago 
  },

  // --- RUTAS PRIVADAS (DASHBOARD) ---
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Toda la sección del dashboard requiere login
    children: [
      // Redirecciona al entrar a /dashboard
      {
        path: '',
        redirect: '/dashboard/inventario'
      },
      // Gestión de Inventario
      { 
        path: 'inventario', 
        name: 'Inventario', 
        component: Inventario,
        meta: { roles: ['admin', 'manager', 'worker'] }
      },
      // Importar Inventario (Añadido)
      { 
        path: 'inventario/importar', 
        name: 'ImportarInventario', 
        component: ImportarInventario, 
        meta: { roles: ['admin', 'manager'] } // Asumo que solo admin/manager pueden importar
      },
      // Gestión de Usuarios
      { 
        path: 'usuarios', 
        name: 'Usuarios', 
        component: Usuarios,
        meta: { roles: ['admin'] }
      },
      // Proyecciones
      { 
        path: 'proyecciones', 
        name: 'Proyecciones', 
        component: Proyecciones,
        meta: { roles: ['admin', 'manager'] }
      },
      // Reportes
      { 
        path: 'reportes', 
        name: 'Reportes', 
        component: Reportes,
        meta: { roles: ['admin', 'manager'] }
      },
      // Configuración
      { 
        path: 'configuracion', 
        name: 'Configuracion', 
        component: Configuracion,
        meta: { roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 🔒 GUARD DE NAVEGACIÓN CON ROLES (Middleware)
router.beforeEach((to, from, next) => {
  // Asegúrate de que estás usando un método de persistencia (como cookies o un store global) en lugar de alert().
  const isAuthenticated = !!localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole');

  // 1. Verificar autenticación si es requerida
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('Redireccionando a login: No autenticado.');
    // Usamos el return aquí para evitar llamar a next() más tarde
    return next('/login');
  }

  // 2. Verificar roles si son requeridos
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    // Usar una notificación de UI en lugar de alert()
    console.warn(`Acceso denegado: Rol (${userRole}) no autorizado para esta ruta.`);
    // Opcional: podrías redirigir a una página de "Acceso Denegado"
    // Redirigir a una ruta segura dentro del dashboard
    return next('/dashboard/inventario'); 
  }

  // Si pasa todas las comprobaciones, continúa la navegación
  next();
})

export default router
