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
import RecuperarPassword from '../components/RecuperarPassword.vue'

// Importar las vistas
import Caracteristicas from '../components/caracteristicas.vue'
import Precios from '../components/precios.vue'
import Documentacion from '../components/documentacion.vue'
import Contacto from '../components/contacto.vue'
import Faq from '../components/faq.vue'
//pago
import ConfirmacionPago from '@/components/ConfirmacionPago.vue'

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
    path: '/recuperar-password', 
    name: 'RecuperarPassword', 
    component: RecuperarPassword 
  },
  { 
    path: '/invex', 
    name: 'Invex', 
    component: Invex 
  },
  // --- Páginas del Footer ---
  { 
    path: '/caracteristicas', 
    name: 'Caracteristicas', 
    component: Caracteristicas 
  },
  { 
    path: '/precios', 
    name: 'Precios', 
    component: Precios 
  },
  { 
    path: '/documentacion', 
    name: 'Documentacion', 
    component: Documentacion 
  },
  { 
    path: '/contacto', 
    name: 'Contacto', 
    component: Contacto 
  },
  { 
    path: '/faq', 
    name: 'Faq', 
    component: Faq 
  },

  //pago
  {
  path: '/pago/confirmacion', // Esta es la URL que Transbank usará
  name: 'ConfirmacionPago',
  component: ConfirmacionPago
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
