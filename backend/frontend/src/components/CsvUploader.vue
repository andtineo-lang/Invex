<template>
  <div>
    <h4>Subir mediante archivo CSV</h4>
    <p class="instrucciones">
      El archivo debe contener al menos las columnas: <strong>nombre</strong> y <strong>stock_actual</strong>.
      <a href="/plantilla_inventario.csv" download class="text-teal-600 hover:underline">Descarga la plantilla de ejemplo aquí.</a>
    </p>

    <div class="file-input-wrapper">
      <input type="file" @change="handleFileChange" accept=".csv" ref="fileInput" class="hidden">
      <button @click="$refs.fileInput.click()" class="btn-file-select">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        {{ selectedFile ? 'Cambiar archivo' : 'Seleccionar archivo CSV' }}
      </button>
      <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="loading" class="loading-message">Procesando archivo, por favor espera...</div>

    <div v-if="parsedData.length > 0" class="preview-container">
      <h5>Previsualización (primeras 10 filas)</h5>
      <div class="table-responsive">
        <table class="preview-table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in parsedData.slice(0, 10)" :key="index">
              <td v-for="header in headers" :key="header">{{ row[header] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="submitFile" :disabled="loading" class="btn-confirm-import">
        {{ loading ? 'Importando...' : `Confirmar e Importar ${parsedData.length} productos` }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Papa from 'papaparse';
import axios from 'axios';

// 1. Define el evento que el componente puede emitir
const emit = defineEmits(['upload-success']);

const selectedFile = ref(null);
const parsedData = ref([]);
const headers = ref([]);
const error = ref('');
const loading = ref(false);

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  if (!selectedFile.value) return;

  error.value = '';
  parsedData.value = [];
  headers.value = [];
  loading.value = true;

  Papa.parse(selectedFile.value, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      loading.value = false;
      if (results.errors.length) {
        error.value = 'Error al leer el archivo. Asegúrate de que es un CSV válido.';
        return;
      }
      if (!results.data.length || !results.meta.fields.includes('nombre')) {
         error.value = 'El archivo CSV está vacío o le falta la columna obligatoria "nombre".';
         return;
      }
      headers.value = results.meta.fields;
      parsedData.value = results.data;
    }
  });
};

const submitFile = async () => {
  if (!selectedFile.value) return;

  loading.value = true;
  error.value = '';
  
  const formData = new FormData();
  formData.append('file', selectedFile.value);

  const empresaId = 1; // Reemplazar con el ID real

  try {
    const response = await axios.post(`/api/empresas/${empresaId}/importar-inventario/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    // 2. Usa el emit para enviar el mensaje de éxito al componente padre
    emit('upload-success', response.data.mensaje);
    
  } catch (err) {
    error.value = err.response?.data?.detalles?.join(', ') || err.response?.data?.error || 'Ocurrió un error inesperado al importar.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Estilos para ManualEntry */
h4 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.table-responsive {
  overflow-x: auto;
  max-height: 400px; /* Limitar altura de la tabla manual */
  margin-bottom: 1.5rem;
}
.manual-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
  min-width: 600px;
}
.manual-table th, .manual-table td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: left;
}
.manual-table th {
  background-color: #f8f8f8;
  font-weight: 600;
  color: #444;
  position: sticky; /* Encabezado fijo */
  top: 0;
  z-index: 1;
}
.manual-table input {
  width: calc(100% - 16px); /* Ajusta para padding */
  padding: 8px;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  font-size: 0.9em;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.manual-table input:focus {
  border-color: #0d9488;
  box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.2);
  outline: none;
}

.actions-column {
  width: 60px; /* Un poco más de espacio para el botón de eliminar */
  text-align: center;
}

/* Estilo para el botón de eliminar fila */
.btn-remove-row {
  background-color: #ef4444; /* Rojo vibrante */
  color: white;
  border: none;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 50%; /* Completamente redondo */
  font-size: 0.9rem;
  font-weight: bold;
  transition: background-color 0.2s ease;
}
.btn-remove-row:hover {
  background-color: #dc2626; /* Rojo más oscuro al pasar el ratón */
}

/* Estilo para el botón "Añadir Fila" */
.btn-add-row {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #22c55e; /* Verde brillante */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 8px rgba(34, 197, 94, 0.2);
}

.btn-add-row:hover {
  background-color: #16a34a; /* Verde más oscuro */
  transform: translateY(-1px);
}

/* Estilo para el botón "Guardar Inventario" */
.btn-save-manual {
  display: inline-flex;
  align-items: center;
  padding: 12px 30px;
  background-color: #0d9488; /* Tu color teal principal */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
  margin-top: 1.5rem;
}

.btn-save-manual:hover:not(:disabled) {
  background-color: #0c7b72;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(13, 148, 136, 0.4);
}

.btn-save-manual:disabled {
  background-color: #b2dfdb; /* Fondo más claro y opaco para deshabilitado */
  cursor: not-allowed;
  box-shadow: none;
}

.error-message {
  color: #d9534f;
  margin-bottom: 1rem;
  font-weight: 500;
}
</style>