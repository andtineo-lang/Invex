<template>
  <div class="min-h-screen bg-green-50">
    <!-- Barra de navegación superior -->
    <nav class="bg-teal-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <h1 class="text-2xl font-bold text-white">INVEX</h1>

          <!-- Botón hamburguesa (móvil) -->
          <div class="md:hidden">
            <button 
              @click="menuOpen = !menuOpen"
              class="text-white hover:text-gray-200 focus:outline-none"
            >
              <svg v-if="!menuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Menú en escritorio -->
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

            <!-- Mini perfil -->
            <div class="relative" @click="perfilOpen = !perfilOpen">
              <div class="flex items-center space-x-2 cursor-pointer">
                <span class="bg-white text-teal-600 font-bold rounded-full px-3 py-1">
                  {{ user.iniciales }}
                </span>
                <span class="text-white font-medium hidden lg:block">{{ user.nombre }}</span>
              </div>

              <!-- Dropdown perfil -->
              <div v-if="perfilOpen" class="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-lg py-2 z-50">
                <p class="px-4 py-2 text-sm text-gray-700 border-b">{{ user.nombre }}</p>
                <button 
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Menú en móvil -->
      <div v-if="menuOpen" class="md:hidden bg-teal-700">
        <div class="px-4 py-3 space-y-2">
          <!-- Links de navegación -->
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

          <!-- Zona de perfil en el menú responsive -->
          <div class="mt-6 border-t border-teal-500 pt-4">
            <div class="flex items-center space-x-3">
              <!-- Avatar con iniciales -->
              <div class="w-10 h-10 flex items-center justify-center rounded-full bg-white text-teal-600 font-bold">
                {{ user.iniciales }}
              </div>
              <div class="flex flex-col">
                <!-- Nombre -->
                <span class="text-white font-semibold">{{ user.nombre }}</span>
                <!-- Rol -->
                <span class="text-sm text-gray-200 italic">{{ user.rol }}</span>
                <!-- Correo (opcional) -->
                <span class="text-xs text-gray-300">{{ user.correo }}</span>
              </div>
            </div>

            <!-- Botón cerrar sesión -->
            <button 
              @click="logout"
              class="w-full mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Aquí va el contenido dinámico -->
    <main class="p-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado de menú y perfil
const menuOpen = ref(false)
const perfilOpen = ref(false)

// Simulación usuario logueado (más adelante vendrá de tu backend/BD)
const user = ref({
  iniciales: 'JP',
  nombre: 'Juan Pérez',
  rol: 'Administrador', // <- este es el rol
  correo: 'juan.perez@empresa.com'
})

// --- CAMBIO AQUÍ ---
// Navegación (se añadió el prefijo /app a todas las rutas)
const navItems = [
  { name: 'Inventario', path: '/app/inventario' },
  { name: 'Importar', path: '/app/inventario/importar' },
  { name: 'Proyecciones', path: '/app/proyecciones' },
  { name: 'Reportes', path: '/app/reportes' },
  { name: 'Usuarios', path: '/app/usuarios' },
  { name: 'Configuracion', path: '/app/configuracion' }
]

const navigateTo = (path) => {
  menuOpen.value = false // Cierra el menú móvil al navegar
  perfilOpen.value = false // Cierra el menú de perfil
  router.push(path)
}

const logout = () => {
  perfilOpen.value = false
  // Aquí pondrías: localStorage.clear(), API logout, etc.
  router.push('/login')
}
</script>