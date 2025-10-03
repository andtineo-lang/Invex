<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-2">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
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
      <div
        class="h-64 bg-gradient-to-br from-teal-50 to-blue-50 rounded-lg flex items-center justify-center border-2 border-dashed border-teal-200">
        <div class="text-center">
          <svg class="w-16 h-16 text-teal-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
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
        <h3 class="text-lg font-bold mb-2">🚨 Acción Urgente</h3>
        <p class="font-semibold text-lg">Comprar en 5 días</p>
        <p class="text-sm opacity-90 mt-2">
          El inventario de Ramos de Rosas Rojas se agotará antes de la temporada de San Valentín
        </p>
      </div>

      <!-- Alerta de Riesgo -->
      <div class="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-bold mb-2">⚠️ Riesgo de Stock</h3>
        <p class="font-semibold text-lg">Posible agotamiento en 2 semanas</p>
        <p class="text-sm opacity-90 mt-2">
          Los disfraces de Halloween muestran señales de alta demanda.
        </p>
      </div>

      <!-- Oportunidad de Optimización -->
      <div class="bg-gradient-to-br from-pink-400 to-pink-500 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-bold mb-2">💡 Oportunidad de Optimización</h3>
        <p class="font-semibold text-lg">Reducir sobrestock</p>
        <p class="text-sm opacity-90 mt-2">
          Las decoraciones navideñas tienen exceso de inventario. Considerar promociones.
        </p>
      </div>
    </div>

    <!-- Tabla de Proyecciones Detalladas -->
    <div class="mt-6 bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado</h3>
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actual</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Demanda Proyectada</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cobertura</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in proyeccionesData" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ item.producto }}</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ item.stockActual }} unidades</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ item.demandaProyectada }} / semana</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ item.semanas }} semanas</td>
            <td class="px-6 py-4">
              <span :class="getEstadoClass(item.tipo)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ getEstadoText(item.tipo) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const proyeccionesData = ref([
  { id: 1, producto: 'Ramo de Rosas Rojas', stockActual: 45, demandaProyectada: 350, semanas: 2, tipo: 'urgente' },
  { id: 2, producto: 'Disfraz Halloween - Bruja', stockActual: 150, demandaProyectada: 80, semanas: 2, tipo: 'riesgo' },
  { id: 3, producto: 'Luces Árbol Navidad', stockActual: 850, demandaProyectada: 120, semanas: 4, tipo: 'optimizacion' }
])

const getEstadoClass = (tipo) => {
  return {
    urgente: 'bg-red-100 text-red-800',
    riesgo: 'bg-yellow-100 text-yellow-800',
    optimizacion: 'bg-pink-100 text-pink-800'
  }[tipo] || 'bg-gray-100 text-gray-800'
}

const getEstadoText = (tipo) => {
  return {
    urgente: '🚨 Urgente',
    riesgo: '⚠️ Riesgo',
    optimizacion: '💡 Optimizar'
  }[tipo] || 'Normal'
}
</script>
