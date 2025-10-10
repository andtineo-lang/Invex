<template>
  <div v-if="user" class="min-h-screen bg-gray-100">
    <nav class="bg-teal-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <h1 class="text-2xl font-bold text-white">INVEX</h1>

          <div class="md:hidden">
            <button 
              @click="menuOpen = !menuOpen"
              class="text-white hover:text-gray-200 focus:outline-none"
            >
              <svg v-if="!menuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="hidden md:flex items-center space-x-4">
            <button
              v-for="item in navItems"
              :key="item.name"
              @click="navigateTo(item.path)"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                $route.path === item.path
                  ? 'bg-white text-teal-600 shadow-md'
                  : 'text-white hover:bg-teal-500'
              ]"
            >
              {{ item.name }}
            </button>

            <div class="relative">
              <div @click="perfilOpen = !perfilOpen" class="flex items-center space-x-2 cursor-pointer">
                <span class="bg-white text-teal-600 font-bold rounded-full px-3 py-1 text-sm">
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
                  <p class="text-sm font-semibold text-gray-800">{{ user.nombre }}</p>
                  <p class="text-xs text-gray-500">{{ user.email }}</p>
                </div>
                <button 
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="menuOpen" class="md:hidden bg-teal-700">
        <div class="px-4 py-3 space-y-2">
          <button
            v-for="item in navItems"
            :key="item.name"
            @click="navigateTo(item.path)"
            :class="[
              'block w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              $route.path === item.path
                ? 'bg-white text-teal-600'
                : 'text-white hover:bg-teal-500'
            ]"
          >
            {{ item.name }}
          </button>
          
          <div class="border-t border-teal-500 mt-4 pt-4">
            <button 
              @click="logout"
              class="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="p-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

// Estado de menús
const menuOpen = ref(false);
const perfilOpen = ref(false);

// El usuario empieza como nulo hasta que lo traemos de la API
const user = ref(null);

// Hook que se ejecuta cuando el componente se monta en la pantalla
onMounted(async () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    router.push('/login');
    return;
  }

  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

  try {
    // ❗ DEBERÁS CREAR ESTE ENDPOINT EN TU BACKEND
    // (una vista que devuelve los datos del usuario actual)
    const response = await axios.get('http://127.0.0.1:8000/api/users/me/');
    
    const userData = response.data;
    user.value = {
      nombre: userData.nombre || userData.email.split('@')[0],
      email: userData.email,
      iniciales: (userData.nombre ? userData.nombre.charAt(0) : userData.email.charAt(0)).toUpperCase()
    };

  } catch (error) {
    console.error("Error al obtener datos del usuario:", error);
    // Si el token es inválido o expiró, cerramos sesión
    logout();
  }
});

// Opciones de navegación
const navItems = [
  { name: 'Inventario', path: '/dashboard/inventario' },
  { name: 'Proyecciones', path: '/dashboard/proyecciones' },
  { name: 'Reportes', path: '/dashboard/reportes' },
  { name: 'Configuración', path: '/dashboard/configuracion' }
];

const navigateTo = (path) => {
  menuOpen.value = false;
  perfilOpen.value = false;
  router.push(path);
};

// Función de Logout funcional
const logout = () => {
  localStorage.removeItem('authToken');
  delete axios.defaults.headers.common['Authorization'];
  router.push('/login');
};
</script>

<style scoped>
/* Puedes añadir estilos específicos para el layout aquí si lo necesitas */
</style>