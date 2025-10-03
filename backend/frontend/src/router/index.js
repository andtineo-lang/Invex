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
import RecuperarPassword from '../components/RecuperarPassword.vue'

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
    path: '/inventario', 
    name: 'Inventario', 
    component: Inventario,
    meta: { requiresAuth: true }
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

export default router
