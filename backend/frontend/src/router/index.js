import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import Registro from '../components/Registro.vue'
import Principal from '../components/principal.vue'

const routes = [
  { path: '/', name: 'Home', component: App },
  { path: '/registro', name: 'Registro', component: Registro },
  { path: '/principal', name: 'Principal', component: Principal }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
