import { createRouter, createWebHistory } from 'vue-router'
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import Invex from '../components/Invex.vue'

// Layout
import DashboardLayout from '../components/DashboardLayout.vue'

// Páginas internas del dashboard
import Inventario from '../components/inventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'

const routes = [
  { 
    path: '/', 
    name: 'Principal', 
    component: Principal 
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: Login 
  },
  { 
    path: '/registro', 
    name: 'Registro', 
    component: Registro 
  },
  { 
    path: '/invex', 
    name: 'Invex', 
    component: Invex 
  },

  // Rutas del dashboard agrupadas bajo el layout
  {
    path: '/',
    component: DashboardLayout,
    children: [
      { 
        path: 'inventario', 
        name: 'Inventario', 
        component: Inventario,
        meta: { requiresAuth: true }
        // meta: { requiresAuth: true, roles: ['admin', 'trabajador'] }
      },
      { 
        path: 'usuarios', 
        name: 'Usuarios', 
        component: Usuarios,
        meta: { requiresAuth: true }
        // meta: { requiresAuth: true, roles: ['admin'] }
      },
      { 
        path: 'proyecciones', 
        name: 'Proyecciones', 
        component: Proyecciones,
        meta: { requiresAuth: true }
        // meta: { requiresAuth: true, roles: ['admin', 'trabajador'] }
      },
      { 
        path: 'reportes', 
        name: 'Reportes', 
        component: Reportes,
        meta: { requiresAuth: true }
        // meta: { requiresAuth: true, roles: ['admin', 'trabajador'] }
      },
      { 
        path: 'configuracion', 
        name: 'Configuracion', 
        component: Configuracion,
        meta: { requiresAuth: true }
        // meta: { requiresAuth: true, roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    return { top: 0, behavior: 'smooth' }
  }
})

/*
// 🔒 Guard de navegación con roles (opcional)
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken') // tu token de auth
  const userRole = localStorage.getItem('userRole') || 'trabajador'

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login')
  }

  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    return next('/inventario') // redirige si no tiene permiso
  }

  next()
})
*/

export default router
