<template>
  <div class="min-h-screen bg-green-50">
     Header con INVEX 
    <div class="bg-white shadow-sm border-b border-green-100">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-teal-600">INVEX</h1>
      </div>
    </div>

     Barra de navegación 
    <div class="bg-teal-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <nav class="flex space-x-1">
          <button 
            v-for="item in navItems" 
            :key="item"
            @click="activeTab = item"
            :class="[
              'px-6 py-3 text-white font-medium transition-colors duration-200',
              activeTab === item 
                ? 'bg-teal-700 border-b-2 border-white' 
                : 'hover:bg-teal-700'
            ]"
          >
            {{ item }}
          </button>
        </nav>
      </div>
    </div>

     Contenido principal 
    <div class="max-w-7xl mx-auto px-4 py-8">
       Título de la sección 
      <div class="mb-8">
        <div class="flex items-center mb-4">
          <div class="w-8 h-8 bg-teal-100 rounded-lg flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-800">Proyecciones de Stock (ASR Predictor)</h2>
        </div>
      </div>

       Gráfico de proyección 
      <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div class="flex items-center mb-4">
          <div class="w-6 h-6 bg-blue-100 rounded flex items-center justify-center mr-3">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-800">Gráfico de Proyección Semanal de Stock</h3>
        </div>
        <p class="text-gray-600 mb-6">Pronóstico de demanda potenciado por IA basado en tendencias estacionales</p>
        
         Placeholder para el gráfico 
        <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
            </svg>
            <p class="text-gray-500 font-medium">Gráfico de Proyecciones</p>
            <p class="text-gray-400 text-sm">Los datos se cargarán aquí</p>
          </div>
        </div>
      </div>

       Tarjetas de alertas 
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
         Alerta Urgente 
        <div class="bg-red-500 text-white rounded-xl p-6 shadow-lg">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <h3 class="text-lg font-bold">Acción Urgente Requerida</h3>
          </div>
          <p class="font-semibold mb-2">Comprar en 5 días</p>
          <p class="text-red-100">El inventario de Ramos de Rosas Rojas se agotará antes de la temporada de San Valentín</p>
        </div>

         Alerta de Riesgo 
        <div class="bg-orange-500 text-white rounded-xl p-6 shadow-lg">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 class="text-lg font-bold">Alerta de Riesgo de Stock</h3>
          </div>
          <p class="font-semibold mb-2">Riesgo de agotarse en 2 semanas</p>
          <p class="text-orange-100">Los disfraces de Halloween muestran señales de alta demanda</p>
          <p class="text-orange-100 mt-1">Orden recomendada: 200 unidades</p>
        </div>

         Oportunidad de Optimización 
        <div class="bg-pink-500 text-white rounded-xl p-6 shadow-lg">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            <h3 class="text-lg font-bold">Oportunidad de Optimización</h3>
          </div>
          <p class="font-semibold mb-2">Reducir sobrestock</p>
          <p class="text-pink-100">Las decoraciones navideñas tienen exceso de inventario</p>
          <p class="text-pink-100 mt-1">Considerar precios promocionales</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('Proyecciones')
const navItems = ['Dashboard', 'Inventario', 'Proyecciones', 'Reportes', 'Usuarios', 'Configuración']
</script>
