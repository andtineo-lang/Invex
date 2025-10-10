<template>
  <div class="layout-container">
    <nav class="main-nav">
      <div class="nav-content">
        <div class="flex-shrink-0">
          <h1 class="text-2xl font-bold text-white">INVEX</h1>
        </div>

        <div class="hidden md:flex items-center space-x-2">
          <button
            v-for="item in navItems"
            :key="item.name"
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
          <div class="hidden md:block relative ml-4">
            <div @click="perfilOpen = !perfilOpen" class="flex items-center space-x-2 cursor-pointer">
              <span class="bg-white text-teal-600 font-bold rounded-full h-8 w-8 flex items-center justify-center">
                {{ user.iniciales }}
              </span>
            </div>
            <transition name="fade">
              <div v-if="perfilOpen" class="dropdown-menu">
                <p class="px-4 py-2 text-sm text-gray-700 border-b">{{ user.nombre }}</p>
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
              <div class="text-sm font-medium text-teal-200">{{ user.correo }}</div>
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const menuOpen = ref(false);
const perfilOpen = ref(false);

const user = ref({
  iniciales: 'JP',
  nombre: 'Juan Pérez',
  rol: 'Administrador',
  correo: 'juan.perez@empresa.com'
});

const navItems = [
  { name: 'Inventario', path: '/app/inventario' },
  { name: 'Importar', path: '/app/inventario/importar' },
  { name: 'Proyecciones', path: '/app/proyecciones' },
  { name: 'Reportes', path: '/app/reportes' },
  { name: 'Usuarios', path: '/app/usuarios' },
  { name: 'Configuración', path: '/app/configuracion' }
];

const navigateTo = (path) => {
  menuOpen.value = false;
  router.push(path);
};

const logout = () => {
  console.log('Cerrando sesión...');
  router.push('/login');
};
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  background-color: #f1f5f9;
}
.main-nav {
  background-color: #0d9488;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 4rem;
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1rem;
}
.main-content {
  padding: 2rem;
  max-width: 80rem;
  margin: 0 auto;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease-in-out;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.dropdown-menu {
  position: absolute; right: 0; margin-top: 0.5rem; width: 12rem;
  border-radius: 0.375rem;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
  padding: 0.25rem 0; background-color: white; z-index: 50;
}
.mobile-menu { background-color: #0f766e; }
.mobile-profile {
  padding-top: 1rem; padding-bottom: 0.75rem; border-top: 1px solid #115e59;
}
</style>