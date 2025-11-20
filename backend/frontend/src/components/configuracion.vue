<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center space-x-3">
        <svg class="w-8 h-8 text-teal-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-1.025 1.11-1.11a1.25 1.25 0 0 1 1.413 1.412c-.09.542-.56 1.025-1.11 1.11a1.25 1.25 0 0 1-1.413-1.412zM10.343 3.94a14.25 14.25 0 0 0-9.332 6.007c-.427.69-.427 1.646 0 2.336a14.25 14.25 0 0 0 9.332 6.007c.427.108.857.108 1.284 0a14.25 14.25 0 0 0 9.332-6.007c.427-.69.427-1.646 0-2.336a14.25 14.25 0 0 0-9.332-6.007c-.427-.108-.857-.108-1.284 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
        </svg>
        <h2 class="text-3xl font-bold text-gray-900">Configuración del Sistema</h2>
      </div>
      <p class="text-gray-600 mt-2 text-sm sm:text-base">
        Personaliza parámetros del sistema y fechas clave para tu negocio.
      </p>
    </div>

    <!-- 🆕 NUEVA SECCIÓN: Parámetros de Inventario -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Parámetros de Inventario</h3>
      </div>
      <p class="text-gray-600 text-sm sm:text-base mb-6">
        Ajusta los parámetros que InveX usa para calcular cuándo comprar y cuánto stock mantener.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <!-- Semanas de Seguridad -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Semanas de Seguridad
            <span class="text-gray-500 font-normal">(1-12)</span>
          </label>
          <input 
            v-model.number="configuracion.semanas_seguridad" 
            type="number" 
            min="1" 
            max="12"
            class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none"
          />
          <p class="text-xs text-gray-500 mt-1">
            Stock mínimo antes de generar alerta de compra
          </p>
        </div>

        <!-- Semanas Objetivo -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Semanas Objetivo
            <span class="text-gray-500 font-normal">(1-52)</span>
          </label>
          <input 
            v-model.number="configuracion.semanas_objetivo" 
            type="number" 
            min="1" 
            max="52"
            class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none"
          />
          <p class="text-xs text-gray-500 mt-1">
            Cantidad objetivo de stock al realizar una compra
          </p>
        </div>

        <!-- Días de Análisis -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Días de Análisis
            <span class="text-gray-500 font-normal">(30-365)</span>
          </label>
          <input 
            v-model.number="configuracion.dias_analisis_demanda" 
            type="number" 
            min="30" 
            max="365"
            class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none"
          />
          <p class="text-xs text-gray-500 mt-1">
            Días históricos para calcular demanda promedio
          </p>
        </div>
      </div>

      <!-- Botón para guardar configuración -->
      <div class="flex justify-end">
        <button 
          @click="guardarConfiguracion"
          :disabled="guardandoConfig"
          class="bg-teal-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-teal-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ guardandoConfig ? 'Guardando...' : 'Guardar Configuración' }}
        </button>
      </div>

      <!-- Información adicional -->
      <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="flex items-start space-x-3">
          <svg class="w-5 h-5 text-blue-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="text-sm text-blue-800">
            <p class="font-semibold mb-1">¿Cómo funcionan estos parámetros?</p>
            <ul class="list-disc list-inside space-y-1 text-xs">
              <li><strong>Semanas de Seguridad:</strong> Si tu stock cubre menos que esto, verás una alerta "Comprar Ahora"</li>
              <li><strong>Semanas Objetivo:</strong> InveX calculará cuánto comprar para alcanzar este nivel de cobertura</li>
              <li><strong>Días de Análisis:</strong> Periodo histórico usado para calcular tu demanda promedio</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Sección de Fechas Especiales (sin cambios) -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m4 8H4m16 8H4m1-4h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Fechas Especiales Personalizadas</h3>
      </div>
      <p class="text-gray-600 text-sm sm:text-base mb-4">
        Agrega fechas importantes para tener un mejor registro de los eventos que afectan tu inventario.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <input v-model="nuevoEvento.nombre" type="text" placeholder="Nombre del evento"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
        <input v-model="nuevoEvento.fecha" type="date"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
        <input v-model="nuevoEvento.descripcion" type="text" placeholder="Descripción (Ej: Aumento en ventas)"
          class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 focus:border-teal-400 outline-none" />
      </div>
      <div class="flex justify-end"><!-- -->
        <button @click="agregarOEditarFecha"
          class="bg-teal-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-teal-600 transition">
          {{ editId === null ? '+ Agregar Fecha' : 'Guardar Cambios' }}
        </button>
      </div>

      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"> <!--  -->
        <div v-for="evento in fechasEspeciales" :key="evento.id" class="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
          <div class="flex items-center mb-1">
            <span class="text-2xl mr-2">{{ obtenerIconoParaEvento(evento.nombre) }}</span>
            <h4 class="font-bold text-lg text-gray-800">{{ evento.nombre }}</h4>
          </div>
          <p class="text-sm text-gray-600"><strong>Fecha:</strong> {{ evento.fecha }}</p>
          <p class="text-sm text-gray-600"><strong>Descripción:</strong> {{ evento.descripcion || 'Sin descripción' }}</p>
          <div class="flex gap-4 mt-3"> <!-- -->
            <button @click="editarEvento(evento)" class="font-medium text-teal-600 hover:text-teal-700">
              Editar
            </button>
            <button @click="eliminarEvento(evento)" class="font-medium text-rose-600 hover:text-rose-700">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>//
import { ref, onMounted } from 'vue'
import axiosInstance from '@/api/axios.js'
import Swal from 'sweetalert2'

// --- ESTADO DEL COMPONENTE ---
const fechasEspeciales = ref([])
const nuevoEvento = ref({ nombre: '', fecha: '', descripcion: '' })
const editId = ref(null)

// 🆕 Estado para configuración de inventario
const configuracion = ref({
  semanas_seguridad: 2,
  semanas_objetivo: 4,
  dias_analisis_demanda: 90
})
const guardandoConfig = ref(false)

// --- LÓGICA DE CONFIGURACIÓN ---

// 🆕 Cargar configuración actual
const cargarConfiguracion = async () => {
  try {
    const response = await axiosInstance.get('/empresa/configuracion/');
    configuracion.value = {
      semanas_seguridad: response.data.semanas_seguridad,
      semanas_objetivo: response.data.semanas_objetivo,
      dias_analisis_demanda: response.data.dias_analisis_demanda
    };
  } catch (error) {
    console.error('Error al cargar configuración:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error al cargar configuración',
      text: 'No se pudo obtener la configuración actual.',
      confirmButtonColor: '#0d9488'
    });
  }
};

// 🆕 Guardar configuración
const guardarConfiguracion = async () => {
  // Validaciones básicas
  if (configuracion.value.semanas_seguridad < 1 || configuracion.value.semanas_seguridad > 12) {
    Swal.fire({ 
      icon: 'warning', 
      title: 'Valor inválido', 
      text: 'Las semanas de seguridad deben estar entre 1 y 12.',
      confirmButtonColor: '#0d9488'
    });
    return;
  }

  if (configuracion.value.semanas_objetivo < configuracion.value.semanas_seguridad) {
    Swal.fire({ 
      icon: 'warning', 
      title: 'Valor inválido', 
      text: 'Las semanas objetivo deben ser mayores o iguales a las semanas de seguridad.',
      confirmButtonColor: '#0d9488'
    });
    return;
  }

  guardandoConfig.value = true;

  try {
    await axiosInstance.patch('/empresa/configuracion/', configuracion.value);
    Swal.fire({ 
      icon: 'success', 
      title: '¡Configuración guardada!', 
      text: 'Los nuevos parámetros se aplicarán en los próximos cálculos.',
      toast: true, 
      position: 'top-end', 
      showConfirmButton: false, 
      timer: 3000 
    });
  } catch (error) {
    const errorMsg = error.response?.data?.semanas_objetivo?.[0] || 
                     error.response?.data?.detail || 
                     'Ocurrió un problema al guardar la configuración.';
    Swal.fire({ 
      icon: 'error', 
      title: 'Error al guardar', 
      text: errorMsg,
      confirmButtonColor: '#0d9488'
    });
  } finally {
    guardandoConfig.value = false;
  }
};

// --- LÓGICA DE FECHAS ESPECIALES (sin cambios) ---

const cargarFechas = async () => {
  try {
    const response = await axiosInstance.get('/dias-importantes/');//
    fechasEspeciales.value = response.data.map(evento => ({
      id: evento.id,
      nombre: evento.nombre_evento,
      fecha: evento.fecha,
      descripcion: evento.descripcion
    }));
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error al cargar las fechas',
      text: 'No se pudo conectar con el servidor. Intenta de nuevo más tarde.',
      confirmButtonColor: '#0d9488'
    });
  }
};
//
onMounted(() => {
  cargarFechas();
  cargarConfiguracion(); // 🆕 Cargar configuración al montar
});
//
const agregarOEditarFecha = async () => {
  if (!nuevoEvento.value.nombre || !nuevoEvento.value.fecha) {
    Swal.fire({ icon: 'warning', title: '¡Ups!', text: 'El nombre y la fecha son obligatorios.' });
    return;
  }
//
  const payload = {
      nombre_evento: nuevoEvento.value.nombre,
      fecha: nuevoEvento.value.fecha,
      descripcion: nuevoEvento.value.descripcion,
  };

  try {
    if (editId.value !== null) {  
      await axiosInstance.patch(`/dias-importantes/${editId.value}/`, payload);
      Swal.fire({ icon: 'success', title: '¡Evento actualizado!', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    } else {  
      await axiosInstance.post('/dias-importantes/', payload);
      Swal.fire({ icon: 'success', title: '¡Evento agregado!', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    }

    nuevoEvento.value = { nombre: '', fecha: '', descripcion: '' };
    editId.value = null;
    await cargarFechas();

  } catch (error) { 
    const errorMsg = error.response?.data?.detail || 'Ocurrió un problema al guardar el evento.';
    Swal.fire({ icon: 'error', title: 'Error al guardar', text: errorMsg });
  }
};

const editarEvento = (evento) => {  
  nuevoEvento.value = { ...evento };
  editId.value = evento.id;
};

const eliminarEvento = (evento) => {
  Swal.fire({
    title: `¿Eliminar "${evento.nombre}"?`,
    text: "Esta acción no se puede deshacer.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#e11d48',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Sí, ¡eliminar!',
    cancelButtonText: 'Cancelar'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await axiosInstance.delete(`/dias-importantes/${evento.id}/`);
        Swal.fire({ title: '¡Eliminado!', text: 'El evento ha sido eliminado.', icon: 'success', timer: 1500, showConfirmButton: false });
        await cargarFechas();
      } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error al eliminar', text: 'No se pudo eliminar el evento.' });
      }
    }
  });
};

const obtenerIconoParaEvento = (nombreEvento) => {
  const nombreEnMinusculas = nombreEvento.toLowerCase();
  if (nombreEnMinusculas.includes('halloween')) return '🎃';
  if (nombreEnMinusculas.includes('san valentín') || nombreEnMinusculas.includes('amor')) return '💖';
  if (nombreEnMinusculas.includes('navidad')) return '🎄';
  if (nombreEnMinusculas.includes('año nuevo')) return '🎆';
  if (nombreEnMinusculas.includes('pascua')) return '🐰';
  if (nombreEnMinusculas.includes('aniversario')) return '🎉';
  if (nombreEnMinusculas.includes('día de la madre')) return '💐';
  if (nombreEnMinusculas.includes('día del padre')) return '👔';
  if (nombreEnMinusculas.includes('día del niño')) return '🎁';
  if (nombreEnMinusculas.includes('cyber') || nombreEnMinusculas.includes('black friday')) return '💻';
  if (nombreEnMinusculas.includes('oferta') || nombreEnMinusculas.includes('liquidación')) return '💸';
  if (nombreEnMinusculas.includes('lanzamiento') || nombreEnMinusculas.includes('nuevo')) return '✨';
  if (nombreEnMinusculas.includes('primavera')) return '🌸';
  if (nombreEnMinusculas.includes('verano')) return '☀️';
  if (nombreEnMinusculas.includes('otoño')) return '🍂';
  if (nombreEnMinusculas.includes('invierno')) return '❄️';
  if (nombreEnMinusculas.includes('escolar') || nombreEnMinusculas.includes('vuelta a clases')) return '🎒';
  if (nombreEnMinusculas.includes('fiestas patrias') || nombreEnMinusculas.includes('dieciocho')) return '🇨🇱';
  return '📅';
};
</script>

<style scoped> 
input[type="date"]:not(:focus):invalid {
  color: #9ca3af;
}
</style> 