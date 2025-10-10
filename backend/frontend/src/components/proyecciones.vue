<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Proyecciones de Stock (ASR Predictor)</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        Pronóstico de demanda potenciado por IA, basado en patrones estacionales y ventas históricas.
      </p>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="text-center mb-4">
        <h3 class="text-xl font-semibold text-gray-800">Gráfico de Proyección Semanal</h3>
        <p class="text-gray-500 text-sm sm:text-base">Visualización de tendencias de inventario y predicciones IA</p>
      </div>
      <div id="chart">
        <VueApexCharts
          type="bar"
          height="300"
          :options="chartData.chartOptions"
          :series="chartData.series"
        ></VueApexCharts>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div v-if="alertaUrgente" class="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚠️ Acción Urgente</h3>
        <p class="text-sm opacity-90">Comprar pronto — <strong>{{ alertaUrgente.producto }}</strong> tiene bajo nivel de
          stock.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ alertaUrgente.stockActual }} unidades</strong></p>
          <p>Demanda proyectada: <strong>{{ alertaUrgente.demandaProyectada }} u/sem</strong></p>
        </div>
      </div>

      <div v-if="alertaRiesgo" class="bg-gradient-to-br from-yellow-400 to-orange-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚡ Riesgo de Agotamiento</h3>
        <p class="text-sm opacity-90"><strong>{{ alertaRiesgo.producto }}</strong> con alta demanda semanal.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ alertaRiesgo.stockActual }} unidades</strong></p>
          <p>Demanda semanal: <strong>{{ alertaRiesgo.demandaProyectada }} u/sem</strong></p>
        </div>
      </div>

      <div v-if="alertaOptimizacion" class="bg-gradient-to-br from-pink-500 to-rose-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">💡 Oportunidad de Optimización</h3>
        <p class="text-sm opacity-90">Exceso de inventario en <strong>{{ alertaOptimizacion.producto }}</strong>.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ alertaOptimizacion.stockActual }} unidades</strong></p>
          <p>Demanda semanal: <strong>{{ alertaOptimizacion.demandaProyectada }} u/sem</strong></p>
        </div>
      </div>
    </div>

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
            <tr v-for="item in proyeccionesProcesadas" :key="item.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ item.producto }}</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.stockActual }} u.</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.demandaProyectada }} u/sem</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.semanasCobertura.toFixed(1) }}</td>
              <td class="px-4 py-3">
                <span :class="['px-2 py-1 text-xs font-semibold rounded-full', getEstadoClass(item.tipo)]">
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
import { ref, computed } from 'vue'
import VueApexCharts from 'vue3-apexcharts'

// --- DATOS CRUDOS ---
// Esto es lo único que necesitarás reemplazar con los datos de tu API/BD.
const proyeccionesData = ref([
  { id: 1, producto: 'Rosas Rojas', stockActual: 45, demandaProyectada: 30 },
  { id: 2, producto: 'Disfraz Halloween', stockActual: 150, demandaProyectada: 80 },
  { id: 3, producto: 'Luces Navidad', stockActual: 850, demandaProyectada: 120 },
  { id: 4, producto: 'Globos Cumpleaños', stockActual: 400, demandaProyectada: 50 },
  { id: 5, producto: 'Velas Aromáticas', stockActual: 200, demandaProyectada: 0 },
])

// --- LÓGICA DE PROCESAMIENTO ---
// Propiedad computada que calcula semanas de cobertura y asigna un tipo a cada producto.
const proyeccionesProcesadas = computed(() => {
  return proyeccionesData.value.map(item => {
    const semanasCobertura = item.demandaProyectada > 0 ? item.stockActual / item.demandaProyectada : Infinity;
    let tipo = 'normal';
    if (semanasCobertura < 2) {
      tipo = 'urgente';
    } else if (semanasCobertura < 4) {
      tipo = 'riesgo';
    } else if (semanasCobertura > 8 && semanasCobertura !== Infinity) {
      tipo = 'optimizacion';
    }
    return {
      ...item,
      semanasCobertura,
      tipo
    }
  });
});

// --- LÓGICA PARA LAS ALERTAS ---
// Propiedades computadas que buscan el primer item que coincida con cada estado.
const alertaUrgente = computed(() => proyeccionesProcesadas.value.find(p => p.tipo === 'urgente'));
const alertaRiesgo = computed(() => proyeccionesProcesadas.value.find(p => p.tipo === 'riesgo'));
const alertaOptimizacion = computed(() => proyeccionesProcesadas.value.find(p => p.tipo === 'optimizacion'));


// --- DATOS PARA EL GRÁFICO ---
// Prepara los datos para ApexCharts de forma reactiva
const chartData = computed(() => {
  const labels = proyeccionesProcesadas.value.map(p => p.producto);
  const stockSeries = proyeccionesProcesadas.value.map(p => p.stockActual);
  const demandaSeries = proyeccionesProcesadas.value.map(p => p.demandaProyectada);

  return {
    series: [
      { name: 'Stock Actual', data: stockSeries },
      { name: 'Demanda Semanal', data: demandaSeries }
    ],
    chartOptions: {
      chart: {
        type: 'bar',
        height: 350,
        toolbar: { show: false }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          endingShape: 'rounded'
        },
      },
      dataLabels: { enabled: false },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: labels,
      },
      yaxis: {
        title: { text: 'Unidades' }
      },
      fill: { opacity: 1 },
      tooltip: {
        y: {
          formatter: (val) => `${val} unidades`
        }
      },
      colors: ['#0d9488', '#f59e0b']
    }
  }
});


// --- FUNCIONES AUXILIARES DE ESTILO ---
const getEstadoClass = (tipo) => {
  const classes = {
    urgente: 'bg-red-100 text-red-800',
    riesgo: 'bg-yellow-100 text-yellow-800',
    optimizacion: 'bg-pink-100 text-pink-800',
    normal: 'bg-green-100 text-green-800'
  }
  return classes[tipo] || 'bg-gray-100 text-gray-800'
}

const getEstadoText = (tipo) => {
  const textos = {
    urgente: '🚨 Urgente',
    riesgo: '⚠️ Riesgo',
    optimizacion: '💡 Optimizar',
    normal: '✅ Óptimo'
  }
  return textos[tipo] || 'Normal'
}
</script>

<style scoped>
/* Puedes añadir estilos específicos para este componente aquí si lo necesitas */
</style>