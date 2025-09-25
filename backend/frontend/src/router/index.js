import { createRouter, createWebHistory } from 'vue-router'
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'

const routes = [
  { path: '/', name: 'Principal', component: Principal },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registro', name: 'Registro', component: Registro }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,     // se mueve a la sección con id
        behavior: 'smooth'
      }
    }
    return { top: 0, behavior: 'smooth' } // vuelve arriba al cambiar de ruta
  }
})

export default router
