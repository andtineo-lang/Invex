<template>
  <div class="min-h-screen bg-green-50">
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
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12" />
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
                <span class="bg-white text-teal-600 font-bold rounded-full px-3 py-1">
                  {{ user.iniciales }}
                </span>
                <span class="text-white font-medium hidden lg:block">{{ user.nombre }}</span>
              </div>

              <div v-if="perfilOpen" class="absolute right-0 mt-4 w-72 bg-teal-600 rounded-lg shadow-xl p-4 z-50 border border-teal-500">
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 flex items-center justify-center rounded-full bg-white text-teal-600 font-bold text-xl">
                    {{ user.iniciales }}
                  </div>
                  <div class="flex flex-col">
                    <span class="text-white font-semibold text-lg">{{ user.nombre }}</span>
                    <span class="text-sm text-teal-100 italic">{{ user.rol }}</span>
                    <span class="text-xs text-teal-200">{{ user.correo }}</span>
                  </div>
                </div>

                <button 
                  @click="logout"
                  class="w-full mt-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition"
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

          <div class="mt-6 border-t border-teal-500 pt-4">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 flex items-center justify-center rounded-full bg-white text-teal-600 font-bold">
                {{ user.iniciales }}
              </div>
              <div class="flex flex-col">
                <span class="text-white font-semibold">{{ user.nombre }}</span>
                <span class="text-sm text-gray-200 italic">{{ user.rol }}</span>
                <span class="text-xs text-gray-300">{{ user.correo }}</span>
              </div>
            </div>

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

// Simulación usuario logueado
const user = ref({
  iniciales: 'JP',
  nombre: 'Juan Pérez',
  rol: 'Administrador',
  correo: 'juan.perez@empresa.com'
})

// Navegación 
const navItems = [
  { name: 'Inventario', path: '/app/inventario' },
  { name: 'Importar', path: '/app/inventario/importar' },
  { name: 'Proyecciones', path: '/app/proyecciones' },
  { name: 'Reportes', path: '/app/reportes' },
  { name: 'Usuarios', path: '/app/usuarios' },
  { name: 'Configuracion', path: '/app/configuracion' }
]

const navigateTo = (path) => {
  menuOpen.value = false 
  perfilOpen.value = false 
  router.push(path)
}

const logout = () => {
  perfilOpen.value = false
  // Lógica de logout: localStorage.clear(), etc.
  router.push('/login')
}
</script>