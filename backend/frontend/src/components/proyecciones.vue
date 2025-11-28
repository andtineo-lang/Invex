<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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

    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="text-center mb-4">
        <h3 class="text-xl font-semibold text-gray-800">Histórico de Ventas Totales</h3>
        <p class="text-gray-500 text-sm sm:text-base">Unidades vendidas por mes (todos los productos)</p>
      </div>
      
      <div v-if="chartState.isLoading" class="h-80 flex items-center justify-center text-gray-500">
        Cargando datos del gráfico...
      </div>
      <div v-else-if="chartState.error" class="h-80 flex items-center justify-center text-red-600 bg-red-50 p-4 rounded-lg">
        Error al cargar los datos: {{ chartState.error }}
      </div>
      <div v-show="!chartState.isLoading && !chartState.error" ref="chartContainer" class="h-80 w-full"></div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div v-if="accionUrgente" class="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚠️ Acción Urgente</h3>
        <p class="text-sm opacity-90">Nivel de stock crítico para <strong>{{ accionUrgente.producto_nombre }}</strong>.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ accionUrgente.stock_actual }} u.</strong></p>
          <p>Cobertura: <strong>~{{ accionUrgente.semanas_cobertura.toFixed(1) }} semanas</strong></p>
        </div>
      </div>
      
      <div v-if="riesgoAgotamiento" class="bg-gradient-to-br from-yellow-400 to-orange-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚡ Riesgo de Agotamiento</h3>
        <p class="text-sm opacity-90">Revisar pronto el stock de <strong>{{ riesgoAgotamiento.producto_nombre }}</strong>.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ riesgoAgotamiento.stock_actual }} u.</strong></p>
          <p>Cobertura: <strong>~{{ riesgoAgotamiento.semanas_cobertura.toFixed(1) }} semanas</strong></p>
        </div>
      </div>

      <div v-if="oportunidadOptimizacion" class="bg-gradient-to-br from-pink-500 to-rose-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">💡 Oportunidad de Optimización</h3>
        <p class="text-sm opacity-90">Exceso de inventario en <strong>{{ oportunidadOptimizacion.producto_nombre }}</strong>.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ oportunidadOptimizacion.stock_actual }} u.</strong></p>
          <p>Cobertura: <strong>Más de {{ oportunidadOptimizacion.semanas_cobertura.toFixed(1) }} sem.</strong></p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado de Proyecciones</h3>
      </div>
      
      <div v-if="proyeccionesState.isLoading" class="p-8 text-center text-gray-500">Cargando proyecciones...</div>
      <div v-else-if="proyeccionesState.error" class="p-8 text-center text-red-600 bg-red-50">
        Error al cargar proyecciones: {{ proyeccionesState.error }}
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actual</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Demanda (sem.)</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cobertura (sem.)</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in proyeccionesState.data" :key="item.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ item.producto_nombre }}</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.stock_actual }} u.</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.demanda_semanal_proyectada }} u.</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.semanas_cobertura.toFixed(1) }}</td>
              <td class="px-4 py-3">
                <span :class="['px-2 py-1 text-xs font-semibold rounded-full', getEstadoClass(item.estado)]">
                  {{ getEstadoText(item.estado) }}
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
import { ref, onMounted, onUnmounted, reactive, computed } from 'vue';
import axiosInstance from '@/api/axios.js';

// --- LÓGICA DEL GRÁFICO (COMPLETA) ---
let chart = null;
const chartContainer = ref(null);
let LightweightCharts = null;

const loadLightweightCharts = () => {
  return new Promise((resolve, reject) => {
    if (window.LightweightCharts) {
      resolve(window.LightweightCharts);
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js';
    script.onload = () => resolve(window.LightweightCharts);
    script.onerror = () => reject(new Error('No se pudo cargar Lightweight Charts'));
    document.head.appendChild(script);
  });
};

const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};

const initChart = (data) => {
  if (!chartContainer.value || data.length === 0 || !LightweightCharts) return;
  chart = LightweightCharts.createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: 320,
    layout: { background: { color: '#ffffff' }, textColor: '#333' },
    grid: { vertLines: { color: '#f0f0f0' }, horzLines: { color: '#f0f0f0' } },
    timeScale: {
      borderColor: '#dddddd',
      tickMarkFormatter: (time) => {
        const date = new Date(time * 1000);
        return date.toLocaleDateString(undefined, { month: 'short', year: '2-digit', timeZone: 'UTC' });
      },
    },
    rightPriceScale: { borderColor: '#dddddd' },
  });
  const series = chart.addAreaSeries({
    topColor: 'rgba(34, 197, 94, 0.5)',
    bottomColor: 'rgba(34, 197, 94, 0.05)',
    lineColor: 'rgba(34, 197, 94, 1)',
    lineWidth: 2,
  });
  series.setData(data);
  chart.timeScale().fitContent();
  window.addEventListener('resize', resizeHandler);
};

// --- ESTADOS REACTIVOS ---
const chartState = reactive({
  data: [],
  isLoading: true,
  error: null,
});

const proyeccionesState = reactive({
  data: [],
  isLoading: true,
  error: null,
});

// --- PROPIEDADES COMPUTADAS PARA LAS TARJETAS DE RESUMEN ---
const accionUrgente = computed(() =>
  proyeccionesState.data.find(p => p.estado === 'Comprar Ahora')
);

const riesgoAgotamiento = computed(() =>
  proyeccionesState.data.find(p => p.estado === 'Revisar Pronto')
);

const oportunidadOptimizacion = computed(() => {
  const productosOK = proyeccionesState.data.filter(p => p.estado === 'Stock OK' && isFinite(p.semanas_cobertura));
  if (productosOK.length === 0) return null;
  return productosOK.sort((a, b) => b.semanas_cobertura - a.semanas_cobertura)[0];
});

// --- CICLO DE VIDA ---
onMounted(async () => {
  try {
    LightweightCharts = await loadLightweightCharts();

    const [ventasResponse, proyeccionesResponse] = await Promise.all([
      axiosInstance.get('/analytics/ventas-mensuales/'),
      axiosInstance.get('/productos/proyecciones/')
    ]);

    // Procesar datos del gráfico de ventas
    const chartApiData = ventasResponse.data;
    if (chartApiData && chartApiData.length > 0) {
      const formattedData = chartApiData.map(item => ({
        time: Date.UTC(
          parseInt(item.time.substring(0, 4)),
          parseInt(item.time.substring(5, 7)) - 1,
          parseInt(item.time.substring(8, 10))
        ) / 1000,
        value: item.value,
      }));
      chartState.data = formattedData;
      initChart(formattedData);
    } else {
      chartState.error = "No hay datos de ventas para mostrar todavía.";
    }

    // Procesar datos de la tabla de proyecciones
    const proyeccionesApiData = proyeccionesResponse.data;
     if (proyeccionesApiData && proyeccionesApiData.length > 0) {
        proyeccionesState.data = proyeccionesApiData;
    } else {
        proyeccionesState.error = "No se encontraron datos de proyecciones.";
    }

  } catch (err) {
    console.error("Error al cargar datos del dashboard:", err);
    const errorMessage = err.response?.data?.error || err.message || "Ocurrió un error desconocido.";
    chartState.error = errorMessage;
    proyeccionesState.error = errorMessage;
  } finally {
    chartState.isLoading = false;
    proyeccionesState.isLoading = false;
  }
});

onUnmounted(() => {
  if (chart) {
    chart.remove();
    chart = null;
  }
  window.removeEventListener('resize', resizeHandler);
});

// --- FUNCIONES HELPERS ---
const getEstadoClass = (estado) => {
  const classes = {
    'Comprar Ahora': 'bg-red-100 text-red-800',
    'Revisar Pronto': 'bg-yellow-100 text-yellow-800',
    'Stock OK': 'bg-green-100 text-green-800',
  };
  return classes[estado] || 'bg-gray-100 text-gray-800';
};

const getEstadoText = (estado) => {
  const textos = {
    'Comprar Ahora': '🚨 Urgente',
    'Revisar Pronto': '⚠️ Riesgo',
    'Stock OK': '✅ OK',
  };
  return textos[estado] || 'Normal';
};
</script>