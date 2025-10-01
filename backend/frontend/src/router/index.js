import { createRouter, createWebHistory } from 'vue-router'
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import Inventario from '../components/inventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'
import Invex from '../components/Invex.vue'

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
    path: '/inventario', 
    name: 'Inventario', 
    component: Inventario,
    meta: { requiresAuth: true } // opcional: si quieres proteger la ruta
  },
  { 
    path: '/usuarios', 
    name: 'Usuarios', 
    component: Usuarios,
    meta: { requiresAuth: true }
  },
  { 
    path: '/proyecciones', 
    name: 'Proyecciones', 
    component: Proyecciones,
    meta: { requiresAuth: true }
  },
  { 
    path: '/reportes', 
    name: 'Reportes', 
    component: Reportes,
    meta: { requiresAuth: true }
  },
  { 
    path: '/configuracion', 
    name: 'Configuracion', 
    component: Configuracion,
    meta: { requiresAuth: true }
  },
  { 
    path: '/invex', 
    name: 'Invex', 
    component: Invex 
  }
  // Header, Footer y Modal no necesitan rutas porque son componentes reutilizables
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

// 🔒 OPCIONAL: Guard de navegación para rutas protegidas
// Descomenta esto si quieres proteger rutas que requieren autenticación
/*
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken') // o tu método de auth
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})
*/

export default router