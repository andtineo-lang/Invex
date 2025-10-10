import { createRouter, createWebHistory } from 'vue-router'
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import Inventario from '../components/inventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'
// ✅ 1. IMPORTA EL COMPONENTE DE CONFIRMACIÓN
import ConfirmacionPago from '@/components/ConfirmacionPago.vue'

const routes = [
  { path: '/', name: 'Principal', component: Principal },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registro', name: 'Registro', component: Registro },
  
  // ✅ 2. AÑADE LA NUEVA RUTA PARA LA CONFIRMACIÓN DEL PAGO
  { 
    path: '/pago/confirmacion', 
    name: 'ConfirmacionPago', 
    component: ConfirmacionPago 
  },

  // Rutas del dashboard agrupadas bajo el layout
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Toda la sección del dashboard requiere login
    children: [
      {
        path: '',
        redirect: '/dashboard/inventario'
      },
      { 
        path: 'inventario', 
        name: 'Inventario', 
        component: Inventario,
        meta: { roles: ['admin', 'manager', 'worker'] }
      },
      { 
        path: 'usuarios', 
        name: 'Usuarios', 
        component: Usuarios,
        meta: { roles: ['admin'] }
      },
      { 
        path: 'proyecciones', 
        name: 'Proyecciones', 
        component: Proyecciones,
        meta: { roles: ['admin', 'manager'] }
      },
      { 
        path: 'reportes', 
        name: 'Reportes', 
        component: Reportes,
        meta: { roles: ['admin', 'manager'] }
      },
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

// 🔒 Guard de navegación con roles (ACTIVADO)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole');

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    alert('No tienes permiso para acceder a esta página.'); 
    return next('/dashboard/inventario'); 
  }

  next();
})

export default router

