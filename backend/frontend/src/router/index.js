import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// --- 1. LAYOUTS ---
import PublicLayout from '../layouts/PublicLayout.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'

// --- 2. VISTAS PÚBLICAS ---
import Principal from '../components/principal.vue'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import ConfirmacionPago from '../components/ConfirmacionPago.vue'
import RecuperarPassword from '../components/RecuperarPassword.vue'
import ResetPasswordConfirm from '../components/ResetPasswordConfirm.vue' // 👈 1. AÑADIDO

// --- 3. VISTAS DEL DASHBOARD ---
import Inventario from '../components/inventario.vue'
import ImportarInventario from '../components/ImportarInventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'


const routes = [
  // --- GRUPO DE RUTAS PÚBLICAS ---
  {
    path: '/',
    component: PublicLayout,
    children: [
      { path: '', name: 'Principal', component: Principal },
      { path: 'login', name: 'Login', component: Login },
      { path: 'registro', name: 'Registro', component: Registro },
      { path: 'pago/confirmacion', name: 'ConfirmacionPago', component: ConfirmacionPago },
      { path: 'recuperar-password', name: 'RecuperarPassword', component: RecuperarPassword },
      { path: 'reset-password', name: 'ResetPasswordConfirm', component: ResetPasswordConfirm } // 👈 2. AÑADIDO
    ]
  },

  // --- GRUPO DE RUTAS PRIVADAS (DASHBOARD) ---
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Protege todo este grupo
    children: [
      { path: '', redirect: '/dashboard/inventario' }, // Redirección por defecto
      { path: 'inventario', name: 'Inventario', component: Inventario, meta: { roles: ['admin', 'manager', 'worker'] }},
      { path: 'inventario/importar', name: 'ImportarInventario', component: ImportarInventario, meta: { roles: ['admin', 'manager'] }},
      { path: 'usuarios', name: 'Usuarios', component: Usuarios, meta: { roles: ['admin'] }},
      { path: 'proyecciones', name: 'Proyecciones', component: Proyecciones, meta: { roles: ['admin', 'manager'] }},
      { path: 'reportes', name: 'Reportes', component: Reportes, meta: { roles: ['admin', 'manager'] }},
      { path: 'configuracion', name: 'Configuracion', component: Configuracion, meta: { roles: ['admin'] }}
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// --- 4. GUARDIÁN DE NAVEGACIÓN (CONECTADO A PINIA) ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.userRole;

  // Si la ruta requiere autenticación y no hay token, redirige a login.
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login' }); // Usar el nombre de la ruta es más robusto
  }

  // Si la ruta requiere un rol específico y el usuario no lo tiene, redirige al inventario.
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    console.warn(`Acceso denegado a la ruta. Rol requerido: ${to.meta.roles}, Rol del usuario: ${userRole}`);
    return next('/dashboard/inventario'); 
  }

  next(); // Permite el acceso si todo está en orden.
})

export default router