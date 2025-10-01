<template>
  <div class="min-h-screen bg-green-50">
    <!-- Barra de navegación superior -->
    <nav class="bg-teal-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <!-- Logo INVEX -->
          <div class="flex-shrink-0">
            <h1 class="text-2xl font-bold text-white">INVEX</h1>
          </div>
          
          <!-- Botones de navegación -->
          <div class="flex space-x-1">
            <button 
              v-for="item in navItems" 
              :key="item.name"
              @click="navigateTo(item.path)"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                item.path === 'proyecciones.vue'
                  ? 'bg-white text-teal-600' 
                  : 'text-white hover:bg-teal-500'
              ]"
            >
              {{ item.name }}
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido de Proyecciones -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-6">
        <div class="flex items-center space-x-2 mb-2">
          <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          <h2 class="text-3xl font-bold text-gray-900">
            Proyecciones de Stock (ASR Predictor)
          </h2>
        </div>
      </div>

      <!-- Gráfico de Proyección -->
      <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <div class="text-center mb-6">
          <div class="flex items-center justify-center space-x-2 mb-2">
            <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <h3 class="text-xl font-bold text-gray-900">
              Gráfico de Proyección Semanal de Stock
            </h3>
          </div>
          <p class="text-gray-600">
            Pronóstico de demanda potenciado por IA basado en tendencias estacionales
          </p>
        </div>

        <!-- Simulación de gráfico -->
        <div class="h-64 bg-gradient-to-br from-teal-50 to-blue-50 rounded-lg flex items-center justify-center border-2 border-dashed border-teal-200">
          <div class="text-center">
            <svg class="w-16 h-16 text-teal-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            <p class="text-gray-500 text-sm">Gráfico de proyección interactivo</p>
            <p class="text-gray-400 text-xs">Visualización de tendencias y predicciones</p>
          </div>
        </div>
      </div>

      <!-- Cards de Alertas -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Acción Urgente -->
        <div class="bg-gradient-to-br from-red-400 to-red-500 rounded-lg shadow-lg p-6 text-white">
          <div class="flex items-center space-x-2 mb-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <h3 class="text-lg font-bold">Acción Urgente Requerida</h3>
          </div>
          <div class="mb-4">
            <p class="font-semibold text-lg">Comprar en 5 días</p>
            <p class="text-sm opacity-90 mt-2">
              El inventario de Ramos de Rosas Rojas se agotará antes de la temporada de San Valentín
            </p>
          </div>
          <div class="flex items-center space-x-2 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <span>Stock actual: 45 unidades</span>
          </div>
          <div class="flex items-center space-x-2 text-sm mt-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <span>Demanda proyectada: 350 unidades</span>
          </div>
        </div>

        <!-- Alerta de Riesgo -->
        <div class="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg shadow-lg p-6 text-white">
          <div class="flex items-center space-x-2 mb-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <h3 class="text-lg font-bold">Alerta de Riesgo de Stock</h3>
          </div>
          <div class="mb-4">
            <p class="font-semibold text-lg">Riesgo de agotarse en 2 semanas</p>
            <p class="text-sm opacity-90 mt-2">
              Los disfraces de Halloween muestran señales de alta demanda, se recomienda orden inmediata de 200 unidades
            </p>
          </div>
          <div class="flex items-center space-x-2 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <span>Stock actual: 150 unidades</span>
          </div>
          <div class="flex items-center space-x-2 text-sm mt-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <span>Demanda semanal: 80 unidades</span>
          </div>
        </div>

        <!-- Oportunidad de Optimización -->
        <div class="bg-gradient-to-br from-pink-400 to-pink-500 rounded-lg shadow-lg p-6 text-white">
          <div class="flex items-center space-x-2 mb-3">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <h3 class="text-lg font-bold">Oportunidad de Optimización</h3>
          </div>
          <div class="mb-4">
            <p class="font-semibold text-lg">Reducir sobrestock</p>
            <p class="text-sm opacity-90 mt-2">
              Las decoraciones navideñas tienen exceso de inventario. Considerar precios promocionales
            </p>
          </div>
          <div class="flex items-center space-x-2 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <span>Stock actual: 850 unidades</span>
          </div>
          <div class="flex items-center space-x-2 text-sm mt-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <span>Demanda semanal: 120 unidades</span>
          </div>
        </div>
      </div>

      <!-- Tabla de Proyecciones Detalladas -->
      <div class="mt-6 bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-bold text-gray-900">Análisis Detallado de Proyecciones</h3>
        </div>
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Producto
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stock Actual
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Demanda Proyectada
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cobertura (semanas)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in proyeccionesData" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ item.producto }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ item.stockActual }} unidades
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ item.demandaProyectada }} unidades/semana
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ item.semanas }} semanas
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getEstadoClass(item.tipo)" class="px-2 py-1 text-xs font-semibold rounded-full">
                  {{ getEstadoText(item.tipo) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const navItems = [
  { name: 'Dashboard', path: 'dashboard.vue' },
  { name: 'Inventario', path: 'inventario.vue' },
  { name: 'Proyecciones', path: 'proyecciones.vue' },
  { name: 'Reportes', path: 'reportes.vue' },
  { name: 'Usuarios', path: 'usuarios.vue' },
  { name: 'Configuración', path: 'configuracion.vue' }
]

const proyeccionesData = ref([
  {
    id: 1,
    producto: 'Ramo de Rosas Rojas',
    stockActual: 45,
    demandaProyectada: 350,
    semanas: 2,
    tipo: 'urgente'
  },
  {
    id: 2,
    producto: 'Disfraz Halloween - Bruja',
    demandaProyectada: 80,
    stockActual: 150,
    semanas: 2,
    tipo: 'riesgo'
  },
  {
    id: 3,
    producto: 'Luces Árbol Navidad',
    stockActual: 850,
    demandaProyectada: 120,
    semanas: 4,
    tipo: 'optimizacion'
  }
])

const navigateTo = (path) => {
  // En una aplicación real con Vue Router:
  // this.$router.push({ name: path })
  console.log(`Navegando a: ${path}`)
  
  // Para desarrollo, puedes usar window.location
  // window.location.href = path
}

const getEstadoClass = (tipo) => {
  const classes = {
    'urgente': 'bg-red-100 text-red-800',
    'riesgo': 'bg-yellow-100 text-yellow-800',
    'optimizacion': 'bg-pink-100 text-pink-800'
  }
  return classes[tipo] || 'bg-gray-100 text-gray-800'
}

const getEstadoText = (tipo) => {
  const texts = {
    'urgente': '🚨 Urgente',
    'riesgo': '⚠️ Riesgo',
    'optimizacion': '💡 Optimizar'
  }
  return texts[tipo] || 'Normal'
}
</script>