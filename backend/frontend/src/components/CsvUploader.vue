<template>
  <div>
    <h4>Subir mediante archivo CSV</h4>
    <p class="instrucciones">Sube tu archivo de inventario y te ayudaremos a mapear las columnas para que coincidan con nuestro sistema.</p>

    <div v-if="step === 'initial'" class="file-input-wrapper">
      <input type="file" @change="handleFileChange" accept=".csv" ref="fileInput" class="hidden">
      <button @click="$refs.fileInput.click()" class="btn-file-select">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        Seleccionar archivo CSV
      </button>
    </div>

    <div v-if="step === 'mapping'" class="mapping-container">
      <h5 class="step-title">Asocia tus columnas</h5>
      <p class="step-description">Indícanos qué columna de tu archivo CSV corresponde a cada campo requerido.</p>

      <div class="mapping-fields">
        <div class="field-map">
          <label for="map-nombre">Nombre del Producto <strong>(Requerido)</strong></label>
          <select id="map-nombre" v-model="columnMap.nombre">
            <option disabled value="">Selecciona una columna de tu archivo...</option>
            <option v-for="header in csvHeaders" :key="header" :value="header">
              {{ header }}
            </option>
          </select>
        </div>

        <div class="field-map">
          <label for="map-stock">Stock Actual <strong>(Requerido)</strong></label>
          <select id="map-stock" v-model="columnMap.stock_actual">
            <option disabled value="">Selecciona una columna de tu archivo...</option>
            <option v-for="header in csvHeaders" :key="header" :value="header">
              {{ header }}
            </option>
          </select>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="goToPreview" class="btn-confirm-import">Continuar a Previsualización</button>
        <button @click="resetFlow" class="btn-secondary">Cancelar</button>
      </div>
    </div>

    <div v-if="step === 'preview'" class="preview-container">
      <h5 class="step-title">Previsualiza y Confirma</h5>
      <p class="step-description">Revisa que los datos se hayan interpretado correctamente. Solo se muestran las primeras 10 filas.</p>
      
      <div class="table-responsive">
        <table class="preview-table">
          <thead>
            <tr>
              <th>Nombre del Producto (Mapeado)</th>
              <th>Stock Actual (Mapeado)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in processedData.slice(0, 10)" :key="index">
              <td>{{ row.nombre }}</td>
              <td>{{ row.stock_actual }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="action-buttons">
        <button @click="submitFile" :disabled="loading" class="btn-confirm-import">
          {{ loading ? 'Importando...' : `Confirmar e Importar ${processedData.length} productos` }}
        </button>
        <button @click="step = 'mapping'" class="btn-secondary">Volver a Mapear</button>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="loading" class="loading-message">Procesando, por favor espera...</div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Papa from 'papaparse';
import axios from 'axios';

const emit = defineEmits(['upload-success']);

// ESTADO DEL COMPONENTE
const selectedFile = ref(null);
const error = ref('');
const loading = ref(false);

// Estado para el flujo de mapeo
const step = ref('initial'); // 'initial' -> 'mapping' -> 'preview'
const csvHeaders = ref([]);
const originalData = ref([]);
const columnMap = ref({
  nombre: '',
  stock_actual: '',
});

// Transforma los datos originales según el mapeo del usuario
const processedData = computed(() => {
  if (originalData.value.length === 0 || !columnMap.value.nombre || !columnMap.value.stock_actual) {
    return [];
  }
  return originalData.value.map(row => ({
    nombre: row[columnMap.value.nombre],
    stock_actual: row[columnMap.value.stock_actual],
  }));
});

// MÉTODOS
const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  if (!selectedFile.value) return;

  resetFlow(false); // Reinicia sin borrar el archivo seleccionado
  loading.value = true;

  Papa.parse(selectedFile.value, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      loading.value = false;
      if (results.errors.length) {
        error.value = 'Error al leer el archivo. Asegúrate de que es un CSV con encabezados.';
        step.value = 'initial';
        return;
      }
      csvHeaders.value = results.meta.fields;
      originalData.value = results.data;
      step.value = 'mapping';
    }
  });
};

const goToPreview = () => {
  if (!columnMap.value.nombre || !columnMap.value.stock_actual) {
    error.value = "Debes mapear las columnas 'Nombre del Producto' y 'Stock Actual'.";
    return;
  }
  error.value = '';
  step.value = 'preview';
};

const submitFile = async () => {
  if (processedData.value.length === 0) {
    error.value = "No hay datos para importar.";
    return;
  }
  loading.value = true;
  error.value = '';
  
  const empresaId = 1; // Reemplazar con el ID real de la empresa

  try {
    const response = await axios.post(`/api/empresas/${empresaId}/importar-inventario/`, processedData.value);
    emit('upload-success', response.data.mensaje);
    resetFlow(true); // Reinicia todo el flujo
  } catch (err) {
    error.value = err.response?.data?.detalles?.join(', ') || err.response?.data?.error || 'Ocurrió un error inesperado al importar.';
  } finally {
    loading.value = false;
  }
};

const resetFlow = (clearFile = true) => {
  if (clearFile) {
    selectedFile.value = null;
  }
  step.value = 'initial';
  error.value = '';
  csvHeaders.value = [];
  originalData.value = [];
  columnMap.value = { nombre: '', stock_actual: '' };
};
</script>

<style scoped>
/* Estilos generales */
h4 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 0.8rem;
}
.instrucciones {
  font-size: 0.95em;
  color: #666;
  margin-bottom: 2rem;
}
.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.5rem;
}
.step-description {
  color: #4a5568;
  margin-bottom: 2rem;
}

/* Contenedores de pasos */
.file-input-wrapper {
  text-align: center;
}
.mapping-container, .preview-container {
  text-align: left;
  border: 1px solid #e2e8f0;
  padding: 2rem;
  border-radius: 8px;
  background-color: #ffffff;
}

/* Estilos de Mapeo */
.mapping-fields {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.field-map {
  display: flex;
  flex-direction: column;
}
.field-map label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3748;
}
.field-map label strong {
  color: #0d9488;
}
.field-map select {
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #fff;
}

/* Botones */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: flex-start;
}
.btn-file-select {
  display: inline-flex;
  align-items: center;
  padding: 12px 25px;
  background-color: #0d9488;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(13, 148, 136, 0.2);
}
.btn-file-select:hover {
  background-color: #0c7b72;
  transform: translateY(-1px);
}
.btn-confirm-import {
  display: inline-flex;
  align-items: center;
  padding: 12px 30px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.btn-confirm-import:hover:not(:disabled) {
  background-color: #0e9f6e;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4);
}
.btn-confirm-import:disabled, .btn-secondary:disabled {
  background-color: #a7f3d0;
  cursor: not-allowed;
  box-shadow: none;
}
.btn-secondary {
  padding: 12px 30px;
  background-color: #e2e8f0;
  color: #2d3748;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.05rem;
  transition: all 0.3s ease;
}
.btn-secondary:hover:not(:disabled) {
  background-color: #cbd5e0;
}

/* Tabla de Previsualización */
.table-responsive {
  overflow-x: auto;
  max-height: 300px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.preview-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}
.preview-table th, .preview-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 15px;
  text-align: left;
}
.preview-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #4a5568;
  position: sticky;
  top: 0;
}

/* Mensajes */
.error-message {
  color: #d9534f;
  margin-top: 1.5rem;
  font-weight: 500;
  text-align: center;
}
.loading-message {
  color: #5bc0de;
  margin-top: 1.5rem;
  font-weight: 500;
  text-align: center;
}
</style>