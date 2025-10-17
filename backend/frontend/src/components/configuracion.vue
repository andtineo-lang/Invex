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
        Personaliza parámetros del sistema y fechas clave para tu negocio.
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
      <div class="flex justify-end">
        <!-- El texto del botón ahora cambia si estamos editando o agregando -->
        <button @click="agregarOEditarFecha"
          class="bg-teal-500 text-white px-5 py-2 rounded-md font-semibold hover:bg-teal-600 transition">
          {{ editId === null ? '+ Agregar Fecha' : 'Guardar Cambios' }}
        </button>
      </div>

      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- La key del v-for ahora usa el ID de la base de datos -->
        <div v-for="evento in fechasEspeciales" :key="evento.id" class="border rounded-lg p-4 shadow-sm hover:shadow-md transition">
          <div class="flex items-center mb-1">
            <span class="text-2xl mr-2">{{ obtenerIconoParaEvento(evento.nombre) }}</span>
            <h4 class="font-bold text-lg text-gray-800">{{ evento.nombre }}</h4>
          </div>
          <p class="text-sm text-gray-600"><strong>Fecha:</strong> {{ evento.fecha }}</p>
          <p class="text-sm text-gray-600"><strong>Descripción:</strong> {{ evento.descripcion || 'Sin descripción' }}</p>
          <div class="flex gap-4 mt-3">
            <!-- Los botones ahora pasan el objeto completo del evento -->
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

<script setup>
// ✅ 1. Importamos lo necesario: onMounted para cargar datos al inicio y nuestra instancia de axios
import { ref, onMounted } from 'vue'
import axiosInstance from '@/api/axios.js'
import Swal from 'sweetalert2'

// --- ESTADO DEL COMPONENTE ---
const fechasEspeciales = ref([]) // Inicia como un array vacío, se llenará desde la API
const nuevoEvento = ref({ nombre: '', fecha: '', descripcion: '' })
const editId = ref(null) // Usaremos el ID de la BD para saber si estamos editando

// --- LÓGICA DE API ---

// ✅ 2. Nueva función para cargar las fechas desde el backend
const cargarFechas = async () => {
  try {
    const response = await axiosInstance.get('/dias-importantes/');
    // Mapeamos los nombres de los campos del backend a los que usa el frontend
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

// ✅ 3. Usamos onMounted para llamar a cargarFechas() cuando el componente se muestra
onMounted(() => {
  cargarFechas();
});

// ✅ 4. Unificamos la lógica de crear y editar en una sola función
const agregarOEditarFecha = async () => {
  if (!nuevoEvento.value.nombre || !nuevoEvento.value.fecha) {
    Swal.fire({ icon: 'warning', title: '¡Ups!', text: 'El nombre y la fecha son obligatorios.' });
    return;
  }

  // Preparamos el payload con los nombres de campo que el backend espera
  const payload = {
      nombre_evento: nuevoEvento.value.nombre,
      fecha: nuevoEvento.value.fecha,
      descripcion: nuevoEvento.value.descripcion,
  };

  try {
    if (editId.value !== null) {
      // --- LÓGICA DE ACTUALIZACIÓN (PATCH) ---
      await axiosInstance.patch(`/dias-importantes/${editId.value}/`, payload);
      Swal.fire({ icon: 'success', title: '¡Evento actualizado!', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    } else {
      // --- LÓGICA DE CREACIÓN (POST) ---
      await axiosInstance.post('/dias-importantes/', payload);
      Swal.fire({ icon: 'success', title: '¡Evento agregado!', toast: true, position: 'top-end', showConfirmButton: false, timer: 2000 });
    }
    
    // Limpiamos el formulario, reseteamos el ID de edición y recargamos la lista de fechas
    nuevoEvento.value = { nombre: '', fecha: '', descripcion: '' };
    editId.value = null;
    await cargarFechas();

  } catch (error) {
    // Manejo de errores de la API
    const errorMsg = error.response?.data?.detail || 'Ocurrió un problema al guardar el evento.';
    Swal.fire({ icon: 'error', title: 'Error al guardar', text: errorMsg });
  }
};

// ✅ 5. La función de editar ahora guarda el ID del evento
const editarEvento = (evento) => {
  // Cargamos los datos del evento en el formulario y guardamos su ID
  nuevoEvento.value = { ...evento };
  editId.value = evento.id;
};

// ✅ 6. La función de eliminar ahora usa el ID del evento para la petición a la API
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
        await cargarFechas(); // Recargamos la lista para que desaparezca el evento
      } catch (error) {
        Swal.fire({ icon: 'error', title: 'Error al eliminar', text: 'No se pudo eliminar el evento.' });
      }
    }
  });
};

// --- FUNCIONES AUXILIARES (sin cambios) ---
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
/* Estilos para que el input de fecha muestre el placeholder correctamente */
input[type="date"]:not(:focus):invalid {
  color: #9ca3af; /* Color de texto gris para el placeholder */
}
</style>
