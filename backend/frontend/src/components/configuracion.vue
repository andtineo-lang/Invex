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
        Personaliza el cerebro de InveX para adaptarlo a tu negocio.
      </p>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Estrategia de Stock (Básica)</h3>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Semanas de Seguridad</label>
          <input v-model.number="configuracion.semanas_seguridad" type="number" min="1" max="12" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none"/>
          <p class="text-xs text-gray-500 mt-1">Tu "colchón". Stock mínimo para dormir tranquilo.</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Semanas Objetivo</label>
          <input v-model.number="configuracion.semanas_objetivo" type="number" min="1" max="52" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none"/>
          <p class="text-xs text-gray-500 mt-1">Cantidad ideal de stock al hacer una compra grande.</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Días de Análisis</label>
          <input v-model.number="configuracion.dias_analisis_demanda" type="number" min="30" max="365" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none"/>
          <p class="text-xs text-gray-500 mt-1">Historial usado para calcular tu promedio de ventas.</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-8 border-t-4 border-orange-400">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Semáforos y Alertas</h3>
      </div>
      <p class="text-gray-600 text-sm sm:text-base mb-6">Define cuándo el sistema debe considerar un producto "Muerto" o "Sobrestockeado".</p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Demanda Mínima (u/sem)</label>
          <input v-model.number="configuracion.umbral_demanda_minima" type="number" step="0.1" min="0" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-orange-400 outline-none bg-orange-50"/>
          <p class="text-xs text-gray-500 mt-1">Si vende menos que esto, el sistema no sugerirá compras (Producto Lento).</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Alerta Sobrestock (Semanas)</label>
          <input v-model.number="configuracion.umbral_sobrestock_semanas" type="number" min="4" max="52" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-orange-400 outline-none bg-orange-50"/>
          <p class="text-xs text-gray-500 mt-1">Si tienes stock para más de estas semanas, se marca como "Exceso".</p>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-8 border-t-4 border-indigo-500">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Logística Avanzada</h3>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Lead Time Máximo (Días)</label>
          <input v-model.number="configuracion.max_lead_time_razonable" type="number" min="15" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-indigo-400 outline-none bg-indigo-50"/>
          <p class="text-xs text-gray-500 mt-1">Ignorar compras que tardaron más de esto (filtro errores).</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Lead Time Defecto (Días)</label>
          <input v-model.number="configuracion.lead_time_defecto" type="number" min="1" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-indigo-400 outline-none bg-indigo-50"/>
          <p class="text-xs text-gray-500 mt-1">Tiempo de espera para productos nuevos sin historial.</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Margen Vencimiento (Sem.)</label>
          <input v-model.number="configuracion.buffer_venta_semanas" type="number" min="0" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-indigo-400 outline-none bg-indigo-50"/>
          <p class="text-xs text-gray-500 mt-1">Semanas libres antes de que caduque el producto.</p>
        </div>
      </div>

      <div class="flex justify-end">
        <button 
          @click="guardarConfiguracion"
          :disabled="guardandoConfig"
          class="bg-indigo-600 text-white px-6 py-2 rounded-md font-semibold hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
        >
          {{ guardandoConfig ? 'Guardando...' : 'Guardar Todos los Cambios' }}
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="flex items-center space-x-2 mb-4">
        <svg class="w-6 h-6 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m4 8H4m16 8H4m1-4h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-900">Fechas Especiales</h3>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <input v-model="nuevoEvento.nombre" type="text" placeholder="Nombre del evento" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none" />
        <input v-model="nuevoEvento.fecha" type="date" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none" />
        <input v-model="nuevoEvento.descripcion" type="text" placeholder="Descripción" class="border rounded-lg px-3 py-2 text-sm w-full focus:ring-2 focus:ring-teal-400 outline-none" />
      </div>
      <div class="flex justify-end">
        <button @click="agregarOEditarFecha" class="bg-teal-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-teal-600 transition">
          {{ editId === null ? '+ Agregar Fecha' : 'Guardar Cambios' }}
        </button>
      </div>

      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="evento in fechasEspeciales" :key="evento.id" class="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
          <div class="flex items-center mb-1">
            <span class="text-2xl mr-2">{{ obtenerIconoParaEvento(evento.nombre) }}</span>
            <h4 class="font-bold text-lg text-gray-800">{{ evento.nombre }}</h4>
          </div>
          <p class="text-sm text-gray-600"><strong>Fecha:</strong> {{ evento.fecha }}</p>
          <p class="text-sm text-gray-600">{{ evento.descripcion || 'Sin descripción' }}</p>
          <div class="flex gap-4 mt-3">
            <button @click="editarEvento(evento)" class="font-medium text-teal-600 hover:text-teal-700">Editar</button>
            <button @click="eliminarEvento(evento)" class="font-medium text-rose-600 hover:text-rose-700">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axiosInstance from '@/api/axios.js'
import Swal from 'sweetalert2'

// --- ESTADO ---
const fechasEspeciales = ref([])
const nuevoEvento = ref({ nombre: '', fecha: '', descripcion: '' })
const editId = ref(null)

const configuracion = ref({
  semanas_seguridad: 2,
  semanas_objetivo: 4,
  dias_analisis_demanda: 90,
  max_lead_time_razonable: 60,
  lead_time_defecto: 7,
  buffer_venta_semanas: 2,
  umbral_demanda_minima: 0.5,
  umbral_sobrestock_semanas: 12
})
const guardandoConfig = ref(false)

// --- LÓGICA CONFIGURACIÓN ---

const cargarConfiguracion = async () => {
  try {
    const response = await axiosInstance.get('/empresa/configuracion/');
    configuracion.value = {
      semanas_seguridad: response.data.semanas_seguridad,
      semanas_objetivo: response.data.semanas_objetivo,
      dias_analisis_demanda: response.data.dias_analisis_demanda,
      max_lead_time_razonable: response.data.max_lead_time_razonable || 60,
      lead_time_defecto: response.data.lead_time_defecto || 7,
      buffer_venta_semanas: response.data.buffer_venta_semanas || 2,
      umbral_demanda_minima: response.data.umbral_demanda_minima !== undefined ? response.data.umbral_demanda_minima : 0.5,
      umbral_sobrestock_semanas: response.data.umbral_sobrestock_semanas || 12
    };
  } catch (error) {
    console.error('Error config:', error);
    Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo cargar la configuración.' });
  }
};

const guardarConfiguracion = async () => {
  if (configuracion.value.semanas_seguridad < 1 || configuracion.value.semanas_seguridad > 12) {
    return Swal.fire({ icon: 'warning', title: 'Inválido', text: 'Semanas seguridad entre 1 y 12.' });
  }
  if (configuracion.value.umbral_sobrestock_semanas < 4) {
    return Swal.fire({ icon: 'warning', title: 'Inválido', text: 'Umbral sobrestock debe ser al menos 4 semanas.' });
  }

  guardandoConfig.value = true;

  try {
    await axiosInstance.patch('/empresa/configuracion/', configuracion.value);
    Swal.fire({ 
      icon: 'success', 
      title: '¡Configuración guardada!', 
      toast: true, position: 'top-end', showConfirmButton: false, timer: 3000 
    });
  } catch (error) {
    Swal.fire({ icon: 'error', title: 'Error al guardar', text: error.response?.data?.detail || 'Ocurrió un error.' });
  } finally {
    guardandoConfig.value = false;
  }
};

// --- LÓGICA FECHAS ---

const cargarFechas = async () => {
  try {
    const response = await axiosInstance.get('/dias-importantes/');
    fechasEspeciales.value = response.data.map(e => ({
      id: e.id, nombre: e.nombre_evento, fecha: e.fecha, descripcion: e.descripcion
    }));
  } catch (error) {
    Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudieron cargar las fechas.' });
  }
};

onMounted(() => {
  cargarFechas();
  cargarConfiguracion();
});

const agregarOEditarFecha = async () => {
  if (!nuevoEvento.value.nombre || !nuevoEvento.value.fecha) {
    return Swal.fire({ icon: 'warning', title: 'Faltan datos', text: 'Nombre y fecha requeridos.' });
  }
  const payload = {
      nombre_evento: nuevoEvento.value.nombre,
      fecha: nuevoEvento.value.fecha,
      descripcion: nuevoEvento.value.descripcion,
  };
  try {
    if (editId.value !== null) {  
      await axiosInstance.patch(`/dias-importantes/${editId.value}/`, payload);
      Swal.fire({ icon: 'success', title: 'Actualizado', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    } else {  
      await axiosInstance.post('/dias-importantes/', payload);
      Swal.fire({ icon: 'success', title: 'Agregado', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    }
    nuevoEvento.value = { nombre: '', fecha: '', descripcion: '' };
    editId.value = null;
    await cargarFechas();
  } catch (error) { 
    Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo guardar el evento.' });
  }
};

const editarEvento = (evento) => {  
  nuevoEvento.value = { ...evento };
  editId.value = evento.id;
};

const eliminarEvento = (evento) => {
  Swal.fire({
    title: `¿Eliminar "${evento.nombre}"?`,
    icon: 'warning', showCancelButton: true,
    confirmButtonColor: '#e11d48', cancelButtonColor: '#6b7280',
    confirmButtonText: 'Eliminar'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await axiosInstance.delete(`/dias-importantes/${evento.id}/`);
        Swal.fire({ title: 'Eliminado', icon: 'success', timer: 1500, showConfirmButton: false });
        await cargarFechas();
      } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo eliminar.' });
      }
    }
  });
};

const obtenerIconoParaEvento = (nombre) => {
  const n = nombre.toLowerCase();
  if (n.includes('halloween')) return '🎃';
  if (n.includes('navidad')) return '🎄';
  if (n.includes('fiestas patrias')) return '🇨🇱';
  return '📅';
};
</script>

<style scoped> 
input[type="date"]:not(:focus):invalid { color: #9ca3af; }
</style>