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
                item.path === 'reportes.vue'
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

    <!-- Contenido de Reportes -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-6">
        <div class="flex items-center space-x-2 mb-2">
          <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          <h2 class="text-3xl font-bold text-gray-900">Reportes y Análisis</h2>
        </div>
      </div>

      <!-- Cards de KPIs -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Rotación de Inventario -->
        <div class="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg shadow-lg p-6 text-white">
          <h3 class="text-lg font-semibold mb-2">Rotación de Inventario</h3>
          <div class="text-4xl font-bold mb-2">8.5x</div>
          <p class="text-sm opacity-90">Rotación anual</p>
        </div>

        <!-- Días de Cobertura -->
        <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
          <h3 class="text-lg font-semibold mb-2">Días de Cobertura</h3>
          <div class="text-4xl font-bold mb-2">45</div>
          <p class="text-sm opacity-90">Días de stock</p>
        </div>

        <!-- Valor de Sobrestock -->
        <div class="bg-gradient-to-br from-violet-500 to-violet-600 rounded-lg shadow-lg p-6 text-white">
          <h3 class="text-lg font-semibold mb-2">Valor de Sobrestock</h3>
          <div class="text-4xl font-bold mb-2">$12,450</div>
          <p class="text-sm opacity-90">Inventario excedente</p>
        </div>
      </div>

      <!-- Gráficos de Rendimiento -->
      <div class="mb-8">
        <div class="flex items-center space-x-2 mb-4">
          <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
          </svg>
          <h3 class="text-2xl font-bold text-gray-900">Gráficos de Rendimiento</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Gráfico Ventas vs Stock vs Compras -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <div class="text-center mb-4">
              <div class="flex items-center justify-center space-x-2 mb-2">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
                <h4 class="text-lg font-bold text-gray-900">Ventas vs Stock vs Compras</h4>
              </div>
            </div>
            <div class="h-64 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg flex items-center justify-center border-2 border-dashed border-indigo-200">
              <div class="text-center">
                <svg class="w-16 h-16 text-indigo-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
                </svg>
                <p class="text-gray-500 text-sm">Gráfico de barras comparativo</p>
                <p class="text-gray-400 text-xs">Análisis mensual de operaciones</p>
              </div>
            </div>
          </div>

          <!-- Gráfico Tendencias de Demanda Estacional -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <div class="text-center mb-4">
              <div class="flex items-center justify-center space-x-2 mb-2">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                </svg>
                <h4 class="text-lg font-bold text-gray-900">Tendencias de Demanda Estacional</h4>
              </div>
            </div>
            <div class="h-64 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg flex items-center justify-center border-2 border-dashed border-purple-200">
              <div class="text-center">
                <svg class="w-16 h-16 text-purple-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <p class="text-gray-500 text-sm">Gráfico de líneas de tendencia</p>
                <p class="text-gray-400 text-xs">Predicción de patrones estacionales</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Botón Descargar Reporte -->
      <div class="flex justify-center mb-8">
        <button @click="descargarReporte" class="bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 flex items-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <span>Descargar Reporte</span>
        </button>
      </div>

      <!-- Tabla de Análisis Detallado -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-bold text-gray-900">Análisis Detallado por Producto</h3>
        </div>
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Producto
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ventas (mes)
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stock Actual
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rotación
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Valor Inventario
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="producto in productosAnalisis" :key="producto.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ producto.nombre }}</div>
                <div class="text-sm text-gray-500">{{ producto.categoria }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ producto.ventas }} unidades
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ producto.stock }} unidades
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ producto.rotacion }}x
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                ${{ producto.valor.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getEstadoClass(producto.estado)" class="px-2 py-1 text-xs font-semibold rounded-full">
                  {{ producto.estado }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Resumen de Métricas -->
      <div class="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg shadow p-4">
          <div class="text-sm text-gray-500 mb-1">Total Ventas (mes)</div>
          <div class="text-2xl font-bold text-gray-900">1,580</div>
          <div class="text-xs text-green-600 mt-1">↑ 12% vs mes anterior</div>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
          <div class="text-sm text-gray-500 mb-1">Valor Total Inventario</div>
          <div class="text-2xl font-bold text-gray-900">$45,230</div>
          <div class="text-xs text-gray-600 mt-1">En 4 productos</div>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
          <div class="text-sm text-gray-500 mb-1">Productos Críticos</div>
          <div class="text-2xl font-bold text-red-600">2</div>
          <div class="text-xs text-red-600 mt-1">Requieren atención</div>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
          <div class="text-sm text-gray-500 mb-1">Eficiencia Stock</div>
          <div class="text-2xl font-bold text-green-600">87%</div>
          <div class="text-xs text-green-600 mt-1">↑ 5% vs mes anterior</div>
        </div>
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

const productosAnalisis = ref([
  {
    id: 1,
    nombre: 'Ramo de Rosas Rojas',
    categoria: 'Flores Estacionales',
    ventas: 450,
    stock: 45,
    rotacion: 10.0,
    valor: 2250,
    estado: 'Crítico'
  },
  {
    id: 2,
    nombre: 'Disfraz Halloween - Bruja',
    categoria: 'Disfraces',
    ventas: 320,
    stock: 150,
    rotacion: 2.1,
    valor: 7500,
    estado: 'Alerta'
  },
  {
    id: 3,
    nombre: 'Luces Árbol Navidad',
    categoria: 'Decoración Navideña',
    ventas: 480,
    stock: 850,
    rotacion: 0.6,
    valor: 25500,
    estado: 'Sobrestock'
  },
  {
    id: 4,
    nombre: 'Electrónicos Black Friday',
    categoria: 'Tecnología',
    ventas: 330,
    stock: 200,
    rotacion: 1.7,
    valor: 9980,
    estado: 'Normal'
  }
])

const navigateTo = (path) => {
  // En una aplicación real con Vue Router:
  // this.$router.push({ name: path })
  console.log(`Navegando a: ${path}`)
}

const getEstadoClass = (estado) => {
  const classes = {
    'Crítico': 'bg-red-100 text-red-800',
    'Alerta': 'bg-yellow-100 text-yellow-800',
    'Sobrestock': 'bg-purple-100 text-purple-800',
    'Normal': 'bg-green-100 text-green-800'
  }
  return classes[estado] || 'bg-gray-100 text-gray-800'
}

const descargarReporte = () => {
  console.log('Descargando reporte...')
  // Aquí implementarías la lógica para generar y descargar el reporte
  alert('Generando reporte PDF...')
}
</script>