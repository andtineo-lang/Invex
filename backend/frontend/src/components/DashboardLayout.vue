<template>
  <div v-if="user" class="min-h-screen bg-gray-100">
    <nav class="bg-teal-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <h1 class="text-2xl font-bold text-white flex-shrink-0">INVEX</h1>

          <div class="hidden md:flex items-center space-x-2">
            <button
              v-for="item in navItems"
              :key="item.name"
              @click="navigateTo(item.path)"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
                isActive(item.path)
                  ? 'bg-white text-teal-600 shadow-md'
                  : 'text-white hover:bg-teal-500 hover:bg-opacity-75'
              ]"
            >
              {{ item.name }}
            </button>
          </div>
          
          <div class="flex items-center">
            <div class="relative hidden md:block">
              <div @click="perfilOpen = !perfilOpen" class="flex items-center space-x-2 cursor-pointer p-2 rounded-full transition-colors hover:bg-teal-500">
                <span class="bg-white text-teal-600 font-bold rounded-full w-8 h-8 flex items-center justify-center text-sm">
                  {{ user.iniciales }}
                </span>
                <span class="text-white font-medium hidden lg:block">{{ user.nombre }}</span>
              </div>

              <div 
                v-if="perfilOpen" 
                v-click-outside="() => perfilOpen = false"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl py-2 z-50"
              >
                <div class="px-4 py-2 border-b">
                  <p class="text-sm font-semibold text-gray-800 truncate">{{ user.nombre }}</p>
                  <p class="text-xs text-gray-500 truncate">{{ user.email }}</p>
                </div>
                <button 
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>

            <button 
              @click="menuOpen = !menuOpen"
              class="md:hidden p-2 rounded-md text-white hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            >
              <MenuIcon v-if="!menuOpen" class="w-6 h-6" />
              <XIcon v-else class="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <transition 
        enter-active-class="duration-200 ease-out" 
        enter-from-class="opacity-0 scale-95" 
        enter-to-class="opacity-100 scale-100" 
        leave-active-class="duration-100 ease-in" 
        leave-from-class="opacity-100 scale-100" 
        leave-to-class="opacity-0 scale-95"
      >
        <div v-if="menuOpen" class="md:hidden bg-teal-700">
          <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <button
              v-for="item in navItems"
              :key="item.name"
              @click="navigateTo(item.path)"
              :class="[
                'block w-full text-left px-3 py-2 rounded-md text-base font-medium transition-colors',
                isActive(item.path)
                  ? 'bg-white text-teal-600'
                  : 'text-white hover:bg-teal-500 hover:bg-opacity-75'
              ]"
            >
              {{ item.name }}
            </button>
            <button 
              @click="logout"
              class="w-full text-center bg-red-600 hover:bg-red-700 text-white mt-2 py-2 px-4 rounded-md font-medium transition"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </transition>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center bg-gray-100">
    <p class="text-gray-500">Cargando...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { MenuIcon, XIcon } from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();

const menuOpen = ref(false);
const perfilOpen = ref(false);
const user = ref(null); 

const navItems = [
  { name: 'Inventario', path: '/dashboard/inventario' },
  { name: 'Proyecciones', path: '/dashboard/proyecciones' },
  { name: 'Reportes', path: '/dashboard/reportes' },
  { name: 'Configuración', path: '/dashboard/configuracion' }
];

const isActive = (path) => {
  return route.path.startsWith(path);
};

const navigateTo = (path) => {
  menuOpen.value = false;
  perfilOpen.value = false;
  router.push(path);
};

const logout = () => {
  localStorage.removeItem('authToken');
  if (axios.defaults.headers.common['Authorization']) {
    delete axios.defaults.headers.common['Authorization'];
  }
  router.push('/login');
};

const fetchUser = async () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    router.push('/login');
    return;
  }

  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

  try {
    const apiUrl = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000';
    const response = await axios.get(`${apiUrl}/api/users/me/`);
    const userData = response.data;
    
    user.value = {
      nombre: userData.nombre || userData.email.split('@')[0],
      email: userData.email,
      iniciales: (userData.nombre ? userData.nombre.charAt(0) : userData.email.charAt(0)).toUpperCase()
    };
  } catch (error) {
    console.error("Error al obtener datos del usuario:", error);
    logout();
  }
};

onMounted(fetchUser);
</script>

<style scoped>
.main-content {
  padding: 1.5rem;
  max-width: 80rem;
  margin: 0 auto;
}
</style>