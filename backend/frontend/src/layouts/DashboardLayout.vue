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
            <div
              @click="perfilOpen = !perfilOpen"
              class="flex items-center space-x-2 cursor-pointer"
            >
              <span
                class="bg-white text-teal-600 font-bold rounded-full h-8 w-8 flex items-center justify-center"
              >
                {{ user.iniciales }}
              </span>
            </div>
            <transition name="fade">
              <div v-if="perfilOpen" class="dropdown-menu">
                <div class="px-4 py-2 border-b">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {{ user.nombre }}
                  </p>
                  <p class="text-xs text-gray-500 capitalize">
                    {{ user.rol }}
                  </p>
                </div>

                <a
                  id="btn-cambiar-password"
                  @click.prevent="openChangePassword"
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Cambiar contraseña
                </a>

                <a
                  @click.prevent="logout"
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Cerrar sesión
                </a>
              </div>
            </transition>
          </div>

          <div class="md:hidden ml-4">
            <button
              @click="menuOpen = !menuOpen"
              class="text-white focus:outline-none"
            >
              <svg
                v-if="!menuOpen"
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16m-7 6h7"
                />
              </svg>
              <svg
                v-else
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
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
              $route.path.startsWith(item.path)
                ? 'bg-white text-teal-600'
                : 'text-white hover:bg-teal-500'
            ]"
          >
            {{ item.name }}
          </button>
        </div>
        <div class="mobile-profile">
          <div class="flex items-center px-5">
            <span
              class="bg-white text-teal-600 font-bold rounded-full h-10 w-10 flex items-center justify-center"
            >
              {{ user.iniciales }}
            </span>
            <div class="ml-3">
              <div class="text-base font-medium text-white">
                {{ user.nombre }}
              </div>
              <div class="text-sm font-medium text-teal-300 capitalize">
                {{ user.rol }}
              </div>
            </div>
          </div>
          <div class="mt-3 px-2 space-y-1">
            <a
              @click.prevent="openChangePassword"
              href="#"
              class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-teal-500"
            >
              Cambiar contraseña
            </a>
            <a
              @click.prevent="logout"
              href="#"
              class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-teal-500"
            >
              Cerrar sesión
            </a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Modal de cambio de contraseña -->
    <transition name="fade">
      <div
        v-if="showChangePassword"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      >
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold">Cambiar contraseña</h2>
            <button
              @click="closeChangePassword"
              class="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <form @submit.prevent="changePassword">
            <!-- Contraseña actual -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Contraseña actual
              </label>
              <div class="relative">
                <input
                  v-model="oldPassword"
                  :type="showOldPassword ? 'text' : 'password'"
                  class="w-full border rounded px-3 py-2 pr-10 focus:outline-none focus:ring focus:ring-teal-500"
                  required
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-gray-700"
                  @click="showOldPassword = !showOldPassword"
                >
                  <svg
                    v-if="!showOldPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.042-3.362M6.24 6.24A9.956 9.956 0 0112 5c4.477 0 8.268 2.943 9.542 7a9.97 9.97 0 01-4.043 5.197M15 12a3 3 0 00-3-3m0 0a3 3 0 00-2.121.879M12 9l-7 7"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Nueva contraseña -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nueva contraseña
              </label>
              <div class="relative">
                <input
                  v-model="newPassword"
                  :type="showNewPassword ? 'text' : 'password'"
                  class="w-full border rounded px-3 py-2 pr-10 focus:outline-none focus:ring focus:ring-teal-500"
                  required
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-gray-700"
                  @click="showNewPassword = !showNewPassword"
                >
                  <svg
                    v-if="!showNewPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.042-3.362M6.24 6.24A9.956 9.956 0 0112 5c4.477 0 8.268 2.943 9.542 7a9.97 9.97 0 01-4.043 5.197M15 12a3 3 0 00-3-3m0 0a3 3 0 00-2.121.879M12 9l-7 7"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Confirmar nueva contraseña -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Confirmar nueva contraseña
              </label>
              <div class="relative">
                <input
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="w-full border rounded px-3 py-2 pr-10 focus:outline-none focus:ring focus:ring-teal-500"
                  required
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-gray-700"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  <svg
                    v-if="!showConfirmPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.042-3.362M6.24 6.24A9.956 9.956 0 0112 5c4.477 0 8.268 2.943 9.542 7a9.97 9.97 0 01-4.043 5.197M15 12a3 3 0 00-3-3m0 0a3 3 0 00-2.121.879M12 9l-7 7"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Reglas de validación -->
            <ul class="text-xs mb-3">
              <li :class="passwordMinLengthOk ? 'text-green-600' : 'text-gray-500'">
                • Al menos 6 caracteres
              </li>
              <li :class="passwordMatchOk ? 'text-green-600' : 'text-gray-500'">
                • Coincide con la confirmación
              </li>
            </ul>

            <p v-if="changePasswordError" class="text-red-600 text-sm mb-3">
              {{ changePasswordError }}
            </p>
            <p v-if="changePasswordSuccess" class="text-green-600 text-sm mb-3">
              {{ changePasswordSuccess }}
            </p>

            <div class="flex justify-end space-x-2">
              <button
                type="button"
                class="px-4 py-2 rounded border border-gray-300 text-sm"
                @click="closeChangePassword"
                :disabled="changePasswordLoading"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="bg-teal-600 text-white px-4 py-2 rounded text-sm hover:bg-teal-700 transition"
                :disabled="changePasswordLoading"
              >
                {{ changePasswordLoading ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
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

// Modal cambio contraseña
const showChangePassword = ref(false);
const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const changePasswordError = ref('');
const changePasswordSuccess = ref('');
const changePasswordLoading = ref(false);

// visibilidad (ojitos)
const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

// validaciones de contraseña nueva
const passwordMinLengthOk = computed(() => newPassword.value.length >= 6);
const passwordMatchOk = computed(
  () => newPassword.value.length > 0 && newPassword.value === confirmPassword.value
);

// navItems base (se filtra según rol al cargar usuario)
const navItems = ref([
  { name: 'Inventario', path: '/dashboard/inventario', roles: ['admin', 'manager', 'worker'] },
  { name: 'Importar', path: '/dashboard/inventario/importar', roles: ['admin', 'manager', 'worker'] },
  { name: 'Proyecciones', path: '/dashboard/proyecciones', roles: ['admin', 'manager', 'worker', 'viewer'] },
  { name: 'Reportes', path: '/dashboard/reportes', roles: ['admin', 'manager', 'viewer'] },
  { name: 'Usuarios', path: '/dashboard/usuarios', roles: ['admin'] },
  { name: 'Configuración', path: '/dashboard/configuracion', roles: ['admin', 'manager'] }
]);

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

  switch (rol) {
    case 'admin':
      tour.addStep({
        title: '¡Bienvenido a INVEX!',
        text: 'Como <strong>Administrador</strong>, tienes acceso a todas las herramientas. Te daremos un breve recorrido.',
        buttons: [buttons.next]
      });
      tour.addStep({
        title: 'Gestión de Inventario',
        text: 'Aquí puedes ver y gestionar todos tus productos, revisar su stock actual, añadir nuevos artículos y editar los existentes.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Importar Datos',
        text: 'Usa esta potente herramienta para cargar masivamente tu inventario desde un archivo (como un Excel o CSV). ¡Ahorra horas de trabajo!',
        attachTo: { element: '#nav-button-importar', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Proyecciones de Demanda',
        text: 'Anticípate al futuro. En esta sección, el sistema analiza tus datos para predecir las ventas y ayudarte a evitar quiebres de stock.',
        attachTo: { element: '#nav-button-proyecciones', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Reportes Detallados',
        text: 'Genera informes clave sobre el rendimiento de tus productos, valor de inventario y mucho más para tomar decisiones informadas.',
        attachTo: { element: '#nav-button-reportes', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Administración de Usuarios',
        text: 'Aquí es donde gestionas a tu equipo. Puedes <strong>agregar, eliminar o buscar a tus trabajadores y editar sus permisos</strong>.',
        attachTo: { element: '#nav-button-usuarios', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Configuración del Sistema',
        text: 'Esta es una sección clave. Aquí puedes agregar <strong>Fechas Especiales</strong> (como Navidad o Cyber Day) para que el sistema ajuste las proyecciones automáticamente. También puedes definir parámetros avanzados como el <strong>Horizonte de Pronóstico</strong> y tu <strong>Nivel de Stock de Seguridad</strong>.',
        attachTo: { element: '#nav-button-configuración', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Cambia tu contraseña',
        text: 'Para mayor seguridad, te recomendamos cambiar tu contraseña inicial. Haz clic en tu avatar (arriba a la derecha) y luego en <strong>"Cambiar contraseña"</strong>.',
        attachTo: { element: '#btn-cambiar-password', on: 'left' },
        buttons: [buttons.back, buttons.finish]
      });
      break;

    case 'manager':
      tour.addStep({
        title: '¡Bienvenido a INVEX!',
        text: 'Como <strong>Manager</strong>, puedes analizar inventario, proyecciones y reportes para tomar decisiones.',
        buttons: [buttons.next]
      });
      tour.addStep({
        title: 'Inventario',
        text: 'Desde <strong>Inventario</strong> puedes revisar el stock disponible por producto y sus detalles.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Proyecciones',
        text: 'En <strong>Proyecciones</strong> verás la demanda estimada y el estado de cada producto (Comprar Ahora, Revisar, OK, etc.).',
        attachTo: { element: '#nav-button-proyecciones', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Reportes',
        text: 'La sección de <strong>Reportes</strong> te permite analizar ventas, proveedores y KPIs generales.',
        attachTo: { element: '#nav-button-reportes', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Cambia tu contraseña',
        text: 'Como eres un usuario nuevo, es importante que cambies la contraseña que te entregaron. Haz clic en tu avatar (arriba a la derecha) y luego en <strong>"Cambiar contraseña"</strong>.',
        attachTo: { element: '#btn-cambiar-password', on: 'left' },
        buttons: [buttons.back, buttons.finish]
      });
      break;

    case 'worker':
      tour.addStep({
        title: '¡Hola y bienvenido!',
        text: 'Tu rol es fundamental para mantener el inventario al día. Te mostraremos tus herramientas principales.',
        buttons: [buttons.next]
      });
      tour.addStep({
        title: 'Tu Espacio de Trabajo',
        text: 'Desde <strong>Inventario</strong> podrás consultar los productos y actualizar las cantidades de stock de forma rápida y sencilla.',
        attachTo: { element: '#nav-button-inventario', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Importación Rápida',
        text: 'Si necesitas registrar una gran cantidad de productos nuevos, aquí podrás hacerlo cargando un archivo.',
        attachTo: { element: '#nav-button-importar', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Cambia tu contraseña',
        text: 'Como eres un usuario nuevo, es muy importante que cambies la contraseña que te entregaron. Haz clic en tu avatar (arriba a la derecha) y luego en <strong>"Cambiar contraseña"</strong>.',
        attachTo: { element: '#btn-cambiar-password', on: 'left' },
        buttons: [buttons.back, buttons.finish]
      });
      break;

    case 'viewer':
    default:
      tour.addStep({
        title: 'Bienvenido a INVEX',
        text: 'Tienes acceso a las secciones de análisis y consulta. Te mostraremos los principales puntos.',
        buttons: [buttons.next]
      });
      tour.addStep({
        title: 'Proyecciones',
        text: 'En <strong>Proyecciones</strong> puedes revisar el estado proyectado del inventario y la demanda futura.',
        attachTo: { element: '#nav-button-proyecciones', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Reportes',
        text: 'En <strong>Reportes</strong> verás indicadores clave, gráficos y tablas para entender mejor el comportamiento del inventario.',
        attachTo: { element: '#nav-button-reportes', on: 'bottom' },
        buttons: [buttons.back, buttons.next]
      });
      tour.addStep({
        title: 'Cambia tu contraseña',
        text: 'Te recomendamos cambiar la contraseña inicial. Haz clic en tu avatar (arriba a la derecha) y luego en <strong>"Cambiar contraseña"</strong>.',
        attachTo: { element: '#btn-cambiar-password', on: 'left' },
        buttons: [buttons.back, buttons.finish]
      });
      break;
  }

  const onTourEnd = async () => {
    try {
      await axiosInstance.post('/auth/marcar-tutorial-visto/');
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

const fetchUserData = async () => {
  try {
    const response = await axiosInstance.get('/users/me/');
    const userData = response.data;

    const backendRole = userData.rol;
    const storedRole = localStorage.getItem('userRole');
    const userRole = backendRole || authStore.userRole || storedRole || 'viewer';

    authStore.userRole = userRole;
    localStorage.setItem('userRole', userRole);

    user.value = {
      nombre: userData.nombre || 'Usuario',
      rol: userRole,
      iniciales: (userData.nombre || 'U')
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
    };

    navItems.value = navItems.value.filter((item) => item.roles.includes(userRole));

    if (userData.mostrar_tutorial) {
      setTimeout(() => iniciarTutorial(userRole), 500);
    }
  } catch (error) {
    console.error('Error al obtener datos del usuario:', error);
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
  authStore.logout();
  router.push('/login');
};

const openChangePassword = () => {
  perfilOpen.value = false;
  menuOpen.value = false;
  changePasswordError.value = '';
  changePasswordSuccess.value = '';
  oldPassword.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  showOldPassword.value = false;
  showNewPassword.value = false;
  showConfirmPassword.value = false;
  showChangePassword.value = true;
};

const closeChangePassword = () => {
  if (!changePasswordLoading.value) {
    showChangePassword.value = false;
  }
};

const changePassword = async () => {
  changePasswordError.value = '';
  changePasswordSuccess.value = '';

  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    changePasswordError.value = 'Debe completar todos los campos.';
    return;
  }

  if (!passwordMinLengthOk.value) {
    changePasswordError.value = 'La nueva contraseña debe tener al menos 6 caracteres.';
    return;
  }

  if (!passwordMatchOk.value) {
    changePasswordError.value = 'Las contraseñas nuevas no coinciden.';
    return;
  }

  changePasswordLoading.value = true;
  try {
    const response = await axiosInstance.post('/auth/cambiar-password/', {
      old_password: oldPassword.value,
      new_password: newPassword.value
    });

    changePasswordSuccess.value =
      response.data.detail || 'Contraseña actualizada correctamente.';
    oldPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
  } catch (err) {
    changePasswordError.value =
      err?.response?.data?.detail || 'Ocurrió un error al cambiar la contraseña.';
  } finally {
    changePasswordLoading.value = false;
  }
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