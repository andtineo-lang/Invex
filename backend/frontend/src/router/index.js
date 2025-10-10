import { createRouter, createWebHistory } from 'vue-router'

// Vistas Públicas
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import Invex from '../components/Invex.vue'
import RecuperarPassword from '../components/RecuperarPassword.vue'
import Caracteristicas from '../components/caracteristicas.vue'
import Precios from '../components/precios.vue'
import Documentacion from '../components/documentacion.vue'
import Contacto from '../components/contacto.vue'
import Faq from '../components/faq.vue'

// Layout y Vistas Privadas (Dashboard)
import DashboardLayout from '../components/DashboardLayout.vue'
import Inventario from '../components/inventario.vue'
import ImportarInventario from '../components/ImportarInventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'

const routes = [
  // --- RUTAS PÚBLICAS SUELTAS ---
  // Estas se renderizan en App.vue, que decide si muestra el Header/Footer público.
  { path: '/', name: 'Principal', component: Principal },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registro', name: 'Registro', component: Registro },
  { path: '/recuperar-password', name: 'RecuperarPassword', component: RecuperarPassword },
  { path: '/invex', name: 'Invex', component: Invex },
  { path: '/caracteristicas', name: 'Caracteristicas', component: Caracteristicas },
  { path: '/precios', name: 'Precios', component: Precios },
  { path: '/documentacion', name: 'Documentacion', component: Documentacion },
  { path: '/contacto', name: 'Contacto', component: Contacto },
  { path: '/faq', name: 'Faq', component: Faq },

  // --- GRUPO DE RUTAS PRIVADAS (DASHBOARD) ---
  // Estas se renderizan dentro del DashboardLayout y no muestran el layout público.
  {
    path: '/app',
    component: DashboardLayout,
    children: [
      { path: 'inventario', name: 'Inventario', component: Inventario, meta: { requiresAuth: true }},
      { path: 'inventario/importar', name: 'ImportarInventario', component: ImportarInventario, meta: { requiresAuth: true }},
      { path: 'usuarios', name: 'Usuarios', component: Usuarios, meta: { requiresAuth: true }},
      { path: 'proyecciones', name: 'Proyecciones', component: Proyecciones, meta: { requiresAuth: true }},
      { path: 'reportes', name: 'Reportes', component: Reportes, meta: { requiresAuth: true }},
      { path: 'configuracion', name: 'Configuracion', component: Configuracion, meta: { requiresAuth: true }},
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
    }
    return { top: 0, behavior: 'smooth' };
  }
})

/*
// :lock: Guard de navegación (opcional)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('userToken');

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  next();
});
*/

export default router