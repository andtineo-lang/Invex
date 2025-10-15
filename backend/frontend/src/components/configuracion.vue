<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-1.025 1.11-1.11a1.25 1.25 0 0 1 1.413 1.412c-.09.542-.56 1.025-1.11 1.11a1.25 1.25 0 0 1-1.413-1.412zM10.343 3.94a14.25 14.25 0 0 0-9.332 6.007c-.427.69-.427 1.646 0 2.336a14.25 14.25 0 0 0 9.332 6.007c.427.108.857.108 1.284 0a14.25 14.25 0 0 0 9.332-6.007c.427-.69.427-1.646 0-2.336a14.25 14.25 0 0 0-9.332-6.007c-.427-.108-.857-.108-1.284 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Configuración del Sistema</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        Personaliza parámetros del sistema, fechas clave y reglas de proyección de inventario.
      </p>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m4 8H4m16 8H4m1-4h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Fechas Especiales Personalizadas</h3>
      </div>
      <p class="text-gray-600 text-sm sm:text-base mb-4">
        Agrega fechas importantes para ajustar proyecciones automáticas del sistema.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <input v-model="nuevoEvento.nombre" type="text" placeholder="Nombre del evento"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
        <input v-model="nuevoEvento.fecha" type="date"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
        <input v-model="nuevoEvento.impacto" type="text" placeholder="Impacto esperado (+25%)"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
        <input v-model="nuevoEvento.categoria" type="text" placeholder="Categoría (Ej: Ropa)"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
      </div>
      <div class="flex justify-end">
        <button @click="agregarFecha"
          class="bg-teal-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-teal-600 transition">
          + Agregar Fecha
        </button>
      </div>

      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="(evento, index) in fechasEspeciales" :key="index" class="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
          <div class="flex items-center mb-1">
            <span class="text-2xl mr-2">{{ obtenerIconoParaEvento(evento.nombre) }}</span>
            <h4 class="font-bold text-lg text-gray-800">{{ evento.nombre }}</h4>
          </div>
          <p class="text-sm text-gray-600"><strong>Fecha:</strong> {{ evento.fecha }}</p>
          <p class="text-sm text-gray-600"><strong>Impacto:</strong> {{ evento.impacto }}</p>
          <p class="text-sm text-gray-600"><strong>Categoría:</strong> {{ evento.categoria }}</p>
          <div class="flex gap-4 mt-3">
            <button @click="editarEvento(index)" class="font-medium text-teal-600 hover:text-teal-700">
              Editar
            </button>
            <button @click="eliminarEvento(index)" class="font-medium text-rose-600 hover:text-rose-700">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Configuración de Predicciones</h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Horizonte de Pronóstico</label>
          <select v-model="horizontePronostico" class="border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none">
            <option value="1 mes">1 mes</option>
            <option value="3 meses">3 meses</option>
            <option value="6 meses">6 meses</option>
            <option value="12 meses">12 meses</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nivel de Stock de Seguridad (%)</label>
          <input v-model.number="stockSeguridad" type="number"
            class="border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
          <p class="text-xs text-gray-500 mt-1">Porcentaje de la demanda promedio para mantener como reserva.</p>
        </div>
      </div>
      <div class="mt-8 flex justify-end">
        <button @click="guardarConfiguracion"
          class="bg-teal-500 text-white px-6 py-2 rounded-md font-semibold hover:bg-teal-600 transition">
          Guardar Configuración
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// CAMBIO AQUÍ: Datos simulados actualizados para incluir más ejemplos
const fechasEspeciales = ref([
  { nombre: 'San Valentín', fecha: '2026-02-14', impacto: '+40% ventas', categoria: 'Regalos y Flores' },
  { nombre: 'Halloween', fecha: '2025-10-31', impacto: '+60% ventas', categoria: 'Disfraces y Dulces' },
  { nombre: 'Navidad', fecha: '2025-12-25', impacto: '+80% ventas', categoria: 'Decoración y Regalos' },
  { nombre: 'Aniversario de la Empresa', fecha: '2026-03-15', impacto: '+25% ventas', categoria: 'Corporativo' },
])

const nuevoEvento = ref({ nombre: '', fecha: '', impacto: '', categoria: '' })
const horizontePronostico = ref('3 meses')
const stockSeguridad = ref(15)
const editIndex = ref(null)

// ---
// CAMBIO AQUÍ: Nueva función para obtener el ícono
// ---
const obtenerIconoParaEvento = (nombreEvento) => {
  const nombreEnMinusculas = nombreEvento.toLowerCase();

  // --- Festividades Comunes ---
  if (nombreEnMinusculas.includes('halloween')) return '🎃';
  if (nombreEnMinusculas.includes('san valentín') || nombreEnMinusculas.includes('amor')) return '💖';
  if (nombreEnMinusculas.includes('navidad')) return '🎄';
  if (nombreEnMinusculas.includes('año nuevo')) return '🎆';
  if (nombreEnMinusculas.includes('pascua')) return '🐰';

  // --- Eventos Personales o Corporativos ---
  if (nombreEnMinusculas.includes('aniversario')) return '🎉';
  if (nombreEnMinusculas.includes('día de la madre')) return '💐';
  if (nombreEnMinusculas.includes('día del padre')) return '👔';
  if (nombreEnMinusculas.includes('día del niño')) return '🎁';

  // --- Eventos de Venta (Retail / E-commerce) ---
  if (nombreEnMinusculas.includes('cyber') || nombreEnMinusculas.includes('black friday')) return '💻';
  if (nombreEnMinusculas.includes('oferta') || nombreEnMinusculas.includes('liquidación') || nombreEnMinusculas.includes('remate')) return '💸';
  if (nombreEnMinusculas.includes('lanzamiento') || nombreEnMinusculas.includes('nuevo')) return '✨';
  
  // --- Temporadas (Moda / General) ---
  if (nombreEnMinusculas.includes('primavera')) return '🌸';
  if (nombreEnMinusculas.includes('verano')) return '☀️';
  if (nombreEnMinusculas.includes('otoño')) return '🍂';
  if (nombreEnMinusculas.includes('invierno')) return '❄️';

  // --- Específicos de Industria ---
  if (nombreEnMinusculas.includes('escolar') || nombreEnMinusculas.includes('vuelta a clases')) return '🎒';
  if (nombreEnMinusculas.includes('libro') || nombreEnMinusculas.includes('lectura')) return '📚';
  if (nombreEnMinusculas.includes('gamer') || nombreEnMinusculas.includes('videojuego')) return '🎮';
  if (nombreEnMinusculas.includes('vino') || nombreEnMinusculas.includes('vendimia')) return '🍷';
  if (nombreEnMinusculas.includes('cerveza') || nombreEnMinusculas.includes('oktoberfest')) return '🍺';
  
  // --- Festividades Nacionales (Ej: Chile) ---
  if (nombreEnMinusculas.includes('fiestas patrias') || nombreEnMinusculas.includes('dieciocho') || nombreEnMinusculas.includes('18')) return '1️⃣8️⃣🎉';

  // Ícono por defecto si no encuentra ninguna palabra clave
  return '📅';
};


const agregarFecha = () => {
  if (!nuevoEvento.value.nombre || !nuevoEvento.value.fecha) {
    alert('Por favor, completa el nombre y la fecha del evento.')
    return
  }
  if (editIndex.value !== null) {
    fechasEspeciales.value[editIndex.value] = { ...nuevoEvento.value };
    editIndex.value = null;
  } else {
    fechasEspeciales.value.push({ ...nuevoEvento.value });
  }
  nuevoEvento.value = { nombre: '', fecha: '', impacto: '', categoria: '' };
}

const editarEvento = (index) => {
  nuevoEvento.value = { ...fechasEspeciales.value[index] };
  editIndex.value = index;
}

const eliminarEvento = (index) => {
  if (confirm(`¿Seguro que deseas eliminar el evento "${fechasEspeciales.value[index].nombre}"?`)) {
    fechasEspeciales.value.splice(index, 1)
  }
}

const guardarConfiguracion = () => {
  alert(`Configuración guardada:\n- Horizonte de pronóstico: ${horizontePronostico.value}\n- Stock de seguridad: ${stockSeguridad.value}%`);
}
</script>