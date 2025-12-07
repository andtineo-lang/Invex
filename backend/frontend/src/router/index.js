import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// --- 1. LAYOUTS ---
import PublicLayout from '../layouts/PublicLayout.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'

// --- 2. VISTAS PÚBLICAS (PRINCIPALES) ---
import Principal from '../components/principal.vue'
import Login from '../components/Login.vue'
import Registro from '../components/Registro.vue'
import ConfirmacionPago from '../components/ConfirmacionPago.vue'
import ConfirmacionUpgrade from '../components/ConfirmacionUpgrade.vue'
import RecuperarPassword from '../components/RecuperarPassword.vue'
import ResetPasswordConfirm from '../components/ResetPasswordConfirm.vue'

// --- 3. VISTAS DEL FOOTER Y PÁGINAS INFORMATIVAS ---
import Caracteristicas from '../components/caracteristicas.vue' 
import Precios from '../components/precios.vue' // Este es tu archivo actual (Mejora de planes/Upgrade)
import Planes from '../components/PlanesPublicos.vue'   // 🔥 NUEVO: Importamos el archivo de planes públicos
import Documentacion from '../components/documentacion.vue'
import Contacto from '../components/contacto.vue'
import Faq from '../components/faq.vue'

// --- 4. VISTAS DEL DASHBOARD ---
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
      { path: 'login', name: 'Login', component: Login, meta: { guest: true } }, 
      { path: 'registro', name: 'Registro', component: Registro, meta: { guest: true } },
      
      // Pago de Registro (Cuenta Nueva)
      { path: 'pago/confirmacion', name: 'ConfirmacionPago', component: ConfirmacionPago },
      
      // Pago de Upgrade (Cuenta Existente)
      { 
        path: 'pago/confirmacion-upgrade', 
        name: 'ConfirmacionUpgrade', 
        component: ConfirmacionUpgrade,
        meta: { requiresAuth: true }
      },

      { path: 'recuperar-password', name: 'RecuperarPassword', component: RecuperarPassword, meta: { guest: true } },
      { path: 'reset-password', name: 'ResetPasswordConfirm', component: ResetPasswordConfirm, meta: { guest: true } },
      
      // RUTAS DEL FOOTER / INFORMATIVAS
      { path: 'caracteristicas', name: 'Caracteristicas', component: Caracteristicas },
      
      // 🔥 AQUÍ ESTÁ LA SEPARACIÓN:
      
      // 1. Ruta Pública (Para gente nueva que quiere ver qué planes hay)
      // Asegúrate de crear el archivo 'src/components/planes.vue'
      { path: 'planes', name: 'Planes', component: Planes },

      // 2. Ruta de Upgrade (Posiblemente para usuarios ya registrados o vista detallada)
      // Apunta a tu archivo original 'precios.vue'
      { path: 'precios', name: 'Precios', component: Precios },

      { path: 'documentacion', name: 'Documentacion', component: Documentacion },
      { path: 'contacto', name: 'Contacto', component: Contacto },
      { path: 'faq', name: 'Faq', component: Faq }
    ]
  },

  // --- GRUPO DE RUTAS PRIVADAS (DASHBOARD) ---
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, 
    children: [
      { path: '', redirect: { name: 'Inventario' } },
      
      { 
        path: 'inventario', 
        name: 'Inventario', 
        component: Inventario, 
        meta: { roles: ['admin', 'manager', 'worker'] }
      },
      { 
        path: 'inventario/importar', 
        name: 'ImportarInventario', 
        component: ImportarInventario, 
        meta: { roles: ['admin', 'manager'] }
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
        meta: { roles: ['admin', 'manager', 'viewer'] }
      },
      { 
        path: 'reportes', 
        name: 'Reportes', 
        component: Reportes, 
        meta: { roles: ['admin', 'manager', 'viewer'] }
      },
      { 
        path: 'configuracion', 
        name: 'Configuracion', 
        component: Configuracion, 
        meta: { roles: ['admin', 'manager'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// --- 5. GUARDIÁN DE NAVEGACIÓN ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  const isAuthenticated = authStore.isAuthenticated;
  const userRole = (authStore.userRole || '').toLowerCase();

  // 1. Bloqueo de no autenticados
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    return next({ name: 'Login' }); 
  }

  // 2. Bloqueo de invitados
  if (to.meta.guest && isAuthenticated) {
    if (userRole === 'viewer') {
        return next({ name: 'Proyecciones' });
    }
    return next({ name: 'Inventario' });
  }

  // 3. Validación de ROLES
  if (to.meta.roles) {
    if (!userRole) {
       return next({ name: 'Login' });
    }

    if (!to.meta.roles.includes(userRole)) {
      console.warn(`⛔ Acceso Denegado. Requerido: [${to.meta.roles}], Tu Rol: ${userRole}`);
      
      if (userRole === 'viewer') {
          return next({ name: 'Proyecciones' });
      }

      return next({ name: 'Inventario' }); 
    }
  }
  
  next(); 
})

export default router