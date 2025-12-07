<template>
  <div class="layout-container">
    <nav class="main-nav">
      <div class="nav-content">
        <div class="flex-shrink-0">
          <h1 class="text-2xl font-bold text-white">INVEX</h1>
        </div>

        <div id="nav-principal" class="hidden md:flex items-center space-x-2">
          <button
            v-for="item in filteredNavItems"
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
              <span v-if="!isFreeUser" class="bg-purple-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full mr-2">PRO</span>
              
              <span class="bg-white text-teal-600 font-bold rounded-full h-8 w-8 flex items-center justify-center">
                {{ user.iniciales }}
              </span>
            </div>
            
            <transition name="fade">
              <div v-if="perfilOpen" class="dropdown-menu w-64"> 
                <div class="px-4 py-3 border-b bg-gray-50">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ user.nombre }}</p>
                  <p class="text-xs text-gray-500 capitalize">{{ user.rol }}</p>
                </div>

                <div class="px-4 py-3 border-b">
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-gray-700">
                      {{ isFreeUser ? 'Plan Inicial' : 'Plan PRO ⚡' }}
                    </span>
                    <span v-if="isFreeUser" class="text-xs text-gray-500">{{ totalProductos }}/50</span>
                  </div>
                  
                  <div v-if="isFreeUser">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        class="bg-teal-500 h-2 rounded-full transition-all duration-500" 
                        :style="{ width: porcentajeUso + '%' }"
                        :class="{'bg-red-500': porcentajeUso >= 90}"
                      ></div>
                    </div>
                    
                    <router-link 
                      v-if="porcentajeUso >= 80 && isAdmin"
                      to="/precios" 
                      class="block mt-2 text-center text-xs text-teal-600 font-bold hover:underline"
                    >
                      Actualizar Plan &rarr;
                    </router-link>
                    
                    <p v-else-if="porcentajeUso >= 80" class="mt-2 text-center text-xs text-gray-400">
                      Contacta al admin para aumentar capacidad.
                    </p>
                  </div>
                  <div v-else class="text-xs text-purple-600 font-medium">
                    IA Activa y Productos Ilimitados
                  </div>
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
            v-for="item in filteredNavItems"
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
          <div class="px-5 mb-4"> 
             <div class="bg-teal-700 rounded p-3 text-white text-sm">
                <div class="flex justify-between mb-1">
                  <span class="font-bold">{{ isFreeUser ? 'Plan Inicial' : 'Plan PRO' }}</span>
                  <span v-if="isFreeUser">{{ totalProductos }}/50</span>
                </div>
                <div v-if="isFreeUser" class="w-full bg-teal-900 rounded-full h-2">
                  <div class="bg-white h-2 rounded-full" :style="{ width: porcentajeUso + '%' }"></div>
                </div>
             </div>
          </div>

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
              <input v-model="passwordForm.old_password" :type="showOldPassword ? 'text' : 'password'" required class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
              <button type="button" @click="showOldPassword = !showOldPassword" class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700 focus:outline-none">
                <span class="text-xl select-none">{{ showOldPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Nueva Contraseña</label>
            <div class="relative">
              <input v-model="passwordForm.new_password" :type="showNewPassword ? 'text' : 'password'" required class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
              <button type="button" @click="showNewPassword = !showNewPassword" class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700 focus:outline-none">
                <span class="text-xl select-none">{{ showNewPassword ? '🙈' : '👁️' }}</span>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Confirmar Nueva Contraseña</label>
            <div class="relative">
              <input v-model="passwordForm.new_password_confirm" :type="showConfirmPassword ? 'text' : 'password'" required class="w-full border rounded px-3 py-2 pr-10 focus:ring-2 focus:ring-teal-400" />
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
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axiosInstance from '@/api/axios.js';
import { useAuthStore } from '@/stores/auth.js';
import Shepherd from 'shepherd.js';
import 'shepherd.js/dist/css/shepherd.css';

const router = useRouter();
const authStore = useAuthStore();

// --- Estados de Interfaz ---
const menuOpen = ref(false);
const perfilOpen = ref(false);
const totalProductos = ref(0);

const user = ref({
  iniciales: '...',
  nombre: 'Cargando...',
  rol: ''
});

// --- Lógica del Plan (Free vs Pro) ---
const isFreeUser = computed(() => authStore.user?.subscription_status === 'free');

// CAMBIO: Detectar si es Admin para mostrar botón de pago
const isAdmin = computed(() => authStore.userRole === 'admin');

const porcentajeUso = computed(() => {
  if (!isFreeUser.value) return 0;
  // CAMBIO: Límite 50
  return Math.min((totalProductos.value / 50) * 100, 100); 
});

// --- Lógica para el Modal de Cambio de Contraseña ---
const showChangePasswordModal = ref(false);
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
});
const passwordError = ref('');
const passwordSuccess = ref('');
const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

function openChangePasswordModal() {
  perfilOpen.value = false;
  menuOpen.value = false;
  Object.assign(passwordForm, {
    old_password: '',
    new_password: '',
    new_password_confirm: ''
  });
  passwordError.value = '';
  passwordSuccess.value = '';
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
    await axiosInstance.put('/users/change-password/', passwordForm);
    passwordSuccess.value = '¡Contraseña actualizada con éxito!';
    Object.assign(passwordForm, {
      old_password: '',
      new_password: '',
      new_password_confirm: ''
    });
    setTimeout(() => {
      showChangePasswordModal.value = false;
      passwordSuccess.value = ''; 
    }, 2000);

  } catch (e) {
    const errors = e.response?.data;
    if (errors) {
      const listaDeMensajes = Object.values(errors).flat();
      passwordError.value = listaDeMensajes.join(' '); 
    } else {
      passwordError.value = 'Ocurrió un error inesperado al conectar con el servidor.';
    }
  }
}

// --- CONFIGURACIÓN DE NAVEGACIÓN ---
const navItems = [
  { 
    name: 'Inventario', 
    path: '/dashboard/inventario', 
    allowedRoles: ['admin', 'manager', 'worker'] 
  },
  { 
    name: 'Importar', 
    path: '/dashboard/inventario/importar', 
    allowedRoles: ['admin', 'manager'] 
  },
  { 
    name: 'Proyecciones', 
    path: '/dashboard/proyecciones', 
    allowedRoles: ['admin', 'manager', 'viewer'] 
  },
  { 
    name: 'Reportes', 
    path: '/dashboard/reportes', 
    allowedRoles: ['admin', 'manager', 'viewer'] 
  },
  { 
    name: 'Usuarios', 
    path: '/dashboard/usuarios', 
    allowedRoles: ['admin'] 
  },
  { 
    name: 'Configuración', 
    path: '/dashboard/configuracion', 
    allowedRoles: ['admin', 'manager'] 
  }
];

const currentRole = computed(() => {
  const fromStore = authStore.userRole || authStore.user?.rol;
  const fromUser = user.value.rol;
  return ((fromStore || fromUser || 'viewer') + '').toLowerCase().trim();
});

const filteredNavItems = computed(() => {
  const myRole = currentRole.value;
  return navItems.filter(item => item.allowedRoles.includes(myRole));
});

// --- Lógica del Tutorial (Shepherd.js) ---
const iniciarTutorial = rol => {
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

  const pasoCambiarClave = {
    title: '¡Importante! Primer Paso',
    text: 'Como tu cuenta fue creada por un administrador, te recomendamos cambiar tu contraseña temporal por una personal y segura.',
    attachTo: { element: '#menu-perfil', on: 'bottom' },
    buttons: [buttons.next]
  };

  switch (rol) {
    case 'admin':
      tour.addStep({
        title: '¡Bienvenido a INVEX!',
        text: 'Como <strong>Administrador</strong>, tienes acceso a todas las herramientas.',
        buttons: [buttons.next]
      });
      tour.addStep(pasoCambiarClave);
      tour.addStep({
        title: 'Gestión de Inventario',
        text: 'Aquí gestionas tus productos.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Administración de Usuarios',
        text: 'Agrega o elimina miembros de tu equipo aquí.',
        attachTo: { element: '#nav-button-usuarios', on: 'bottom' },
        buttons: [buttons.back, buttons.finish]
      });
      break;

    case 'manager':
      tour.addStep({
        title: '¡Bienvenido Manager!',
        text: 'Tienes control sobre inventario, reportes y configuración.',
        buttons: [buttons.next]
      });
      tour.addStep(pasoCambiarClave);
      tour.addStep({
        title: 'Reportes y Proyecciones',
        text: 'Analiza el rendimiento de la empresa aquí.',
        attachTo: { element: '#nav-button-reportes', on: 'bottom' },
        buttons: [buttons.back, buttons.finish]
      });
      break;

    case 'worker':
      tour.addStep({
        title: '¡Hola y bienvenido!',
        text: 'Tu rol es fundamental para mantener el inventario al día.',
        buttons: [buttons.next]
      });
      tour.addStep(pasoCambiarClave);
      tour.addStep({
        title: 'Tu Espacio de Trabajo',
        text: 'Desde <strong>Inventario</strong> podrás actualizar el stock.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.finish]
      });
      break;
  }

  const onTourEnd = async () => {
    try {
      await axiosInstance.post('/users/marcar-tutorial-visto/');
    } catch (error) {
      console.error('Error al marcar el tutorial como visto:', error);
    }
  };

  tour.on('complete', onTourEnd);
  tour.on('cancel', onTourEnd);

  if (tour.steps.length > 0) {
    tour.start();
  }
};

// --- Carga de Datos Inicial ---
const fetchUserData = async () => {
  try {
    const response = await axiosInstance.get('/users/me/');
    const userData = response.data;

    // 1. Guardar en Store
    authStore.user = userData;

    // 2. Determinar Rol
    const userRole = (userData.rol || 'invitado').toLowerCase();

    // 3. Actualizar estado local
    user.value = {
      nombre: userData.nombre || 'Usuario',
      rol: userRole,
      iniciales: (userData.nombre || 'U')
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
    };

    // 4. Iniciar Tutorial
    if (userData.mostrar_tutorial) {
      setTimeout(() => iniciarTutorial(userRole), 500);
    }

    // 5. Verificar límites (Solo si es Free)
    if (userData.subscription_status === 'free') {
      try {
        const resProductos = await axiosInstance.get('/productos/?limit=1');
        totalProductos.value = resProductos.data.count || resProductos.data.results?.length || 0;
      } catch (err) {
        console.error("Error cargando conteo de productos", err);
      }
    }
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
    logout();
  }
};

onMounted(() => {
  fetchUserData();
});

const navigateTo = path => {
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
/* Estilos Layout */
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

/* Shepherd Styles */
.shepherd-arrow::before { background-color: #ffffff; }
.shepherd-element {
  background: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}
.shepherd-header {
  padding: 1rem 1rem 0.75rem;
  background-color: #f9fafb;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}
.shepherd-title {
  color: #0d9488;
  font-weight: 700;
  font-size: 1.125rem;
}
.shepherd-cancel-icon { color: #9ca3af; transition: color 0.2s; }
.shepherd-cancel-icon:hover { color: #374151; }
.shepherd-text {
  padding: 1.25rem;
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.6;
}
.shepherd-text strong { color: #0f766e; }
.shepherd-footer { padding: 0 1.25rem 1.25rem; }
.shepherd-button {
  background: #0d9488;
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
.shepherd-button:not(.shepherd-button-secondary):hover { background: #0f766e; }
.shepherd-button.shepherd-button-secondary { background: #e5e7eb; color: #374151; }
.shepherd-button.shepherd-button-secondary:hover { background: #d1d5db; }
</style>