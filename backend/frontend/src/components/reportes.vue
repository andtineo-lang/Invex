<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-2">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Reportes y Análisis de Inventario</h2>
        <span v-if="aiEnabled" class="ml-3 px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold rounded-full">
          🤖 inxex AI PRO
        </span>
      </div>
    </div>

    <!-- KPIs Cards -->
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

    <!-- Charts -->
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

    <!-- AI Report Content -->
    <div v-if="aiReportContent" class="mb-8 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg shadow-lg p-6 border-2 border-purple-200">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <h3 class="text-xl font-bold text-gray-900">🤖 Análisis Inteligente</h3>
      </div>
      <div class="prose prose-sm max-w-none text-gray-700" v-html="formatMarkdown(aiReportContent)"></div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-center gap-4 mb-8">
      <button 
        v-if="aiEnabled"
        @click="descargarReporteConIA" 
        :disabled="downloading || globalState.isLoading || isGeneratingAI" 
        class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="!downloading && !isGeneratingAI" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        <svg v-if="downloading || isGeneratingAI" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span v-if="isGeneratingAI">Analizando inventario...</span>
        <span v-else-if="downloading">Creando PDF...</span>
        <span v-else>🤖 Generar Reporte Estratégico con IA</span>
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

    <!-- Products Table -->
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
                {{ Math.ceil(producto.demanda_semanal_proyectada) }} u.
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ producto.stock_actual }} u.
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ calculateVisualCoverage(producto.stock_actual, producto.demanda_semanal_proyectada) }}
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

    <!-- Bottom KPIs -->
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
import { ref, reactive, computed, onMounted } from 'vue';
import axiosInstance from '@/api/axios.js';
import VueApexCharts from 'vue3-apexcharts';

// ==========================================
// TOON IMPORT (Asíncrono)
// ==========================================

let toTOON = null;
let toonDisponible = false;

import('@toon-format/toon').then(toonModule => {
  toTOON = toonModule.encode;
  toonDisponible = true;
  console.log('✅ TOON cargado correctamente');
}).catch(() => {
  console.warn('⚠️ TOON no disponible - Se usará JSON estándar');
  toonDisponible = false;
});

// ==========================================
// GEMINI AI INITIALIZATION
// ==========================================

const model = ref(null);
const GEMINI_API_KEY = process.env.VUE_APP_GEMINI_API_KEY;

const initGemini = () => {
  import('@google/generative-ai').then(({ GoogleGenerativeAI }) => {
    if (GEMINI_API_KEY) {
      const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
      model.value = genAI.getGenerativeModel({ 
        model: "gemini-2.5-flash",
        generationConfig: {
          temperature: 0.3,
          maxOutputTokens: 4096,
          topP: 0.95,
          topK: 40,
        }
      });
      geminiReady.value = true;
      console.log('✅ Gemini 2.5 Flash inicializado para producción');
    } else {
      console.warn('⚠️ GEMINI_API_KEY no configurada');
    }
  }).catch(err => {
    console.error('❌ Error al cargar Gemini:', err);
    geminiReady.value = false;
  });
};

// ==========================================
// STATE MANAGEMENT
// ==========================================

const globalState = reactive({ isLoading: true, error: null });
const downloading = ref(false);
const cdnLoaded = ref(false);
const isGeneratingAI = ref(false);
const aiReportContent = ref(null);
const geminiReady = ref(false);
const aiEnabled = computed(() => !!(GEMINI_API_KEY && model.value && geminiReady.value));

const proyecciones = ref([]);
const empresaConfig = ref(null);
const kpisData = reactive({
  tasa_cumplimiento: 0, 
  eficiencia_stock: 0, 
  dias_cobertura_promedio: 0,
  unidades_sobrestock: 0, 
  total_ventas_unidades: 0, 
  unidades_totales_stock: 0, 
  productos_criticos: 0
});

// ==========================================
// CHART OPTIONS
// ==========================================

const ventasChartOptions = reactive({
  series: [{ name: 'Unidades Vendidas', data: [] }],
  chart: { type: 'bar', height: 256, toolbar: { show: false } },
  plotOptions: { bar: { columnWidth: '45%', distributed: true } },
  dataLabels: { enabled: false },
  legend: { show: false },
  xaxis: { categories: [], labels: { style: { fontSize: '12px' } } },
  yaxis: { title: { text: 'Unidades' } },
  colors: ['#4F46E5', '#7C3AED', '#EC4899', '#10B981', '#F59E0B', '#3B82F6'],
});

const leadTimeChartOptions = reactive({
  series: [{ name: 'Días Promedio', data: [] }],
  chart: { type: 'bar', height: '100%', toolbar: { show: false } },
  plotOptions: { bar: { horizontal: true, barHeight: '50%' } },
  dataLabels: { 
    enabled: true, 
    textAnchor: 'start', 
    style: { colors: ['#000'] }, 
    offsetX: 0, 
    formatter: (val) => val + " días" 
  },
  xaxis: { categories: [], title: { text: 'Días Promedio de Espera' } },
  yaxis: { labels: { show: true, align: 'right', minWidth: 100, maxWidth: 200 } },
  grid: { xaxis: { lines: { show: true } } },
  tooltip: { x: { show: false } }
});

// ==========================================
// LIFECYCLE
// ==========================================

onMounted(async () => {
  initGemini();
  try {
    await loadJsPdfCdn();
    await loadDashboardData();
  } catch (error) {
    console.error('Error en onMounted:', error);
    globalState.error = "Error al cargar datos.";
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
    empresaConfig.value = data.configuracion || {}; 
    
    Object.assign(kpisData, data.kpis || {});
    
    updateVentasChart(data.ventas_mensuales || []);
    updateLeadTimeChart(data.lead_times || []);
    
    globalState.isLoading = false;
  } catch (err) {
    console.error('Error al cargar dashboard:', err);
    globalState.error = "Error al cargar los datos.";
    globalState.isLoading = false;
  }
};

const updateVentasChart = (data) => {
  if (data?.length) {
    ventasChartOptions.xaxis.categories = data.map(i => 
      new Date(i.time).toLocaleString('es-CL', { month: 'short', year: '2-digit' })
    );
    ventasChartOptions.series[0].data = data.map(i => i.value);
  }
};

const updateLeadTimeChart = (data) => {
  if (data?.length) {
    const sorted = [...data].sort((a, b) => a.avg_lead_time_days - b.avg_lead_time_days);
    leadTimeChartOptions.xaxis.categories = sorted.map(i => i.proveedor__nombre);
    leadTimeChartOptions.series[0].data = sorted.map(i => i.avg_lead_time_days);
  }
};

// ==========================================
// HELPER FUNCTIONS
// ==========================================

const calculateVisualCoverage = (stock, rawDemand) => {
  const roundedDemand = Math.ceil(rawDemand || 0);
  if (roundedDemand <= 0) return '∞'; 
  const coverage = stock / roundedDemand;
  return coverage.toFixed(1);
};

const formatDiasComprar = (dias) => {
  if (dias === null || dias === undefined) return 'N/A';
  if (dias === 0) return '¡AHORA!';
  if (dias < 0) return 'URGENTE';
  return `${dias} días`;
};

const getDiasComprarClass = (dias) => {
  if (dias === null || dias === undefined) return 'text-gray-500';
  if (dias === 0 || dias < 0) return 'text-red-600 font-bold';
  if (dias <= 7) return 'text-orange-600 font-semibold';
  return 'text-gray-900';
};

const getEstadoClass = (estado) => {
  const classes = { 
    'Comprar Ahora': 'bg-red-100 text-red-800', 
    'Revisar Pronto': 'bg-yellow-100 text-yellow-800', 
    'Stock OK': 'bg-green-100 text-green-800', 
    'Sobrestock': 'bg-purple-100 text-purple-800' 
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
// AI GENERATION - SIMPLIFICADA
// ==========================================

const prepararDatosParaIA = () => {
  // ==========================================
  // 📊 KPIs PRINCIPALES
  // ==========================================
  const kpis = {
    cumplimiento: kpisData.tasa_cumplimiento,
    eficiencia: kpisData.eficiencia_stock,
    cobertura_dias: kpisData.dias_cobertura_promedio,
    productos_criticos: kpisData.productos_criticos,
    unidades_sobrestock: kpisData.unidades_sobrestock,
    total_ventas_unidades: kpisData.total_ventas_unidades,
    unidades_totales_stock: kpisData.unidades_totales_stock
  };

  // ==========================================
  // 🚨 PRODUCTOS CRÍTICOS (Top 10 más urgentes)
  // ==========================================
  const productosCriticos = proyecciones.value
    .filter(p => p.estado === 'Comprar Ahora' || p.dias_para_comprar <= 7)
    .map(p => ({
      nombre: p.producto_nombre,
      stock_actual: p.stock_actual,
      demanda_semanal: Math.ceil(p.demanda_semanal_proyectada),
      dias_para_comprar: p.dias_para_comprar,
      cantidad_sugerida: p.cantidad_sugerida || 0,
      estado: p.estado
    }))
    .sort((a, b) => (a.dias_para_comprar || 0) - (b.dias_para_comprar || 0))
    .slice(0, 10); // Solo top 10

  // ==========================================
  // 📦 PRODUCTOS CON SOBRESTOCK (Top 10)
  // ==========================================
  const productosConSobrestock = proyecciones.value
    .filter(p => p.estado === 'Sobrestock')
    .map(p => ({
      nombre: p.producto_nombre,
      stock_actual: p.stock_actual,
      demanda_semanal: Math.ceil(p.demanda_semanal_proyectada),
      cobertura_semanas: p.semanas_cobertura !== null ? parseFloat(p.semanas_cobertura.toFixed(1)) : null
    }))
    .sort((a, b) => b.cobertura_semanas - a.cobertura_semanas)
    .slice(0, 10); // Top 10 con más sobrestock

  // ==========================================
  // 📊 TENDENCIA DE VENTAS
  // ==========================================
  const datosVentas = ventasChartOptions.series[0].data.slice(-6);
  
  const tendenciaVentas = {
    tendencia: calcularTendencia(datosVentas),
    unidades_ultimo_mes: datosVentas[datosVentas.length - 1] || 0
  };

  // ==========================================
  // 📋 RESUMEN POR ESTADO
  // ==========================================
  const resumenPorEstado = {
    'Comprar Ahora': proyecciones.value.filter(p => p.estado === 'Comprar Ahora').length,
    'Revisar Pronto': proyecciones.value.filter(p => p.estado === 'Revisar Pronto').length,
    'Stock OK': proyecciones.value.filter(p => p.estado === 'Stock OK').length,
    'Sobrestock': proyecciones.value.filter(p => p.estado === 'Sobrestock').length
  };

  // ==========================================
  // 🎯 RETORNAR SOLO LO ESENCIAL
  // ==========================================
  return {
    kpis_generales: kpis,
    productos_criticos: productosCriticos,
    productos_sobrestock: productosConSobrestock,
    tendencia_ventas: tendenciaVentas,
    resumen_estados: resumenPorEstado
  };
};

// Helper para calcular tendencia
const calcularTendencia = (datos) => {
  if (!datos || datos.length < 2) {
    console.log('⚠️ Insuficientes datos para calcular tendencia (mínimo 2 meses)');
    return 'ESTABLE';
  }
  
  const ultimo = datos[datos.length - 1];
  
  if (datos.length === 2) {
    const penultimo = datos[datos.length - 2];
    const cambio = ((ultimo - penultimo) / Math.max(penultimo, 1)) * 100;
    
    console.log(`📊 Tendencia (2 meses): ${ultimo} vs ${penultimo} = ${cambio.toFixed(1)}%`);
    
    if (cambio > 10) return 'CRECIENTE';
    if (cambio < -10) return 'DECRECIENTE';
    return 'ESTABLE';
  }
  
  const ultimos2Anteriores = datos.slice(-3, -1);
  const promedio2Meses = ultimos2Anteriores.reduce((a, b) => a + b, 0) / 2;
  const cambio = ((ultimo - promedio2Meses) / Math.max(promedio2Meses, 1)) * 100;
  
  console.log(`📊 Tendencia (3+ meses): Actual=${ultimo} vs Promedio(2 meses anteriores)=${promedio2Meses.toFixed(1)} = ${cambio.toFixed(1)}%`);
  
  if (cambio > 10) return 'CRECIENTE';
  if (cambio < -10) return 'DECRECIENTE';
  return 'ESTABLE';
};

const generarReporteConIA = async () => {
  if (!aiEnabled.value) {
    alert("Gemini AI no está configurado. Por favor verifica tu API key.");
    return;
  }
  
  isGeneratingAI.value = true;
  aiReportContent.value = null;
  
  try {
    const datosOptimizados = prepararDatosParaIA();
    
    let datosFormateados;
    let formatoUsado = 'JSON';

    try {
      if (toonDisponible && toTOON) {
        datosFormateados = toTOON(datosOptimizados);
        formatoUsado = 'TOON';
        console.log('📦 Datos codificados en formato TOON');
      } else {
        datosFormateados = JSON.stringify(datosOptimizados, null, 2);
        console.log('📦 Datos en formato JSON estándar');
      }
    } catch (e) {
      console.warn('Error al codificar, usando JSON:', e);
      datosFormateados = JSON.stringify(datosOptimizados, null, 2);
    }

    const prompt = `Eres un Gerente de Logística Senior con 15+ años de experiencia en retail y distribución. 
Analiza estos datos de inventario y crea un reporte ejecutivo accionable para el dueño del negocio.

**DATOS SIMPLIFICADOS (${formatoUsado}):**
${datosFormateados}

**TU MISIÓN:**
Crear un reporte en español, directo y profesional que el dueño pueda leer en 3 minutos y actuar inmediatamente.

**ESTRUCTURA OBLIGATORIA:**

## 1. 🎯 Estado General del Inventario (3-4 líneas)
- Salud operativa: ¿estamos bien, en riesgo o críticos?
- Tendencia de movimiento: ¿vendemos más o menos que antes?
- Eficiencia general del stock

## 2. 🚨 ALERTAS URGENTES (Acción Inmediata)
Para cada producto crítico:
- **[Nombre Producto]**: 
  - Stock: X unidades | Demanda semanal: Y unidades
  - ⏰ Tiempo hasta agotarse: Z días
  - 📦 Cantidad sugerida: X unidades

*Si NO hay críticos, di: "✅ No hay productos en riesgo inmediato."*

## 3. 📦 Optimización de Bodega (Sobrestock)
Productos que ocupan espacio sin moverse:
- **[Nombre]**: X unidades | Cobertura: Y semanas
- Sugerencia: Oferta / Reasignación / Esperar

*Si no hay: "✅ No hay sobrestock significativo."*

## 4. 💡 Recomendaciones Estratégicas (2-3 puntos)
- Acción prioritaria #1
- Mejora operativa sugerida
- Oportunidad de optimización

**REGLAS DE ORO:**
✅ Usa negritas para productos y números clave
✅ Sé directo: "Debes comprar" no "Podrías considerar"
✅ NUNCA hables de dinero/costos (no tenemos esos datos)
✅ Enfócate en UNIDADES, TIEMPO (días/semanas), ESPACIO (bodega)
✅ Si un campo está vacío/null, no lo menciones
✅ Máximo 800 palabras
✅ Usa emojis para jerarquía visual (🚨📦✅)

**TONO:** Profesional pero cercano, como si hablaras con el dueño en persona.`;

    console.log('📡 Enviando solicitud a Gemini...');
    
    const result = await model.value.generateContent(prompt);
    const response = await result.response;
    aiReportContent.value = response.text();
    
    console.log('✅ Reporte IA generado exitosamente');
    
  } catch (error) {
    console.error('❌ Error al generar reporte IA:', error);
    
    let mensajeError = 'No se pudo generar el reporte inteligente.';
    let detalleError = '';
    
    if (error.message?.includes('429') || error.status === 429) {
      mensajeError = '⏱️ Límite de solicitudes alcanzado';
      detalleError = 'Has superado la cuota de la API de Gemini. Intenta nuevamente en unos minutos.';
    } else if (error.message?.includes('400') || error.status === 400) {
      mensajeError = '⚠️ Solicitud demasiado grande';
      detalleError = 'El inventario es muy extenso. Intenta con menos productos.';
    } else if (error.message?.includes('403') || error.status === 403) {
      mensajeError = '🔑 Error de autenticación';
      detalleError = 'Verifica que tu API Key de Gemini sea válida.';
    } else if (error.message?.includes('network') || !navigator.onLine) {
      mensajeError = '🌐 Error de conexión';
      detalleError = 'Verifica tu conexión a internet.';
    }
    
    aiReportContent.value = `### ${mensajeError}\n\n${detalleError}\n\n*Puedes descargar el reporte básico mientras tanto.*`;
    
    if (error.status === 403 || error.status === 401) {
      alert(`${mensajeError}\n\n${detalleError}`);
    }
    
  } finally {
    isGeneratingAI.value = false;
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
        console.log('✅ jsPDF cargado correctamente');
        resolve();
      };
      
      scriptAutoTable.onerror = () => reject(new Error('Error al cargar autoTable'));
      document.head.appendChild(scriptAutoTable);
    };
    
    scriptJsPdf.onerror = () => reject(new Error('Error al cargar jsPDF'));
    document.head.appendChild(scriptJsPdf);
  });
};

const generarBasePDF = (doc) => {
  doc.setFontSize(20);
  doc.setTextColor(20, 184, 166);
  doc.text('Reporte de Análisis de Inventario', 14, 20);
  
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Generado: ${new Date().toLocaleString('es-CL')}`, 14, 27);
  
  doc.setFontSize(12);
  doc.setTextColor(0);
  doc.text('📊 Indicadores Clave:', 14, 38);
  
  doc.setFontSize(9);
  doc.setTextColor(60);
  const yPos = 44;
  doc.text(`Cumplimiento: ${kpisData.tasa_cumplimiento}%`, 14, yPos);
  doc.text(`Eficiencia: ${kpisData.eficiencia_stock}%`, 70, yPos);
  doc.text(`Críticos: ${kpisData.productos_criticos}`, 130, yPos);
  doc.text(`Cobertura: ${kpisData.dias_cobertura_promedio} días`, 160, yPos);

  const cols = ['Producto', 'Stock', 'Dem/sem', 'Cobertura', 'Días Compra', 'Estado'];
  const rows = proyecciones.value.map(item => [
    item.producto_nombre.substring(0, 30),
    `${item.stock_actual} u.`,
    `${Math.ceil(item.demanda_semanal_proyectada)} u.`,
    calculateVisualCoverage(item.stock_actual, item.demanda_semanal_proyectada),
    formatDiasComprar(item.dias_para_comprar),
    item.estado
  ]);

  doc.autoTable({
    head: [cols],
    body: rows,
    startY: 52,
    theme: 'grid',
    headStyles: { 
      fillColor: [20, 184, 166],
      fontSize: 8,
      fontStyle: 'bold'
    },
    styles: { 
      fontSize: 7,
      cellPadding: 2
    },
    columnStyles: {
      0: { cellWidth: 60 },
      1: { cellWidth: 20 },
      2: { cellWidth: 20 },
      3: { cellWidth: 20 },
      4: { cellWidth: 25 },
      5: { cellWidth: 30 }
    }
  });
};

const descargarReporteBasico = async () => {
  if (globalState.isLoading) {
    alert('Espera a que terminen de cargar los datos.');
    return;
  }
  
  downloading.value = true;
  
  try {
    await loadJsPdfCdn();
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    generarBasePDF(doc);
    
    const fecha = new Date().toISOString().split('T')[0];
    doc.save(`reporte_inventario_${fecha}.pdf`);
    
    console.log('✅ Reporte básico generado');
  } catch (error) {
    console.error('Error al generar PDF:', error);
    alert('Error al generar el PDF. Intenta nuevamente.');
  } finally {
    downloading.value = false;
  }
};

const descargarReporteConIA = async () => {
  if (globalState.isLoading) {
    alert('Espera a que terminen de cargar los datos.');
    return;
  }
  
  await generarReporteConIA();
  
  if (!aiReportContent.value || aiReportContent.value.includes('⏱️') || aiReportContent.value.includes('🔑')) {
    const continuar = confirm('No se pudo generar el análisis IA. ¿Deseas descargar el reporte básico?');
    if (!continuar) return;
  }
  
  downloading.value = true;
  
  try {
    await loadJsPdfCdn();
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    generarBasePDF(doc);
    
    if (aiReportContent.value && !aiReportContent.value.includes('⏱️')) {
      doc.addPage();
      
      doc.setFontSize(16);
      doc.setTextColor(147, 51, 234);
      doc.text('🤖 Análisis Estratégico (IA)', 14, 20);
      
      doc.setFontSize(9);
      doc.setTextColor(0);
      
      const cleanText = aiReportContent.value
        .replace(/\*\*/g, '')
        .replace(/\*/g, '')
        .replace(/#{1,3}\s/g, '')
        .replace(/🚨|⚡|📦/g, '');
      
      const lines = doc.splitTextToSize(cleanText, 180);
      let yPosition = 30;
      const lineHeight = 5;
      const pageHeight = doc.internal.pageSize.height;
      
      lines.forEach(line => {
        if (yPosition > pageHeight - 20) {
          doc.addPage();
          yPosition = 20;
        }
        doc.text(line, 14, yPosition);
        yPosition += lineHeight;
      });
    }
    
    const fecha = new Date().toISOString().split('T')[0];
    doc.save(`reporte_IA_${fecha}.pdf`);
    
    console.log('✅ Reporte con IA generado');
  } catch (error) {
    console.error('Error al generar PDF con IA:', error);
    alert('Error al generar el PDF. Intenta nuevamente.');
  } finally {
    downloading.value = false;
  }
};
</script>