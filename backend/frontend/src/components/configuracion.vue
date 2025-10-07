<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Encabezado -->
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Configuración del Sistema</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        Personaliza parámetros del sistema, fechas clave y reglas de proyección de inventario.
      </p>
    </div>

    <!-- Sección: Fechas Especiales -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3M5 11h14M5 19h14" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Fechas Especiales Personalizadas</h3>
      </div>
      <p class="text-gray-600 text-sm sm:text-base mb-4">
        Agrega fechas importantes para ajustar proyecciones automáticas del sistema.
      </p>

      <!-- Formulario -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <input v-model="nuevoEvento.nombre" type="text" placeholder="Nombre del evento"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-500 outline-none" />
        <input v-model="nuevoEvento.fecha" type="date"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-500 outline-none" />
        <input v-model="nuevoEvento.impacto" type="text" placeholder="Impacto esperado (+25%)"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-500 outline-none" />
        <input v-model="nuevoEvento.categoria" type="text" placeholder="Categoría"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-500 outline-none" />
      </div>
      <div class="flex justify-end">
        <button @click="agregarFecha"
          class="bg-teal-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-teal-700 transition">
          + Agregar Fecha
        </button>
      </div>

      <!-- Lista de eventos -->
      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="(evento, index) in fechasEspeciales" :key="index" class="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
          <h4 class="font-bold text-lg text-gray-800 mb-1">{{ evento.nombre }}</h4>
          <p class="text-sm text-gray-700"><strong>📅 Fecha:</strong> {{ evento.fecha }}</p>
          <p class="text-sm text-gray-700"><strong>📈 Impacto:</strong> {{ evento.impacto }}</p>
          <p class="text-sm text-gray-700"><strong>🏷️ Categoría:</strong> {{ evento.categoria }}</p>
          <div class="flex flex-col sm:flex-row gap-2 mt-3">
            <button @click="editarEvento(index)" class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">
              Editar
            </button>
            <button @click="eliminarEvento(index)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Configuración de Predicciones -->
    <div class="bg-white rounded-lg shadow-lg p-6">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Configuración de Predicciones</h3>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Horizonte de Pronóstico</label>
          <select v-model="horizontePronostico" class="border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-teal-500 outline-none">
            <option value="1 mes">1 mes</option>
            <option value="3 meses">3 meses</option>
            <option value="6 meses">6 meses</option>
            <option value="12 meses">12 meses</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Stock de Seguridad (%)</label>
          <input v-model.number="stockSeguridad" type="number"
            class="border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-teal-500 outline-none" />
          <p class="text-xs text-gray-500 mt-1">Porcentaje de la demanda promedio para mantener como reserva</p>
        </div>
      </div>

      <div class="mt-6 flex justify-center">
        <button
          @click="guardarConfiguracion"
          class="bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105"
        >
          Guardar Configuración
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Fechas simuladas
const fechasEspeciales = ref([
  { nombre: '🎉 Aniversario de la Empresa', fecha: '2024-03-15', impacto: '+25% ventas', categoria: 'Eventos corporativos' },
  { nombre: '🎃 Halloween', fecha: '2024-10-31', impacto: '+60% ventas', categoria: 'Temporada festiva' },
  { nombre: '🎄 Navidad', fecha: '2024-12-25', impacto: '+80% ventas', categoria: 'Decoración y regalos' }
])

const nuevoEvento = ref({ nombre: '', fecha: '', impacto: '', categoria: '' })
const horizontePronostico = ref('3 meses')
const stockSeguridad = ref(15)

// Funciones simuladas
const agregarFecha = () => {
  if (!nuevoEvento.value.nombre || !nuevoEvento.value.fecha) {
    alert('Por favor completa los campos obligatorios.')
    return
  }
  fechasEspeciales.value.push({ ...nuevoEvento.value })
  nuevoEvento.value = { nombre: '', fecha: '', impacto: '', categoria: '' }
}

const editarEvento = (index) => {
  nuevoEvento.value = { ...fechasEspeciales.value[index] }
  fechasEspeciales.value.splice(index, 1)
}

const eliminarEvento = (index) => {
  if (confirm('¿Seguro que deseas eliminar este evento?')) {
    fechasEspeciales.value.splice(index, 1)
  }
}

const guardarConfiguracion = () => {
  alert(`Configuración guardada:\n- Horizonte: ${horizontePronostico.value}\n- Stock Seguridad: ${stockSeguridad.value}%`)
}
</script>
