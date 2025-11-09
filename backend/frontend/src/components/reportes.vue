<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-2">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Reportes y Análisis de Inventario</h2>
        <span v-if="aiEnabled" class="ml-3 px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold rounded-full">
          🤖 inxex AI
        </span>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Tasa de Cumplimiento</h3>
        <div v-if="!globalState.isLoading" class="text-4xl font-bold mb-2">
          {{ kpisData.tasa_cumplimiento || 'N/A' }}%
        </div>
        <div v-else class="text-2xl font-bold mb-2">Cargando...</div>
        <p class="text-sm opacity-90">Productos sin necesidad crítica de compra</p>
      </div>
      
      <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Días Promedio de Cobertura</h3>
        <div v-if="!globalState.isLoading" class="text-4xl font-bold mb-2">
          {{ kpisData.dias_cobertura_promedio || 'N/A' }}
        </div>
        <div v-else class="text-2xl font-bold mb-2">Cargando...</div>
        <p class="text-sm opacity-90">Días de stock restantes (promedio)</p>
      </div>
      
      <div class="bg-gradient-to-br from-violet-500 to-violet-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Unidades en Sobrestock</h3>
        <div v-if="!globalState.isLoading" class="text-4xl font-bold mb-2">
          {{ (kpisData.unidades_sobrestock || 0).toLocaleString() }} u.
        </div>
        <div v-else class="text-2xl font-bold mb-2">Cargando...</div>
        <p class="text-sm opacity-90">Inventario excedente (unidades)</p>
      </div>
    </div>

    <div class="mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
        </svg>
        <h3 class="text-2xl font-bold text-gray-900">Gráficos de Rendimiento</h3>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h4 class="text-lg font-bold text-gray-900 mb-4">Ventas Mensuales (Unidades)</h4>
          <div v-if="!globalState.isLoading && ventasChartOptions.series[0].data.length > 0">
            <VueApexCharts type="bar" height="256" :options="ventasChartOptions" :series="ventasChartOptions.series" />
          </div>
          <div v-else-if="!globalState.isLoading" class="h-64 flex items-center justify-center text-sm text-gray-500 border-2 border-dashed border-indigo-200 rounded-lg">
            <p>No hay datos de ventas disponibles</p>
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500 border-2 border-dashed border-indigo-200 rounded-lg">
            Cargando gráfico...
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <h4 class="text-lg font-bold text-gray-900 mb-4">Tiempo de Espera (Lead Time) Promedio por Proveedor</h4>
          <div v-if="!globalState.isLoading" class="h-64">
            <div v-if="leadTimeChartOptions.series[0].data.length === 0" class="h-full flex items-center justify-center text-sm text-gray-500 border-2 border-dashed border-purple-200 rounded-lg">
              <p>No hay suficientes datos de fecha de pedido/recepción.</p>
            </div>
            <VueApexCharts v-else type="bar" height="100%" :options="leadTimeChartOptions" :series="leadTimeChartOptions.series" />
          </div>
          <div v-else class="h-64 flex items-center justify-center text-gray-500 border-2 border-dashed border-purple-200 rounded-lg">
            Cargando gráfico...
          </div>
        </div>
      </div>
    </div>

    <div v-if="aiReportContent" class="mb-8 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg shadow-lg p-6 border-2 border-purple-200">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <h3 class="text-xl font-bold text-gray-900">🤖 Análisis Inteligente</h3>
      </div>
      <div class="prose prose-sm max-w-none text-gray-700" v-html="formatMarkdown(aiReportContent)"></div>
    </div>

    <div class="flex justify-center gap-4 mb-8">
      <button 
        v-if="aiEnabled"
        @click="descargarReporteConIA" 
        :disabled="downloading || globalState.isLoading" 
        class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="!downloading && !isGeneratingAI" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <svg v-if="downloading || isGeneratingAI" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span v-if="isGeneratingAI">Generando análisis con IA...</span>
        <span v-else-if="downloading">Creando ...</span>
        <span v-else>🤖 Generar Reporte con IA </span>
      </button>

      <button 
        @click="descargarReporteBasico" 
        :disabled="downloading || globalState.isLoading" 
        class="bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="!downloading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span v-if="!downloading">Descargar Reporte {{ aiEnabled ? 'Básico' : '' }} (PDF)</span>
        <span v-else>Generando PDF...</span>
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado por Producto</h3>
      </div>
      
      <div v-if="globalState.isLoading" class="p-8 text-center text-gray-500">
        Cargando datos de proyecciones...
      </div>
      <div v-else-if="globalState.error" class="p-8 text-center text-red-600 bg-red-50">
        Error: {{ globalState.error }}
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Demanda (sem.)</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Actual</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cobertura (sem.)</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lead Time</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Días p/ Comprar</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Compra Sugerida</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="producto in proyecciones" :key="producto.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ producto.producto_nombre }}</div>
                <div class="text-sm text-gray-500">SKU: {{ producto.producto_id }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ producto.demanda_semanal_proyectada.toFixed(1) }} u.
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ producto.stock_actual }} u.
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ formatSemanasCobertura(producto.semanas_cobertura) }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ producto.lead_time_dias }} días
              </td>
              <td class="px-6 py-4 text-sm" :class="getDiasComprarClass(producto.dias_para_comprar)">
                {{ formatDiasComprar(producto.dias_para_comprar) }}
              </td>
              <td class="px-6 py-4 text-sm font-medium" :class="producto.cantidad_sugerida > 0 ? 'text-red-600' : 'text-gray-900'">
                {{ (producto.cantidad_sugerida || 0).toLocaleString() }} u.
              </td>
              <td class="px-6 py-4">
                <span :class="getEstadoClass(producto.estado)" class="px-2 py-1 text-xs font-semibold rounded-full">
                  {{ producto.estado }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Total Ventas (unidades)</div>
        <div v-if="!globalState.isLoading" class="text-2xl font-bold text-gray-900">
          {{ (kpisData.total_ventas_unidades || 0).toLocaleString() }}
        </div>
        <div v-else class="text-xl font-bold">...</div>
        <div class="text-xs text-green-600 mt-1">Últimos 12 meses</div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Unidades Totales en Stock</div>
        <div v-if="!globalState.isLoading" class="text-2xl font-bold text-gray-900">
          {{ (kpisData.unidades_totales_stock || 0).toLocaleString() }}
        </div>
        <div v-else class="text-xl font-bold">...</div>
        <div class="text-xs text-gray-600 mt-1">En {{ proyecciones.length }} productos</div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Productos Críticos (Urgente)</div>
        <div v-if="!globalState.isLoading" class="text-2xl font-bold text-red-600">
          {{ kpisData.productos_criticos || 0 }}
        </div>
        <div v-else class="text-xl font-bold">...</div>
        <div class="text-xs text-red-600 mt-1">Requieren acción inmediata</div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Eficiencia Stock</div>
        <div v-if="!globalState.isLoading" class="text-2xl font-bold text-green-600">
          {{ kpisData.eficiencia_stock || 'N/A' }}%
        </div>
        <div v-else class="text-xl font-bold">...</div>
        <div class="text-xs text-gray-500 mt-1">Productos con stock óptimo</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import axiosInstance from '@/api/axios.js';
import VueApexCharts from 'vue3-apexcharts';

// ==========================================
// GEMINI AI INITIALIZATION
// ==========================================

// ❗ CAMBIO 1: 'model' ahora es una 'ref' para ser reactivo.
const model = ref(null);

// ✅ Obtener API Key desde variables de entorno de Vue CLI
const GEMINI_API_KEY = process.env.VUE_APP_GEMINI_API_KEY;

console.log('🔑 API Key detectada:', GEMINI_API_KEY ? 'SÍ ✅' : 'NO ❌');


// Try to initialize Gemini (async but not awaited)
const initGemini = async () => {
  try {
    const { GoogleGenerativeAI } = await import('@google/generative-ai');
    
    if (GEMINI_API_KEY) {
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      
      // ❗ CAMBIO 2: Usamos model.value y un modelo estable 
      model.value = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
      
      console.log('✅ Gemini AI inicializado correctamente');
      return true;
    } else {
      console.warn('⚠️ API Key de Gemini no configurada. La funcionalidad de IA estará deshabilitada.');
      console.warn('   Crea un archivo .env con: VUE_APP_GEMINI_API_KEY=tu_api_key');
      return false;
    }
  } catch (error) {
    console.warn('⚠️ No se pudo cargar @google/generative-ai. La funcionalidad de IA estará deshabilitada.');
    console.warn('   Instala con: npm install @google/generative-ai');
    console.error('   Error:', error.message);
    return false;
  }
};

// Start initialization (non-blocking)
const geminiReady = ref(false);
initGemini().then(ready => {
  geminiReady.value = ready;
});

// ==========================================
// STATE MANAGEMENT
// ==========================================

const globalState = reactive({
  isLoading: true,
  error: null,
});

const downloading = ref(false);
const cdnLoaded = ref(false);
const isGeneratingAI = ref(false);
const aiReportContent = ref(null);

// ❗ CAMBIO 3: La propiedad computada ahora lee 'model.value'.
const aiEnabled = computed(() => !!(GEMINI_API_KEY && model.value && geminiReady.value));

// Data containers
const proyecciones = ref([]);
const kpisData = reactive({
  tasa_cumplimiento: 0,
  eficiencia_stock: 0,
  dias_cobertura_promedio: 0,
  unidades_sobrestock: 0,
  total_ventas_unidades: 0,
  unidades_totales_stock: 0,
  productos_criticos: 0,
});

// ==========================================
// CHART OPTIONS
// ==========================================

const ventasChartOptions = reactive({
  series: [{
    name: 'Unidades Vendidas',
    data: []
  }],
  chart: { 
    type: 'bar', 
    height: 256, 
    toolbar: { show: false } 
  },
  plotOptions: { 
    bar: { 
      columnWidth: '45%', 
      distributed: true 
    } 
  },
  dataLabels: { enabled: false },
  legend: { show: false },
  xaxis: {
    categories: [],
    labels: { style: { fontSize: '12px' } }
  },
  yaxis: { 
    title: { text: 'Unidades' } 
  },
  colors: ['#4F46E5', '#7C3AED', '#EC4899', '#10B981', '#F59E0B', '#3B82F6'],
});

const leadTimeChartOptions = reactive({
  series: [{
    name: 'Días Promedio',
    data: []
  }],
  chart: { 
    type: 'bar', 
    height: '100%', 
    toolbar: { show: false } 
  },
  plotOptions: { 
    bar: { 
      horizontal: true, 
      barHeight: '50%' 
    } 
  },
  dataLabels: { 
    enabled: true, 
    textAnchor: 'start', 
    style: { colors: ['#000'] }, 
    offsetX: 0, 
    formatter: (val) => val + " días" 
  },
  xaxis: {
    categories: [],
    title: { text: 'Días Promedio de Espera' }
  },
  yaxis: { 
    labels: { 
      show: true, 
      align: 'right', 
      minWidth: 100, 
      maxWidth: 200 
    } 
  },
  grid: { 
    xaxis: { lines: { show: true } } 
  },
  tooltip: { x: { show: false } }
});

// ==========================================
// LIFECYCLE
// ==========================================

onMounted(async () => {
  try {
    await loadJsPdfCdn();
    console.log('✅ jsPDF CDN cargado correctamente');
    
    await loadDashboardData();
  } catch (error) {
    console.error("Error en la carga inicial:", error);
    globalState.error = "Error al cargar datos. Por favor, intente recargar la página.";
    globalState.isLoading = false;
  }
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
    Object.assign(kpisData, data.kpis || {});
    
    updateVentasChart(data.ventas_mensuales || []);
    updateLeadTimeChart(data.lead_times || []);
    
    globalState.isLoading = false;
  } catch (err) {
    console.error("Error al cargar dashboard:", err);
    globalState.error = "Error al cargar los datos. Intente más tarde.";
    globalState.isLoading = false;
  }
};

const updateVentasChart = (ventasData) => {
  if (ventasData && ventasData.length > 0) {
    ventasChartOptions.xaxis.categories = ventasData.map(item => 
      new Date(item.time).toLocaleString('es-CL', { month: 'short', year: '2-digit' })
    );
    ventasChartOptions.series[0].data = ventasData.map(item => item.value);
  }
};

const updateLeadTimeChart = (leadTimeData) => {
  if (leadTimeData && leadTimeData.length > 0) {
    const sortedData = [...leadTimeData].sort((a, b) => a.avg_lead_time_days - b.avg_lead_time_days);
    
    leadTimeChartOptions.xaxis.categories = sortedData.map(item => item.proveedor__nombre);
    leadTimeChartOptions.series[0].data = sortedData.map(item => item.avg_lead_time_days);
  }
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
  return semanas.toFixed(1);
};

const formatDiasComprar = (dias) => {
  if (dias === null || dias === undefined) {
    return 'N/A';
  }
  if (dias === 0) {
    return '¡AHORA!';
  }
  if (dias < 0) {
    return 'URGENTE';
  }
  return `${dias} días`;
};

const getDiasComprarClass = (dias) => {
  if (dias === null || dias === undefined) {
    return 'text-gray-500';
  }
  if (dias === 0 || dias < 0) {
    return 'text-red-600 font-bold';
  }
  if (dias <= 7) {
    return 'text-orange-600 font-semibold';
  }
  return 'text-gray-900';
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

const formatMarkdown = (text) => {
  if (!text) return '';
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold mt-4 mb-2">$1</h3>')
    .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-4 mb-2">$1</h2>')
    .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-4 mb-2">$1</h1>')
    .replace(/^- (.*$)/gim, '<li class="ml-4">• $1</li>')
    .replace(/\n\n/g, '</p><p class="mt-2">')
    .replace(/^(.+)$/gim, '<p>$1</p>');
};

// ==========================================
// AI REPORT GENERATION
// ==========================================

const generarReporteConIA = async () => {
  console.log('🤖 Iniciando generación de reporte con IA...');
  
  if (!aiEnabled.value) {
    alert("⚠️ Gemini AI no está disponible.\n\n" +
          "Para habilitar esta función:\n" +
          "1. Instala: npm install @google/generative-ai\n" +
          "2. Crea archivo .env con: VUE_APP_GEMINI_API_KEY=tu_api_key\n" +
          "3. Obtén tu API key en: https://makersuite.google.com/app/apikey\n" +
          "4. Reinicia el servidor con: npm run serve");
    return null;
  }

  isGeneratingAI.value = true;
  aiReportContent.value = null;

  const datosParaIA = {
    kpis: kpisData,
    productos_criticos: proyecciones.value.filter(p => p.estado === 'Comprar Ahora').slice(0, 5).map(p => ({
      nombre: p.producto_nombre,
      stock: p.stock_actual,
      demanda_semanal: p.demanda_semanal_proyectada,
      cobertura_semanas: p.semanas_cobertura,
      comprar: p.cantidad_sugerida,
      // 🆕 NUEVOS DATOS PARA IA
      lead_time_dias: p.lead_time_dias,
      punto_reorden: p.punto_reorden,
      dias_para_comprar: p.dias_para_comprar
    })),
    productos_sobrestock: proyecciones.value.filter(p => p.estado === 'Sobrestock').slice(0, 3).map(p => ({
      nombre: p.producto_nombre,
      stock: p.stock_actual,
      cobertura_semanas: p.semanas_cobertura
    })),
    resumen: {
      total_productos: proyecciones.value.length,
      productos_ok: proyecciones.value.filter(p => p.estado === 'Stock OK').length,
      productos_criticos: kpisData.productos_criticos,
      eficiencia: kpisData.eficiencia_stock
    }
  };
  
  console.log('📊 Datos preparados para IA');
  const datosJSON = JSON.stringify(datosParaIA, null, 2);

  const prompt = `Eres un experto analista de inventarios para una PYME.

Analiza los siguientes datos del inventario y genera un reporte ejecutivo en español con:

1. **Resumen Ejecutivo** (2-3 oraciones sobre la situación general)
2. **Productos Críticos** (Máximo 3, menciona cuántos días faltan para comprar y el lead time del proveedor)
3. **Recomendaciones Accionables** (Máximo 3, específicas considerando los tiempos de entrega)

DATOS DEL INVENTARIO:
${datosJSON}

CONTEXTO IMPORTANTE:
- "dias_para_comprar": Cuántos días quedan antes de que el stock llegue al punto de reorden
- "lead_time_dias": Cuántos días tarda el proveedor en entregar el pedido
- "punto_reorden": Stock mínimo antes de quedarse sin producto

IMPORTANTE:
- Usa un tono profesional pero directo
- Sé específico con los productos problemáticos
- Las recomendaciones deben considerar los tiempos de entrega 
- Si "dias_para_comprar" es 0 o negativo, es URGENTE
- Usa formato Markdown simple (**, -, ##)
- Máximo 300 palabras en total`;

  try {
    console.log('📡 Enviando solicitud a Gemini AI...');
    
    // ❗ CAMBIO 4: Usamos 'model.value' para llamar a la IA.
    const result = await model.value.generateContent(prompt);
    
    const response = await result.response;
    const text = response.text();
    
    console.log('✅ Texto generado:', text.substring(0, 100) + '...');
    console.log('📝 Longitud del texto:', text.length, 'caracteres');
    
    aiReportContent.value = text;
    isGeneratingAI.value = false;
    
    return text;
  
  } catch (error) {
    console.error("❌ Error al generar reporte con IA:", error);
    console.error("Error completo:", error);
    
    alert(`Error al conectar con Gemini AI: ${error.message}\n\nEl reporte se generará sin recomendaciones.`);
    isGeneratingAI.value = false;
    return null;
  }
};

// ==========================================
// PDF GENERATION
// ==========================================

const loadJsPdfCdn = () => {
  return new Promise((resolve, reject) => {
    if (window.jspdf && typeof window.jspdf.jsPDF === 'function') {
      cdnLoaded.value = true;
      resolve();
      return;
    }

    const scriptJsPdf = document.createElement('script');
    scriptJsPdf.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
    scriptJsPdf.async = true;
    
    scriptJsPdf.onload = () => {
      const scriptAutoTable = document.createElement('script');
      scriptAutoTable.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js';
      scriptAutoTable.async = true;
      
      scriptAutoTable.onload = () => {
        cdnLoaded.value = true;
        resolve();
      };
      
      scriptAutoTable.onerror = () => reject(new Error('Error al cargar autoTable CDN'));
      document.head.appendChild(scriptAutoTable);
    };
    
    scriptJsPdf.onerror = () => reject(new Error('Error al cargar jsPDF CDN'));
    document.head.appendChild(scriptJsPdf);
  });
};

const generarBasePDF = (doc) => {
  // Encabezado
  doc.setFontSize(18);
  doc.setTextColor(20, 184, 166);
  doc.text('Reporte de Análisis de Inventario', 14, 20);
  
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Fecha: ${new Date().toLocaleDateString('es-CL', { year: 'numeric', month: 'long', day: 'numeric' })}`, 14, 27);
  
  // KPIs Resumen
  doc.setFontSize(12);
  doc.setTextColor(0);
  doc.text('Resumen de Indicadores Clave', 14, 37);
  
  doc.setFontSize(9);
  doc.setTextColor(60);
  let yPos = 43;
  doc.text(`• Tasa de Cumplimiento: ${kpisData.tasa_cumplimiento || 'N/A'}%`, 16, yPos);
  doc.text(`• Días Promedio de Cobertura: ${kpisData.dias_cobertura_promedio || 'N/A'}`, 16, yPos + 5);
  doc.text(`• Unidades en Sobrestock: ${(kpisData.unidades_sobrestock || 0).toLocaleString()} u.`, 16, yPos + 10);
  doc.text(`• Productos Críticos: ${kpisData.productos_criticos || 0}`, 16, yPos + 15);
  
  // Tabla de productos con NUEVAS columnas
  const columnas = [
    'Producto', 
    'Dem.\n(sem.)', 
    'Stock', 
    'Días p/\nComprar',  // 🆕 NUEVA COLUMNA
    'Compra', 
    'Estado'
  ];
  
  const filas = proyecciones.value.map(item => [
    item.producto_nombre || 'N/A',
    `${(item.demanda_semanal_proyectada || 0).toFixed(1)}`,
    `${item.stock_actual || 0}`,
    formatDiasComprar(item.dias_para_comprar),  // 🆕 NUEVO CAMPO
    `${(item.cantidad_sugerida || 0).toLocaleString()}`,
    item.estado || 'N/A'
  ]);

  const pageWidth = doc.internal.pageSize.width;
  const leftMargin = 10;
  const rightMargin = 10;
  const availableWidth = pageWidth - leftMargin - rightMargin;

  doc.autoTable({
    head: [columnas],
    body: filas,
    startY: yPos + 25,
    theme: 'striped',
    headStyles: {
      fillColor: [20, 184, 166],
      textColor: 255,
      fontSize: 8,
      fontStyle: 'bold',
      halign: 'center'
    },
    bodyStyles: {
      fontSize: 7,
      cellPadding: 2
    },
    alternateRowStyles: {
      fillColor: [245, 247, 250]
    },
    columnStyles: {
      0: { cellWidth: 'auto' },  // Producto - se ajusta automáticamente
      1: { halign: 'center', cellWidth: 16 },
      2: { halign: 'center', cellWidth: 14 },
      3: { halign: 'center', cellWidth: 18 },  // 🆕 Días p/ Comprar
      4: { halign: 'center', cellWidth: 18 },
      5: { halign: 'center', cellWidth: 22 }
    },
    margin: { left: leftMargin, right: rightMargin },
    tableWidth: availableWidth
  });
};

const agregarPaginaIA = (doc, textoIA) => {
  if (!textoIA || textoIA.length === 0) {
    console.warn('⚠️ No se añadió página de IA (texto vacío)');
    return;
  }
  
  console.log('✅ Añadiendo página de IA al PDF...');
  doc.addPage();
  
  doc.setFontSize(14);
  doc.setTextColor(147, 51, 234);
  doc.text('🤖 Análisis y Recomendaciones (Gemini AI)', 14, 20);

  doc.setFontSize(10);
  doc.setTextColor(0);
  
  const textoFormateado = textoIA
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/^- /gm, '• ')
    .replace(/^## /gm, '\n')
    .replace(/^# /gm, '\n');

  const lineas = doc.splitTextToSize(textoFormateado, 180);
  doc.text(lineas, 14, 30);
  
  console.log('✅ Página de IA añadida correctamente');
};

const agregarPiePagina = (doc) => {
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(150);
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 10,
      { align: 'center' }
    );
  }
};

const descargarReporteConIA = async () => {
  console.log('📄 Iniciando descarga de reporte con IA...');
  downloading.value = true;
  
  if (proyecciones.value.length === 0) {
    alert("No hay datos en la tabla para generar un reporte.");
    downloading.value = false;
    return;
  }

  console.log('🤖 Llamando a generarReporteConIA()...');
  const recomendacionesIA = await generarReporteConIA();
  
  console.log('📊 Recomendaciones recibidas:', recomendacionesIA ? `SÍ (${recomendacionesIA.length} caracteres)` : 'NO');

  try {
    if (!cdnLoaded.value) {
      await loadJsPdfCdn();
    }

    if (!window.jspdf || typeof window.jspdf.jsPDF !== 'function') {
      throw new Error('jsPDF no está disponible');
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    generarBasePDF(doc);
    
    if (recomendacionesIA && recomendacionesIA.length > 0) {
      agregarPaginaIA(doc, recomendacionesIA);
    }
    
    agregarPiePagina(doc);

    doc.save(`reporte_IA_${new Date().toISOString().split('T')[0]}.pdf`);
    console.log('✅ PDF descargado correctamente');

  } catch (error) {
    console.error("❌ Error al generar el PDF:", error);
    alert('Error al generar el reporte PDF.');
  } finally {
    downloading.value = false;
    isGeneratingAI.value = false;
  }
};

const descargarReporteBasico = async () => {
  downloading.value = true;
  
  if (proyecciones.value.length === 0) {
    alert("No hay datos en la tabla para generar un reporte.");
    downloading.value = false;
    return;
  }

  try {
    if (!cdnLoaded.value) {
      await loadJsPdfCdn();
    }

    if (!window.jspdf || typeof window.jspdf.jsPDF !== 'function') {
      throw new Error('jsPDF no está disponible');
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    generarBasePDF(doc);
    agregarPiePagina(doc);

    doc.save(`reporte_basico_${new Date().toISOString().split('T')[0]}.pdf`);

  } catch (error) {
    console.error("Error al generar el PDF:", error);
    alert('Error al generar el reporte PDF.');
  } finally {
    downloading.value = false;
  }
};
</script>

<style scoped>
button:hover:not(:disabled) {
  box-shadow: 0 10px 25px -5px rgba(20, 184, 166, 0.4);
}

button:active:not(:disabled) {
  transform: scale(0.98);
}

.prose p {
  margin-bottom: 0.5rem;
}

.prose li {
  margin-bottom: 0.25rem;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>