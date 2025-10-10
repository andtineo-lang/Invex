<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-6">
      <div class="flex items-center space-x-2 mb-2">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Reportes y Análisis</h2>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Rotación de Inventario</h3>
        <div class="text-4xl font-bold mb-2">{{ kpiRotacionTotal.toFixed(1) }}x</div>
        <p class="text-sm opacity-90">Rotación mensual promedio</p>
      </div>
      <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Días de Cobertura</h3>
        <div class="text-4xl font-bold mb-2">{{ kpiDiasCobertura.toFixed(0) }}</div>
        <p class="text-sm opacity-90">Días promedio de stock</p>
      </div>
      <div class="bg-gradient-to-br from-violet-500 to-violet-600 rounded-lg shadow-lg p-6 text-white">
        <h3 class="text-lg font-semibold mb-2">Valor de Sobrestock</h3>
        <div class="text-4xl font-bold mb-2">${{ kpiValorSobrestock.toLocaleString() }}</div>
        <p class="text-sm opacity-90">Inventario excedente</p>
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
          <h4 class="text-lg font-bold text-gray-900 mb-4">Ventas vs Stock vs Compras</h4>
          <VueApexCharts type="bar" height="250" :options="barChartData.chartOptions" :series="barChartData.series" />
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h4 class="text-lg font-bold text-gray-900 mb-4">Tendencias de Demanda Estacional</h4>
          <VueApexCharts type="area" height="250" :options="lineChartData.chartOptions" :series="lineChartData.series" />
        </div>
      </div>
    </div>

    <div class="flex justify-center mb-8">
      <button @click="descargarReporte" class="bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2">
        <span>Descargar Reporte</span>
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-bold text-gray-900">Análisis Detallado por Producto</h3>
      </div>
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ventas (mes)</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Actual</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rotación</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor Inventario</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="producto in productosProcesados" :key="producto.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900">{{ producto.nombre }}</div>
              <div class="text-sm text-gray-500">{{ producto.categoria }}</div>
            </td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ producto.ventasMensuales }} u.</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ producto.stockActual }} u.</td>
            <td class="px-6 py-4 text-sm text-gray-900">{{ producto.rotacion.toFixed(1) }}x</td>
            <td class="px-6 py-4 text-sm font-medium text-gray-900">${{ producto.valorInventario.toLocaleString() }}</td>
            <td class="px-6 py-4">
              <span :class="getEstadoClass(producto.estado)" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ producto.estado }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Total Ventas (mes)</div>
        <div class="text-2xl font-bold text-gray-900">{{ resumenTotalVentas }}</div>
        <div class="text-xs text-green-600 mt-1">↑ 12% vs mes anterior</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Valor Total Inventario</div>
        <div class="text-2xl font-bold text-gray-900">${{ resumenValorTotalInventario.toLocaleString() }}</div>
        <div class="text-xs text-gray-600 mt-1">En {{ reportesData.length }} productos</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Productos Críticos</div>
        <div class="text-2xl font-bold text-red-600">{{ resumenProductosCriticos }}</div>
        <div class="text-xs text-red-600 mt-1">Requieren atención</div>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 mb-1">Eficiencia Stock</div>
        <div class="text-2xl font-bold text-green-600">{{ resumenEficienciaStock.toFixed(0) }}%</div>
        <div class="text-xs text-green-600 mt-1">↑ 5% vs mes anterior</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

// --- DATOS CRUDOS ---
// Esto es lo único que necesitarás reemplazar con los datos de tu API/BD.
const reportesData = ref([
  { id: 1, nombre: 'Ramo de Rosas Rojas', categoria: 'Flores Estacionales', ventasMensuales: 450, stockActual: 45, costoUnitario: 5, comprasMensuales: 400, ventasHistoricas: [120, 150, 200, 180, 250, 450] },
  { id: 2, nombre: 'Disfraz Halloween - Bruja', categoria: 'Disfraces', ventasMensuales: 320, stockActual: 150, costoUnitario: 50, comprasMensuales: 300, ventasHistoricas: [50, 80, 70, 150, 220, 320] },
  { id: 3, nombre: 'Luces Árbol Navidad', categoria: 'Decoración Navideña', ventasMensuales: 480, stockActual: 850, costoUnitario: 30, comprasMensuales: 500, ventasHistoricas: [80, 110, 130, 200, 350, 480] },
  { id: 4, nombre: 'Electrónicos Black Friday', categoria: 'Tecnología', ventasMensuales: 330, stockActual: 200, costoUnitario: 49.9, comprasMensuales: 350, ventasHistoricas: [90, 120, 150, 180, 280, 330] }
]);

// --- LÓGICA DE PROCESAMIENTO (CÁLCULOS POR PRODUCTO) ---
const productosProcesados = computed(() => {
  return reportesData.value.map(p => {
    const valorInventario = p.stockActual * p.costoUnitario;
    const rotacion = p.stockActual > 0 ? p.ventasMensuales / p.stockActual : 0;
    
    let estado = 'Normal';
    if (rotacion > 5) estado = 'Crítico';
    else if (rotacion < 1) estado = 'Sobrestock';
    else if (rotacion < 2) estado = 'Alerta';

    return { ...p, valorInventario, rotacion, estado };
  });
});

// --- LÓGICA PARA KPIs Y MÉTRICAS (CÁLCULOS GLOBALES) ---
const kpiRotacionTotal = computed(() => {
    const totalVentas = reportesData.value.reduce((sum, p) => sum + p.ventasMensuales, 0);
    const totalStock = reportesData.value.reduce((sum, p) => sum + p.stockActual, 0);
    return totalStock > 0 ? totalVentas / totalStock : 0;
});
const kpiDiasCobertura = computed(() => (1 / kpiRotacionTotal.value) * 30);
const kpiValorSobrestock = computed(() => productosProcesados.value
    .filter(p => p.estado === 'Sobrestock')
    .reduce((sum, p) => sum + p.valorInventario, 0));

const resumenTotalVentas = computed(() => productosProcesados.value.reduce((sum, p) => sum + p.ventasMensuales, 0));
const resumenValorTotalInventario = computed(() => productosProcesados.value.reduce((sum, p) => sum + p.valorInventario, 0));
const resumenProductosCriticos = computed(() => productosProcesados.value.filter(p => p.estado === 'Crítico').length);
const resumenEficienciaStock = computed(() => {
    const totalStock = productosProcesados.value.reduce((sum, p) => sum + p.stockActual, 0);
    return (resumenTotalVentas.value / (resumenTotalVentas.value + totalStock)) * 100;
});

// --- DATOS PARA GRÁFICOS ---
const barChartData = computed(() => ({
  series: [
    { name: 'Ventas', data: productosProcesados.value.map(p => p.ventasMensuales) },
    { name: 'Stock', data: productosProcesados.value.map(p => p.stockActual) },
    { name: 'Compras', data: productosProcesados.value.map(p => p.comprasMensuales) },
  ],
  chartOptions: {
    chart: { type: 'bar', height: 250, toolbar: { show: false } },
    plotOptions: { bar: { horizontal: false, columnWidth: '60%', endingShape: 'rounded' } },
    dataLabels: { enabled: false },
    stroke: { show: true, width: 2, colors: ['transparent'] },
    xaxis: { categories: productosProcesados.value.map(p => p.nombre) },
    fill: { opacity: 1 },
    colors: ['#4f46e5', '#a855f7', '#7c3aed'], // Indigo, Purple, Violet
  },
}));

const lineChartData = computed(() => ({
  series: [
    { name: 'Rosas Rojas', data: reportesData.value.find(p=>p.id===1)?.ventasHistoricas },
    { name: 'Luces Navidad', data: reportesData.value.find(p=>p.id===3)?.ventasHistoricas },
  ],
  chartOptions: {
    chart: { type: 'area', height: 250, toolbar: { show: false }, zoom: { enabled: false } },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth' },
    xaxis: { categories: ['May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct'] },
    colors: ['#ec4899', '#8b5cf6'], // Pink, Violet
  },
}));

// --- FUNCIONES AUXILIARES ---
const getEstadoClass = (estado) => {
  const classes = {
    'Crítico': 'bg-red-100 text-red-800',
    'Alerta': 'bg-yellow-100 text-yellow-800',
    'Sobrestock': 'bg-purple-100 text-purple-800',
    'Normal': 'bg-green-100 text-green-800'
  };
  return classes[estado] || 'bg-gray-100 text-gray-800';
};

const descargarReporte = () => {
  alert('Generando reporte PDF...');
};
</script>

<style scoped>
/* Estilos específicos para este componente si son necesarios */
</style>