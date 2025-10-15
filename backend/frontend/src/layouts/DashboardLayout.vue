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
                <a @click.prevent="logout" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Cerrar sesión</a>
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
            <a @click.prevent="logout" href="#" class="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-teal-500">Cerrar sesión</a>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
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
        buttons: [buttons.back, buttons.finish]
      });
      break;
  }

  const onTourEnd = async () => {
    try {
      await axiosInstance.post('/auth/marcar-tutorial-visto/');
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