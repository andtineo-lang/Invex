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
  routes
})

export default router
