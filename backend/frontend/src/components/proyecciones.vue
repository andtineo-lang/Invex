<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Predictor Inteligente de Compras</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        🎯 Sistema predictivo basado en demanda real y tiempos de entrega de proveedores
      </p>
    </div>

    <!-- 🆕 NUEVA SECCIÓN: Alertas de Compra Inteligente -->
    <div v-if="!globalState.isLoading && proximasCompras.length > 0" class="mb-8">
      <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-lg p-6">
        <h3 class="text-xl font-bold mb-3 flex items-center">
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          ⏰ Calendario de Compras Recomendadas
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          <div v-for="compra in proximasCompras.slice(0, 6)" :key="compra.id" 
               class="bg-white/10 backdrop-blur rounded-lg p-4 border border-white/20">
            <div class="flex justify-between items-start mb-2">
              <p class="font-bold text-lg">{{ compra.producto_nombre }}</p>
              <span :class="getDiasClass(compra.dias_para_comprar)" class="px-2 py-1 rounded-full text-xs font-bold">
                {{ formatDiasParaComprar(compra.dias_para_comprar) }}
              </span>
            </div>
            <div class="text-sm space-y-1 opacity-90">
              <p>📦 Stock actual: <strong>{{ compra.stock_actual }} u.</strong></p>
              <p>🎯 Punto de reorden: <strong>{{ compra.punto_reorden }} u.</strong></p>
              <p>🚚 Lead time: <strong>{{ compra.lead_time_dias }} días</strong></p>
              <p>💰 Comprar: <strong>{{ compra.cantidad_sugerida }} u.</strong></p>
            </div>
          </div>
        </div>
        <p class="text-xs mt-4 opacity-75">
          💡 El sistema calcula el momento óptimo considerando tu demanda y el tiempo que tarda tu proveedor en entregar
        </p>
      </div>
    </div>

    <!-- Tarjetas de Resumen -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div v-if="accionUrgente" class="bg-gradient-to-br from-red-500 to-red-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚠️ Acción Urgente</h3>
        <p class="text-sm opacity-90">Nivel de stock crítico para <strong>{{ accionUrgente.producto_nombre }}</strong>.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ accionUrgente.stock_actual }} u.</strong></p>
          <p>Punto de reorden: <strong>{{ accionUrgente.punto_reorden }} u.</strong></p>
          <p>Lead time: <strong>{{ accionUrgente.lead_time_dias }} días</strong></p>
          <p v-if="accionUrgente.cantidad_sugerida > 0" class="mt-2 font-bold text-yellow-200">
            💡 Comprar YA: {{ accionUrgente.cantidad_sugerida }} unidades
          </p>
        </div>
      </div>
      
      <div v-if="riesgoAgotamiento" class="bg-gradient-to-br from-yellow-400 to-orange-500 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">⚡ Próxima Compra Programada</h3>
        <p class="text-sm opacity-90"><strong>{{ riesgoAgotamiento.producto_nombre }}</strong></p>
        <div class="mt-4 text-sm space-y-1">
          <p>Comprar en: <strong>{{ formatDiasParaComprar(riesgoAgotamiento.dias_para_comprar) }}</strong></p>
          <p>Stock actual: <strong>{{ riesgoAgotamiento.stock_actual }} u.</strong></p>
          <p>Lead time: <strong>{{ riesgoAgotamiento.lead_time_dias }} días</strong></p>
        </div>
      </div>

      <div v-if="oportunidadOptimizacion" class="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">💡 Oportunidad de Optimización</h3>
        <p class="text-sm opacity-90">Sobrestock en <strong>{{ oportunidadOptimizacion.producto_nombre }}</strong> (con demanda activa).</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Stock actual: <strong>{{ oportunidadOptimizacion.stock_actual }} u.</strong></p>
          <p>Demanda: <strong>{{ oportunidadOptimizacion.demanda_semanal_proyectada.toFixed(1) }} u/sem</strong></p>
          <p>Cobertura: <strong>{{ formatSemanasCobertura(oportunidadOptimizacion.semanas_cobertura) }}</strong></p>
          <p class="text-xs opacity-75 mt-2">💡 Considera reducir próximas órdenes de compra</p>
        </div>
      </div>

      <!-- Tarjeta alternativa si no hay sobrestock real pero hay productos sin demanda -->
      <div v-else-if="productosSinDemanda > 0" class="bg-gradient-to-br from-gray-500 to-gray-600 text-white rounded-lg shadow-lg p-5">
        <h3 class="text-lg font-bold mb-1">📊 Productos Sin Movimiento</h3>
        <p class="text-sm opacity-90">Tienes <strong>{{ productosSinDemanda }} productos</strong> sin ventas recientes.</p>
        <div class="mt-4 text-sm space-y-1">
          <p>Representan <strong>{{ ((productosSinDemanda / proyecciones.length) * 100).toFixed(1) }}%</strong> de tu catálogo</p>
          <p class="text-xs opacity-75 mt-2">💡 Considera descontinuar o promocionar estos productos</p>
        </div>
      </div>
    </div>

    <!-- Gráficos en Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      
      <!-- Gráfico 1: Estado de Inventario (Dona) -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="mb-4">
          <h3 class="text-xl font-semibold text-gray-800">Estado General del Inventario</h3>
          <p class="text-gray-500 text-sm">Distribución por nivel de urgencia</p>
        </div>
        
        <div v-if="globalState.isLoading" class="h-80 flex items-center justify-center text-gray-500">
          Cargando datos...
        </div>
        <div v-else-if="globalState.error" class="h-80 flex items-center justify-center text-red-600 bg-red-50 p-4 rounded-lg">
          Error: {{ globalState.error }}
        </div>
        <div v-else>
          <VueApexCharts type="donut" height="320" :options="donutChartOptions" :series="donutChartOptions.series" />
        </div>
      </div>

      <!-- Gráfico 2: Inversión Sugerida en Compras -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="mb-4">
          <h3 class="text-xl font-semibold text-gray-800">Inversión Sugerida en Compras</h3>
          <p class="text-gray-500 text-sm">Total de unidades a adquirir por urgencia</p>
        </div>
        
        <div v-if="globalState.isLoading" class="h-80 flex items-center justify-center text-gray-500">
          Cargando datos...
        </div>
        <div v-else-if="unidadesAComprar.total === 0" class="h-80 flex items-center justify-center text-gray-500 border-2 border-dashed border-gray-200 rounded-lg">
          <div class="text-center">
            <svg class="w-16 h-16 mx-auto text-green-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="font-medium text-gray-700">¡Excelente!</p>
            <p class="text-sm text-gray-500">No necesitas comprar nada por ahora</p>
          </div>
        </div>
        <div v-else>
          <VueApexCharts type="bar" height="320" :options="comprasChartOptions" :series="comprasChartOptions.series" />
        </div>
      </div>

      <!-- Gráfico 3: Tendencia de Ventas Mensuales -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="mb-4">
          <h3 class="text-xl font-semibold text-gray-800">Tendencia de Ventas</h3>
          <p class="text-gray-500 text-sm">Evolución mensual de unidades vendidas</p>
        </div>
        
        <div v-if="globalState.isLoading" class="h-80 flex items-center justify-center text-gray-500">
          Cargando datos...
        </div>
        <div v-else-if="globalState.error" class="h-80 flex items-center justify-center text-red-600 bg-red-50 p-4 rounded-lg">
          Error: {{ globalState.error }}
        </div>
        <div v-else>
          <VueApexCharts type="area" height="320" :options="trendChartOptions" :series="trendChartOptions.series" />
        </div>
      </div>

      <!-- Gráfico 4: Distribución de Cobertura -->
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="mb-4">
          <h3 class="text-xl font-semibold text-gray-800">Distribución de Cobertura</h3>
          <p class="text-gray-500 text-sm">Cantidad de productos por rango de cobertura</p>
        </div>
        
        <div v-if="globalState.isLoading" class="h-80 flex items-center justify-center text-gray-500">
          Cargando datos...
        </div>
        <div v-else>
          <VueApexCharts type="bar" height="320" :options="distribucionChartOptions" :series="distribucionChartOptions.series" />
        </div>
      </div>

    </div>

    <!-- KPIs Adicionales -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Total Unidades a Comprar</div>
        <div class="text-2xl font-bold text-red-600">
          {{ unidadesAComprar.total.toLocaleString() }}
        </div>
        <div class="text-xs text-gray-600 mt-1">
          {{ unidadesAComprar.productosUrgentes }} productos urgentes
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">⏰ Compras en 7 Días</div>
        <div class="text-2xl font-bold text-orange-600">
          {{ comprasProximas7dias }}
        </div>
        <div class="text-xs text-gray-600 mt-1">
          productos a pedir pronto
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Lead Time Promedio</div>
        <div class="text-2xl font-bold text-blue-600">
          {{ leadTimePromedio }} días
        </div>
        <div class="text-xs text-gray-600 mt-1">
          tiempo de entrega de proveedores
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Productos Sin Demanda</div>
        <div class="text-2xl font-bold text-gray-600">
          {{ productosSinDemanda }}
        </div>
        <div class="text-xs text-orange-600 mt-1">
          {{ ((productosSinDemanda / proyecciones.length) * 100).toFixed(1) }}% del inventario
        </div>
      </div>
    </div>

    <!-- Tabla de Proyecciones Detalladas -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado con Predicción de Compras</h3>
        <p class="text-sm text-gray-500 mt-1">🎯 Punto de reorden calculado según demanda y lead time del proveedor</p>
      </div>
      
      <div v-if="globalState.isLoading" class="p-8 text-center text-gray-500">Cargando proyecciones...</div>
      <div v-else-if="globalState.error" class="p-8 text-center text-red-600 bg-red-50">
        Error al cargar proyecciones: {{ globalState.error }}
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Producto</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock Actual</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Punto Reorden</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Lead Time</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comprar en</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cantidad</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in proyecciones" :key="item.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ item.producto_nombre }}</td>
              <td class="px-4 py-3 text-sm text-gray-800">{{ item.stock_actual }} u.</td>
              <td class="px-4 py-3 text-sm font-medium" :class="item.stock_actual <= item.punto_reorden ? 'text-red-600' : 'text-gray-800'">
                {{ item.punto_reorden }} u.
              </td>
              <td class="px-4 py-3 text-sm text-gray-800">
                {{ item.lead_time_dias }} días
              </td>
              <td class="px-4 py-3 text-sm font-medium" :class="getDiasClass(item.dias_para_comprar)">
                {{ formatDiasParaComprar(item.dias_para_comprar) }}
              </td>
              <td class="px-4 py-3 text-sm font-medium" :class="item.cantidad_sugerida > 0 ? 'text-red-600' : 'text-gray-800'">
                {{ item.cantidad_sugerida || 0 }} u.
              </td>
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
import { onMounted, reactive, computed, ref } from 'vue';
import axiosInstance from '@/api/axios.js';
import VueApexCharts from 'vue3-apexcharts';

// ==========================================
// STATE MANAGEMENT
// ==========================================

const globalState = reactive({
  isLoading: true,
  error: null,
});

const proyecciones = ref([]);

// ==========================================
// COMPUTED PROPERTIES
// ==========================================

const accionUrgente = computed(() =>
  proyecciones.value.find(p => p.estado === 'Comprar Ahora')
);

const riesgoAgotamiento = computed(() =>
  proyecciones.value.find(p => p.estado === 'Revisar Pronto')
);

const oportunidadOptimizacion = computed(() => {
  const productosExceso = proyecciones.value.filter(
    p => p.estado === 'Sobrestock' && 
    p.semanas_cobertura !== null && 
    isFinite(p.semanas_cobertura) &&
    p.semanas_cobertura <= 52 &&
    p.demanda_semanal_proyectada >= 0.5
  );
  if (productosExceso.length === 0) return null;
  return productosExceso.sort((a, b) => (b.semanas_cobertura || 0) - (a.semanas_cobertura || 0))[0];
});

// 🆕 Productos que necesitas comprar pronto (ordenados por urgencia)
const proximasCompras = computed(() => {
  return proyecciones.value
    .filter(p => p.dias_para_comprar !== null && p.dias_para_comprar <= 30)
    .sort((a, b) => a.dias_para_comprar - b.dias_para_comprar);
});

const unidadesAComprar = computed(() => {
  const productosUrgentes = proyecciones.value.filter(p => p.estado === 'Comprar Ahora');
  const total = productosUrgentes.reduce((sum, p) => sum + (p.cantidad_sugerida || 0), 0);
  return {
    total,
    productosUrgentes: productosUrgentes.length
  };
});

//const productosConDemanda = computed(() => {
//  return proyecciones.value.filter(
//    p => p.semanas_cobertura !== null && isFinite(p.semanas_cobertura)
//  ).length;
//});

const productosSinDemanda = computed(() => {
  return proyecciones.value.filter(
    p => p.semanas_cobertura === null || !isFinite(p.semanas_cobertura)
  ).length;
});

// 🆕 Compras en los próximos 7 días
const comprasProximas7dias = computed(() => {
  return proyecciones.value.filter(
    p => p.dias_para_comprar !== null && p.dias_para_comprar <= 7
  ).length;
});

// 🆕 Lead time promedio
const leadTimePromedio = computed(() => {
  const productosConLead = proyecciones.value.filter(p => p.lead_time_dias > 0);
  if (productosConLead.length === 0) return 0;
  const suma = productosConLead.reduce((sum, p) => sum + p.lead_time_dias, 0);
  return Math.round(suma / productosConLead.length);
});

const distribucionCobertura = computed(() => {
  const rangos = {
    'Crítico\n(< 2 sem)': 0,
    'Bajo\n(2-4 sem)': 0,
    'Óptimo\n(4-8 sem)': 0,
    'Alto\n(8-12 sem)': 0,
    'Exceso\n(> 12 sem)': 0
  };
  
  proyecciones.value.forEach(p => {
    if (p.semanas_cobertura === null || !isFinite(p.semanas_cobertura)) return;
    
    if (p.semanas_cobertura < 2) rangos['Crítico\n(< 2 sem)']++;
    else if (p.semanas_cobertura < 4) rangos['Bajo\n(2-4 sem)']++;
    else if (p.semanas_cobertura < 8) rangos['Óptimo\n(4-8 sem)']++;
    else if (p.semanas_cobertura < 12) rangos['Alto\n(8-12 sem)']++;
    else rangos['Exceso\n(> 12 sem)']++;
  });
  
  return rangos;
});

// ==========================================
// CHART OPTIONS
// ==========================================

const donutChartOptions = reactive({
  series: [],
  chart: { type: 'donut', height: 320 },
  labels: ['Comprar Ahora', 'Revisar Pronto', 'Stock OK', 'Sobrestock'],
  colors: ['#EF4444', '#F59E0B', '#10B981', '#A855F7'],
  legend: { position: 'bottom' },
  plotOptions: {
    pie: {
      donut: {
        size: '65%',
        labels: {
          show: true,
          total: {
            show: true,
            label: 'Total Productos',
            fontSize: '16px',
            fontWeight: 600
          }
        }
      }
    }
  },
  dataLabels: { enabled: true }
});

const comprasChartOptions = reactive({
  series: [{ name: 'Unidades', data: [] }],
  chart: { type: 'bar', height: 320, toolbar: { show: false } },
  plotOptions: { 
    bar: { 
      horizontal: false,
      columnWidth: '60%',
      distributed: true
    } 
  },
  colors: ['#EF4444', '#F59E0B', '#10B981', '#A855F7'],
  dataLabels: { 
    enabled: true,
    formatter: (val) => val > 0 ? val.toLocaleString() + ' u.' : ''
  },
  xaxis: { 
    categories: ['Urgente', 'Revisar Pronto', 'Stock OK', 'Sobrestock'],
    labels: { style: { fontSize: '11px' } }
  },
  yaxis: { title: { text: 'Unidades a Comprar' } },
  legend: { show: false },
  tooltip: {
    y: {
      formatter: (val) => val.toLocaleString() + ' unidades'
    }
  }
});

const trendChartOptions = reactive({
  series: [{ name: 'Unidades Vendidas', data: [] }],
  chart: { type: 'area', height: 320, toolbar: { show: false } },
  stroke: { curve: 'smooth', width: 2 },
  fill: { 
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.3,
    }
  },
  colors: ['#14B8A6'],
  xaxis: { categories: [] },
  yaxis: { title: { text: 'Unidades' } },
  dataLabels: { enabled: false }
});

const distribucionChartOptions = reactive({
  series: [{ name: 'Productos', data: [] }],
  chart: { type: 'bar', height: 320, toolbar: { show: false } },
  plotOptions: { 
    bar: { 
      horizontal: false,
      columnWidth: '70%',
      distributed: true
    } 
  },
  colors: ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#A855F7'],
  dataLabels: { 
    enabled: true,
    formatter: (val) => val > 0 ? val : ''
  },
  xaxis: { 
    categories: [],
    labels: { 
      style: { fontSize: '10px' },
      rotate: 0
    }
  },
  yaxis: { 
    title: { text: 'Cantidad de Productos' },
    labels: {
      formatter: (val) => Math.round(val)
    }
  },
  legend: { show: false },
  tooltip: {
    y: {
      formatter: (val) => val + ' productos'
    }
  }
});

// ==========================================
// LIFECYCLE
// ==========================================

onMounted(async () => {
  await loadDashboardData();
});

// ==========================================
// DATA LOADING
// ==========================================

const loadDashboardData = async () => {
  globalState.isLoading = true;
  globalState.error = null;
  
  try {
    const response = await axiosInstance.get('/analytics/dashboard-consolidado/');
    const data = response.data;
    
    proyecciones.value = data.proyecciones || [];
    
    updateDonutChart(data.estado_inventario || []);
    updateTrendChart(data.ventas_mensuales || []);
    updateComprasChart();
    updateDistribucionChart();
    
    globalState.isLoading = false;
  } catch (err) {
    console.error("Error al cargar dashboard:", err);
    globalState.error = err.response?.data?.error || err.message || "Error al cargar datos.";
    globalState.isLoading = false;
  }
};

const updateDonutChart = (estadoInventario) => {
  const ordenEstados = ['Comprar Ahora', 'Revisar Pronto', 'Stock OK', 'Sobrestock'];
  donutChartOptions.series = ordenEstados.map(estado => {
    const item = estadoInventario.find(d => d.estado === estado);
    return item ? item.count : 0;
  });
};

const updateTrendChart = (ventasData) => {
  if (ventasData && ventasData.length > 0) {
    trendChartOptions.xaxis.categories = ventasData.map(item => 
      new Date(item.time).toLocaleDateString('es-CL', { month: 'short', year: '2-digit' })
    );
    trendChartOptions.series[0].data = ventasData.map(item => item.value);
  }
};

const updateComprasChart = () => {
  const estados = ['Comprar Ahora', 'Revisar Pronto', 'Stock OK', 'Sobrestock'];
  const unidadesPorEstado = estados.map(estado => {
    const productos = proyecciones.value.filter(p => p.estado === estado);
    return productos.reduce((sum, p) => sum + (p.cantidad_sugerida || 0), 0);
  });
  
  comprasChartOptions.series[0].data = unidadesPorEstado;
};

const updateDistribucionChart = () => {
  const dist = distribucionCobertura.value;
  distribucionChartOptions.xaxis.categories = Object.keys(dist);
  distribucionChartOptions.series[0].data = Object.values(dist);
};

// ==========================================
// HELPER FUNCTIONS
// ==========================================

const formatSemanasCobertura = (semanas) => {
  if (semanas === null || semanas === undefined) {
    return 'Sin demanda';
  }
  if (!isFinite(semanas)) {
    return 'N/A';
  }
  return `~${semanas.toFixed(1)} sem.`;
};

// 🆕 Formatear días para comprar
const formatDiasParaComprar = (dias) => {
  if (dias === null || dias === undefined) {
    return 'Sin demanda';
  }
  if (dias === 0) {
    return '¡AHORA!';
  }
  if (dias === 1) {
    return 'Mañana';
  }
  if (dias <= 7) {
    return `${dias} días`;
  }
  if (dias <= 30) {
    return `~${Math.round(dias / 7)} semanas`;
  }
  return `${dias} días`;
};

// 🆕 Clase CSS según urgencia de días
const getDiasClass = (dias) => {
  if (dias === null) return 'text-gray-500';
  if (dias === 0) return 'text-red-600 bg-red-100';
  if (dias <= 3) return 'text-orange-600 bg-orange-100';
  if (dias <= 7) return 'text-yellow-600 bg-yellow-100';
  if (dias <= 14) return 'text-blue-600 bg-blue-100';
  return 'text-gray-600 bg-gray-100';
};

const getEstadoClass = (estado) => {
  const classes = {
    'Comprar Ahora': 'bg-red-100 text-red-800',
    'Revisar Pronto': 'bg-yellow-100 text-yellow-800',
    'Stock OK': 'bg-green-100 text-green-800',
    'Sobrestock': 'bg-purple-100 text-purple-800',
  };
  return classes[estado] || 'bg-gray-100 text-gray-800';
};

const getEstadoText = (estado) => {
  const textos = {
    'Comprar Ahora': '🚨 Urgente',
    'Revisar Pronto': '⚠️ Riesgo',
    'Stock OK': '✅ OK',
    'Sobrestock': '📦 Exceso',
  };
  return textos[estado] || 'Normal';
};
</script>

<style scoped>
.bg-white {
  transition: transform 0.2s;
}

.bg-white:hover {
  transform: translateY(-2px);
}
</style>