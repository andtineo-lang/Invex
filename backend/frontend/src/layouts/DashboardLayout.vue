<template>
  <div class="layout-container">
    <nav class="main-nav">
      <div class="nav-content">
        <div class="flex-shrink-0">
          <h1 class="text-2xl font-bold text-white">INVEX</h1>
        </div>

        <div id="nav-principal" class="hidden md:flex items-center space-x-2">
          <button
            v-for="item in navItems"
            :key="item.name"
            :id="`nav-button-${item.name.toLowerCase()}`"
            @click="navigateTo(item.path)"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
              $route.path.startsWith(item.path)
                ? 'bg-white text-teal-600 shadow-md'
                : 'text-white hover:bg-teal-500 hover:bg-opacity-75'
            ]"
          >
            {{ item.name }}
          </button>
        </div>

        <div class="flex items-center">
          <div id="menu-perfil" class="hidden md:block relative ml-4">
            <div @click="perfilOpen = !perfilOpen" class="flex items-center space-x-2 cursor-pointer">
              <span class="bg-white text-teal-600 font-bold rounded-full h-8 w-8 flex items-center justify-center">
                {{ user.iniciales }}
              </span>
            </div>
            <transition name="fade">
              <div v-if="perfilOpen" class="dropdown-menu">
                <div class="px-4 py-2 border-b">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ user.nombre }}</p>
                  <p class="text-xs text-gray-500 capitalize">{{ user.rol }}</p>
                </div>
                <a @click.prevent="openChangePasswordModal" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Cambiar Contraseña</a>
                <a @click.prevent="logout" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 border-t">Cerrar sesión</a>
              </div>
            </transition>
          </div>
          <div class="md:hidden ml-4">
            <button @click="menuOpen = !menuOpen" class="text-white focus:outline-none">
              <svg v-if="!menuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" /></svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="menuOpen" class="md:hidden mobile-menu">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <button
            v-for="item in navItems"
            :key="item.name"
            @click="navigateTo(item.path)"
            :class="[
              'block w-full text-left px-3 py-2 rounded-md text-base font-medium',
              $route.path.startsWith(item.path) ? 'bg-white text-teal-600' : 'text-white hover:bg-teal-500'
            ]">
            {{ item.name }}
          </button>
        </div>
        <div class="mobile-profile">
          <div class="flex items-center px-5">
            <span class="bg-white text-teal-600 font-bold rounded-full h-10 w-10 flex items-center justify-center">
              {{ user.iniciales }}
            </span>
            <div class="ml-3">
              <div class="text-base font-medium text-white">{{ user.nombre }}</div>
              <div class="text-sm font-medium text-teal-300 capitalize">{{ user.rol }}</div>
            </div>
          </div>
          <div class="mt-3 px-2 space-y-1">
            <a @click.prevent="openChangePasswordModal" href="#" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-teal-500">Cambiar Contraseña</a>
            <a @click.prevent="logout" href="#" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-teal-500">Cerrar sesión</a>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <div v-if="showChangePasswordModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">Cambiar Contraseña</h2>
        <form @submit.prevent="submitChangePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Contraseña Actual</label>
            <div class="relative">
              <input v-model="passwordForm.old_password" 
                     :type="showOldPassword ? 'text' : 'password'" 
                     required 
                     class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
              <button type="button" @click="showOldPassword = !showOldPassword" class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700 focus:outline-none">
                <span class="text-xl select-none">{{ showOldPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Nueva Contraseña</label>
            <div class="relative">
              <input v-model="passwordForm.new_password" 
                     :type="showNewPassword ? 'text' : 'password'" 
                     required 
                     class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
              <button type="button" @click="showNewPassword = !showNewPassword" class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700 focus:outline-none">
                <span class="text-xl select-none">{{ showNewPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">Confirmar Nueva Contraseña</label>
            <div class="relative">
              <input v-model="passwordForm.new_password_confirm" 
                     :type="showConfirmPassword ? 'text' : 'password'" 
                     required 
                     class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
              <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700 focus:outline-none">
                <span class="text-xl select-none">{{ showConfirmPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
          </div>

          <p v-if="passwordError" class="text-red-600 text-sm">{{ passwordError }}</p>
          <p v-if="passwordSuccess" class="text-green-600 text-sm">{{ passwordSuccess }}</p>

          <div class="space-y-2 pt-2">
            <button type="submit" class="w-full h-11 rounded-lg bg-teal-500 text-white font-semibold hover:bg-teal-600">Guardar Cambios</button>
            <button type="button" @click="showChangePasswordModal = false" class="w-full h-11 rounded-lg border hover:bg-slate-50">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axiosInstance from '@/api/axios.js';
import { useAuthStore } from '@/stores/auth.js';
import Shepherd from 'shepherd.js';
import 'shepherd.js/dist/css/shepherd.css';

const router = useRouter();
const authStore = useAuthStore();

const menuOpen = ref(false);
const perfilOpen = ref(false);

const user = ref({
  iniciales: '...',
  nombre: 'Cargando...',
  rol: ''
});

// --- Lógica para el Modal de Cambio de Contraseña ---
const showChangePasswordModal = ref(false);
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
});
const passwordError = ref('');
const passwordSuccess = ref('');

// --- Refs para controlar la visibilidad de las contraseñas ---
const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

function openChangePasswordModal() {
  perfilOpen.value = false; // Cierra el menú de perfil
  menuOpen.value = false;   // Cierra el menú móvil
  Object.assign(passwordForm, { old_password: '', new_password: '', new_password_confirm: '' });
  passwordError.value = '';
  passwordSuccess.value = '';
  
  // Resetea la visibilidad de los iconos
  showOldPassword.value = false;
  showNewPassword.value = false;
  showConfirmPassword.value = false;
  
  showChangePasswordModal.value = true;
}

async function submitChangePassword() {
  passwordError.value = '';
  passwordSuccess.value = '';

  if (passwordForm.new_password !== passwordForm.new_password_confirm) {
    passwordError.value = 'Las contraseñas nuevas no coinciden.';
    return;
  }
  
  try {
    // Llama al endpoint de la API que creamos en Django
    await axiosInstance.put('/users/change-password/', passwordForm);
    passwordSuccess.value = '¡Contraseña actualizada con éxito!';
    
    // Cierra el modal después de 2 segundos
    setTimeout(() => {
      showChangePasswordModal.value = false;
    }, 2000);
  } catch (e) {
    const errors = e.response?.data;
    if (errors) {
      // Muestra el error específico que envía el backend
      passwordError.value = Object.values(errors).flat().join(' ');
    } else {
      passwordError.value = 'Ocurrió un error inesperado.';
    }
  }
}

// --- Configuración de la Navegación y el Tutorial ---
const navItems = [
  { name: 'Inventario', path: '/dashboard/inventario' },
  { name: 'Importar', path: '/dashboard/inventario/importar' },
  { name: 'Proyecciones', path: '/dashboard/proyecciones' },
  { name: 'Reportes', path: '/dashboard/reportes' },
  { name: 'Usuarios', path: '/dashboard/usuarios' },
  { name: 'Configuración', path: '/dashboard/configuracion' }
];

const iniciarTutorial = (rol) => {
  const tour = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
      classes: 'shadow-md',
      scrollTo: true,
      cancelIcon: { enabled: true }
    }
  });

  const buttons = {
    back: { text: 'Atrás', action: tour.back, secondary: true },
    next: { text: 'Siguiente', action: tour.next },
    finish: { text: '¡Entendido!', action: tour.complete }
  };

  // El nuevo paso que le indica al usuario que cambie su contraseña
  const pasoCambiarClave = {
    title: '¡Importante! Primer Paso',
    text: 'Como tu cuenta fue creada por un administrador, te recomendamos cambiar tu contraseña temporal por una personal y segura.',
    attachTo: { element: '#menu-perfil', on: 'bottom' },
    buttons: [buttons.next] // Se quita el botón "Atrás" para que sea el primer paso real
  };

  switch (rol) {
    case 'admin':
      tour.addStep({
        title: '¡Bienvenido a INVEX!',
        text: 'Como <strong>Administrador</strong>, tienes acceso a todas las herramientas. Te daremos un breve recorrido.',
        buttons: [buttons.next]
      });
      tour.addStep(pasoCambiarClave); // Se añade el paso aquí
      tour.addStep({
        title: 'Gestión de Inventario',
        text: 'Aquí puedes ver y gestionar todos tus productos y su stock.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Administración de Usuarios',
        text: 'Aquí gestionas a tu equipo: agregas, eliminas y editas sus permisos.',
        attachTo: { element: '#nav-button-usuarios', on: 'bottom' },
        buttons: [buttons.back, buttons.finish]
      });
      break;
    
    case 'worker':
      tour.addStep({
        title: '¡Hola y bienvenido!',
        text: 'Tu rol es fundamental para mantener el inventario al día.',
        buttons: [buttons.next]
      });
      tour.addStep(pasoCambiarClave); // Se añade el paso aquí también
      tour.addStep({
        title: 'Tu Espacio de Trabajo',
        text: 'Desde <strong>Inventario</strong> podrás consultar y actualizar las cantidades de stock.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.finish]
      });
      break;
  }

  const onTourEnd = async () => {
    try {
      // Llama al endpoint correcto para marcar el tutorial como visto
      await axiosInstance.post('/users/marcar-tutorial-visto/');
    } catch (error) {
      console.error("Error al marcar el tutorial como visto:", error);
    }
  };
  
  tour.on('complete', onTourEnd);
  tour.on('cancel', onTourEnd);

  if (tour.steps.length > 0) {
    tour.start();
  }
};

// --- Funciones de Carga de Datos y Navegación ---
const fetchUserData = async () => {
  try {
    const response = await axiosInstance.get('/users/me/');
    const userData = response.data;
    const userRole = authStore.userRole || 'Invitado';

    user.value = {
      nombre: userData.nombre || 'Usuario',
      rol: userRole,
      iniciales: (userData.nombre || 'U').split(' ').map(n => n[0]).join('').toUpperCase(),
    };
    
    // Si el flag del backend es true, inicia el tutorial
    if (userData.mostrar_tutorial) {
      setTimeout(() => iniciarTutorial(userRole), 500);
    }

  } catch (error) {
    console.error("Error al obtener datos del usuario:", error);
    logout(); 
  }
};

onMounted(() => {
  fetchUserData();
});

const navigateTo = (path) => {
  menuOpen.value = false;
  router.push(path);
};

const logout = () => {
  perfilOpen.value = false;
  authStore.logout();
  router.push('/login');
};
</script>

<style>
/* Estilos para el layout, menú desplegable, etc. */
.layout-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f7fafc;
}
.main-nav {
  background-color: #0d9488;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.nav-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 4rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.main-content {
  flex-grow: 1;
  padding: 2rem;
  overflow-y: auto;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  width: 12rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  z-index: 50;
}
.mobile-menu {
  border-top: 1px solid #0f766e;
}
.mobile-profile {
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-top: 1px solid #0f766e;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Estilos para que Shepherd.js coincida con la paleta de colores de Invex */
.shepherd-arrow::before {
  background-color: #ffffff;
}
.shepherd-element {
  background: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb; /* Gray-200 */
}
.shepherd-header {
  padding: 1rem 1rem 0.75rem;
  background-color: #f9fafb; /* Gray-50 */
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
  border-bottom: 1px solid #e5e7eb; /* Gray-200 */
}
.shepherd-title {
  color: #0d9488; /* Teal-600 (color principal de tu marca) */
  font-weight: 700;
  font-size: 1.125rem;
}
.shepherd-cancel-icon {
  color: #9ca3af; /* Gray-400 */
  transition: color 0.2s;
}
.shepherd-cancel-icon:hover {
  color: #374151; /* Gray-700 */
}
.shepherd-text {
  padding: 1.25rem;
  color: #374151; /* Gray-700 */
  font-size: 0.95rem;
  line-height: 1.6;
}
.shepherd-text strong {
  color: #0f766e; /* Teal-700 */
}
.shepherd-footer {
  padding: 0 1.25rem 1.25rem;
}
.shepherd-button {
  background: #0d9488; /* Teal-600 */
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 0.375rem;
  font-weight: 600;
  transition: background-color 0.2s;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  border: none;
}
.shepherd-button:not(.shepherd-button-secondary):hover {
  background: #0f766e; /* Teal-700 */
}
.shepherd-button.shepherd-button-secondary {
  background: #e5e7eb; /* Gray-200 */
  color: #374151; /* Gray-700 */
}
.shepherd-button.shepherd-button-secondary:hover {
  background: #d1d5db; /* Gray-300 */
}
</style>