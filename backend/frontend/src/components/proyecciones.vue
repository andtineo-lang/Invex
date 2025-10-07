<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Encabezado -->
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Proyecciones de Stock (ASR Predictor)</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        Pronóstico de demanda potenciado por IA, basado en patrones estacionales y ventas históricas.
      </p>
    </div>

    <!-- Gráfico de proyección -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="text-center mb-4">
        <h3 class="text-xl font-semibold text-gray-800">Gráfico de Proyección Semanal</h3>
        <p class="text-gray-500 text-sm sm:text-base">Visualización de tendencias de inventario y predicciones IA</p>
      </div>
      <div
        class="h-64 bg-gradient-to-br from-teal-50 to-blue-50 rounded-lg flex items-center justify-center border-2 border-dashed border-teal-200"
      >
        <div class="text-center">
          <svg class="w-16 h-16 text-teal-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
          <p class="text-gray-500 text-sm">Gráfico interactivo próximamente</p>
        </div>
      </div>
    </div>

    <!-- Alertas de estado -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <!-- Urgente -->
      <div class="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚠️ Acción Urgente</h3>
        <p class="text-sm opacity-90">Comprar en 5 días — <strong>Rosas Rojas</strong> bajo nivel de stock.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>45 unidades</strong></p>
          <p>Demanda proyectada: <strong>350 unidades</strong></p>
        </div>
      </div>

      <!-- Riesgo -->
      <div class="bg-gradient-to-br from-yellow-400 to-orange-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚡ Riesgo de Agotamiento</h3>
        <p class="text-sm opacity-90">Disfraces de Halloween con alta demanda semanal.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>150 unidades</strong></p>
          <p>Demanda semanal: <strong>80 unidades</strong></p>
        </div>
      </div>

      <!-- Oportunidad -->
      <div class="bg-gradient-to-br from-pink-500 to-rose-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">💡 Oportunidad de Optimización</h3>
        <p class="text-sm opacity-90">Exceso de inventario — luces navideñas.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>850 unidades</strong></p>
          <p>Demanda semanal: <strong>120 unidades</strong></p>
        </div>
      </div>
    </div>

    <!-- Tabla detallada -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado de Proyecciones</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actual</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Demanda Proyectada</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cobertura (semanas)</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in proyeccionesData" :key="item.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ item.producto }}</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.stockActual }} u.</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.demandaProyectada }} u/sem</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.semanas }}</td>
              <td class="px-4 py-3">
                <span
                  :class="[ 'px-2 py-1 text-xs font-semibold rounded-full', getEstadoClass(item.tipo) ]"
                >
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

// Datos simulados (como si vinieran de BD)
const proyeccionesData = ref([
  { id: 1, producto: 'Ramos de Rosas Rojas', stockActual: 45, demandaProyectada: 350, semanas: 2, tipo: 'urgente' },
  { id: 2, producto: 'Disfraz Halloween - Bruja', stockActual: 150, demandaProyectada: 80, semanas: 3, tipo: 'riesgo' },
  { id: 3, producto: 'Luces Árbol Navidad', stockActual: 850, demandaProyectada: 120, semanas: 5, tipo: 'optimizacion' }
])

const getEstadoClass = (tipo) => {
  const classes = {
    urgente: 'bg-red-100 text-red-800',
    riesgo: 'bg-yellow-100 text-yellow-800',
    optimizacion: 'bg-pink-100 text-pink-800'
  }
  return classes[tipo] || 'bg-gray-100 text-gray-800'
}

const getEstadoText = (tipo) => {
  const textos = {
    urgente: '🚨 Urgente',
    riesgo: '⚠️ Riesgo',
    optimizacion: '💡 Optimizar'
  }
  return textos[tipo] || 'Normal'
}
</script>
