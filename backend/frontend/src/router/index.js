import { createRouter, createWebHistory } from 'vue-router'
import Principal from '../components/principal.vue'
import Registro from '../components/Registro.vue'
import Login from '../components/Login.vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import Inventario from '../components/inventario.vue'
import Usuarios from '../components/usuarios.vue'
import Proyecciones from '../components/proyecciones.vue'
import Reportes from '../components/reportes.vue'
import Configuracion from '../components/configuracion.vue'
// ...otros imports...

const routes = [
  { path: '/', name: 'Principal', component: Principal },
  { path: '/login', name: 'Login', component: Login },
  { path: '/registro', name: 'Registro', component: Registro },
  // ...otras rutas públicas...

  // Rutas del dashboard agrupadas bajo el layout
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Toda la sección del dashboard requiere login
    children: [
      {
        path: '',
        redirect: '/dashboard/inventario'
      },
      { 
        path: 'inventario', 
        name: 'Inventario', 
        component: Inventario,
        meta: { roles: ['admin', 'manager', 'worker'] }
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
        meta: { roles: ['admin', 'manager'] }
      },
      { 
        path: 'reportes', 
        name: 'Reportes', 
        component: Reportes,
        meta: { roles: ['admin', 'manager'] }
      },
      { 
        path: 'configuracion', 
        name: 'Configuracion', 
        component: Configuracion,
        meta: { roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // ... scrollBehavior
})

// 🔒 Guard de navegación con roles (ACTIVADO)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole');

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  // La comprobación de roles solo se aplica a las rutas hijas que tienen 'meta.roles'
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    alert('No tienes permiso para acceder a esta página.'); // Opcional: mostrar alerta
    return next('/dashboard/inventario'); // Redirige si no tiene permiso
  }

  next();
})

export default router