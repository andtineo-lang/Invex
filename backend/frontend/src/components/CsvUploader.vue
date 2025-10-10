<template>
  <div class="import-component">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Procesando...</p>
    </div>

    <Transition name="fade" mode="out-in">
      
      <div v-if="step === 'initial'" key="initial" class="step-container">
        <div class="drop-zone" @click="$refs.fileInput.click()">
          <input type="file" @change="handleFileChange" accept=".csv" ref="fileInput" class="hidden">
          <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <p class="font-semibold text-gray-700">Haz clic para seleccionar un archivo</p>
          <p class="text-sm text-gray-500">o arrástralo aquí (CSV, hasta 5MB)</p>
        </div>
      </div>

      <div v-else-if="step === 'mapping'" key="mapping" class="step-container">
        <h5 class="step-title">
          <svg class="w-6 h-6 mr-2 inline-block text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Necesitamos tu ayuda
        </h5>
        <p class="step-description">No pudimos reconocer todas las columnas requeridas. Por favor, ayúdanos a asociarlas.</p>
        
        <div class="mapping-fields">
          <div class="field-map">
            <label for="map-nombre">Nombre del Producto <strong>(Requerido)</strong></label>
            <select id="map-nombre" v-model="columnMap.nombre">
              <option disabled value="">Selecciona la columna de productos...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-stock">Stock Actual <strong>(Requerido)</strong></label>
            <select id="map-stock" v-model="columnMap.stock_actual">
              <option disabled value="">Selecciona la columna de stock...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-categoria">Categoría (Opcional)</label>
            <select id="map-categoria" v-model="columnMap.categoria">
              <option value="">No importar categoría...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="goToPreview" class="btn btn-primary">Continuar</button>
          <button @click="resetFlow" class="btn btn-secondary">Cancelar</button>
        </div>
      </div>

      <div v-else-if="step === 'preview'" key="preview" class="step-container">
        <h5 class="step-title">
          <svg class="w-6 h-6 mr-2 inline-block text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
          Previsualiza y Confirma
        </h5>
        <p class="step-description">Revisa que los datos se hayan interpretado correctamente. Solo se muestran las primeras 10 filas.</p>
        
        <div class="table-responsive">
          <table class="preview-table">
            <thead>
              <tr>
                <th>Nombre del Producto (Mapeado)</th>
                <th>Stock Actual (Mapeado)</th>
                <th>Categoría (Mapeado)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in processedData.slice(0, 10)" :key="index">
                <td>{{ row.nombre }}</td>
                <td>{{ row.stock_actual }}</td>
                <td>{{ row.categoria }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="action-buttons">
          <button @click="submitFile" class="btn btn-primary">Confirmar e Importar</button>
          <button @click="step = 'mapping'" class="btn btn-secondary">Corregir Mapeo</button>
        </div>
      </div>
      
      <div v-else-if="step === 'success'" key="success" class="step-container text-center">
        <svg class="w-16 h-16 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <h5 class="step-title mt-4">¡Importación Exitosa!</h5>
        <p class="step-description">{{ successMessage }}</p>
        <div class="action-buttons justify-center">
          <button @click="resetFlow" class="btn btn-primary">Importar otro archivo</button>
        </div>
      </div>

    </Transition>
    
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Papa from 'papaparse';
import axios from 'axios';

const emit = defineEmits(['upload-success']);

const step = ref('initial');
const selectedFile = ref(null);
const error = ref('');
const loading = ref(false);
const csvHeaders = ref([]);
const originalData = ref([]);
const successMessage = ref('');
const columnMap = ref({
  nombre: '',
  stock_actual: '',
  categoria: '',
});

const aliasMap = {
  nombre: ['producto', 'productos', 'nombre', 'nombre_del_producto', 'nombre del producto', 'item', 'items', 'articulo', 'artículos', 'descripción', 'descripcion', 'código', 'codigo', 'sku', 'product', 'products', 'name', 'description'],
  stock_actual: ['stock', 'stock_actual', 'en_stock', 'en stock', 'cantidad', 'cant.', 'unidades', 'disponible', 'disponibles', 'existencia', 'existencias', 'inventario', 'quantity', 'qty', 'on_hand', 'on hand', 'inventory', 'available'],
  categoria: ['categoría', 'categoria', 'categorías', 'categorias', 'tipo', 'tipos', 'familia', 'grupo', 'línea', 'linea', 'departamento', 'category', 'categories', 'group', 'type', 'department', 'line']
};

const guessColumnMappings = (headers) => {
  const newMap = { nombre: '', stock_actual: '', categoria: '' };
  headers.forEach(header => {
    const normalizedHeader = header.toLowerCase().trim().replace(/ /g, '_').replace(/-/g, '_');
    for (const key in aliasMap) {
      if (aliasMap[key].includes(normalizedHeader) && !newMap[key]) {
        newMap[key] = header;
      }
    }
  });
  columnMap.value = newMap;
};

const processedData = computed(() => {
  if (originalData.value.length === 0 || !columnMap.value.nombre || !columnMap.value.stock_actual) {
    return [];
  }
  return originalData.value.map(row => ({
    nombre: row[columnMap.value.nombre],
    stock_actual: row[columnMap.value.stock_actual],
    categoria: columnMap.value.categoria ? row[columnMap.value.categoria] : null,
  }));
});

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  if (!selectedFile.value) return;
  resetFlow(false);
  loading.value = true;
  Papa.parse(selectedFile.value, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      loading.value = false;
      if (results.errors.length || !results.meta.fields) {
        error.value = 'Error al leer el archivo. Asegúrate de que es un CSV con encabezados.';
        resetFlow();
        return;
      }
      csvHeaders.value = results.meta.fields;
      originalData.value = results.data;
      guessColumnMappings(csvHeaders.value);
      if (columnMap.value.nombre && columnMap.value.stock_actual) {
        step.value = 'preview';
      } else {
        step.value = 'mapping';
      }
    }
  });
};

const goToPreview = () => {
  if (!columnMap.value.nombre || !columnMap.value.stock_actual) {
    error.value = "Debes mapear las columnas requeridas.";
    return;
  }
  error.value = '';
  step.value = 'preview';
};

const submitFile = async () => {
  loading.value = true;
  error.value = '';
  const empresaId = 1;
  try {
    const response = await axios.post(`/api/empresas/${empresaId}/importar-inventario/`, processedData.value);
    emit('upload-success', response.data.mensaje);
    successMessage.value = response.data.mensaje;
    step.value = 'success';
  } catch (err) {
    error.value = err.response?.data?.detalles?.join(', ') || err.response?.data?.error || 'Ocurrió un error inesperado.';
  } finally {
    loading.value = false;
  }
};

const resetFlow = (clearFile = true) => {
  if (clearFile) selectedFile.value = null;
  step.value = 'initial';
  error.value = '';
  successMessage.value = '';
  csvHeaders.value = [];
  originalData.value = [];
  columnMap.value = { nombre: '', stock_actual: '', categoria: '' };
};
</script>

<style scoped>
.import-component {
  background-color: #f8fafc;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(15px);
}

.loading-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 50;
  color: #0d9488;
  font-weight: 600;
}
.spinner {
  border: 4px solid rgba(13, 148, 136, 0.2);
  border-left-color: #0d9488;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

.drop-zone {
  border: 2px dashed #e2e8f0;
  border-radius: 10px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s ease, background-color 0.3s ease;
}
.drop-zone:hover {
  border-color: #0d9488;
  background-color: #f0fdfa;
}
.upload-icon {
  width: 48px;
  height: 48px;
  color: #0d9488;
  margin: 0 auto 1rem;
}

.action-buttons {
  display: flex;
  gap: 1.25rem;
  margin-top: 2.5rem;
  justify-content: flex-start;
}
.btn {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.btn-primary { background-color: #0d9488; color: white; }
.btn-primary:hover { background-color: #0c7b72; }
.btn-secondary { background-color: #e2e8f0; color: #2d3748; }
.btn-secondary:hover { background-color: #cbd5e0; }

.mapping-fields {
  display: grid;
  gap: 1.5rem;
  margin-top: 2rem;
}
.field-map label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3748;
}
.field-map select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #fff;
}

.table-responsive {
  overflow-x: auto;
  max-height: 400px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}
.preview-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}
.preview-table th, .preview-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 1.25rem;
  text-align: left;
  white-space: nowrap;
}
.preview-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #4a5568;
  position: sticky;
  top: 0;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.preview-table tr:last-child td {
  border-bottom: none;
}
.error-message {
  color: #ef4444;
  background-color: rgba(239, 68, 68, 0.1);
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  font-weight: 500;
  text-align: center;
}
</style>