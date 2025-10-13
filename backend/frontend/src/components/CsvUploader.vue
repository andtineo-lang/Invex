<template>
  <div class="import-component">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Procesando...</p>
    </div>

    <Transition name="fade" mode="out-in">
      
      <div v-if="step === 'initial'" key="initial" class="step-container">
        <div class="drop-zone" @click="openFilePicker" @dragover.prevent @drop.prevent="handleDrop" @dragenter.prevent @dragleave.prevent>
          <input type="file" @change="handleFileChange" accept=".csv" ref="fileInput" class="hidden">
          <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          <p class="font-semibold text-gray-700">Haz clic para seleccionar un archivo</p>
          <p class="text-sm text-gray-500">o arrástralo aquí (CSV)</p>
        </div>
      </div>

      <div v-else-if="step === 'mapping'" key="mapping" class="step-container">
        <h5 class="step-title">Necesitamos tu ayuda</h5>
        <p class="step-description">No pudimos reconocer las columnas requeridas. Por favor, asocia las columnas.</p>
        <div class="mapping-fields">
          <div class="field-map">
            <label for="map-nombre">Nombre del Producto <strong>(Requerido)</strong></label>
            <select id="map-nombre" v-model="columnMap.nombre">
              <option disabled value="">Selecciona una columna...</option>
              <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
            </select>
          </div>
          <div class="field-map">
            <label for="map-stock">Stock Actual <strong>(Requerido)</strong></label>
            <select id="map-stock" v-model="columnMap.stock_actual">
              <option disabled value="">Selecciona una columna...</option>
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
          <button @click="goToPreview" class="btn btn-primary">Continuar a Previsualización</button>
          <button @click="resetFlow()" class="btn btn-secondary">Cancelar</button>
        </div>
      </div>

      <div v-else-if="step === 'preview'" key="preview" class="step-container">
        <h5 class="step-title">Previsualiza y Confirma</h5>
        <p class="step-description">Revisa que los datos se hayan interpretado correctamente. Solo se muestran las primeras 10 filas.</p>
        
        <div class="table-responsive">
          <table class="preview-table">
            <thead>
              <tr>
                <th>Nombre del Producto </th>
                <th>Stock Actual </th>
                <th>Categoría </th>
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
        </div>

    </Transition>
    
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
// El script que ya tienes está correcto, no necesita cambios
import { ref, computed } from 'vue';
import Papa from 'papaparse';
import axios from 'axios';
const emit = defineEmits(['upload-success']);
const step = ref('initial');
const selectedFile = ref(null);
const fileInput = ref(null);
const error = ref('');
const loading = ref(false);
const csvHeaders = ref([]);
const originalData = ref([]);
const successMessage = ref('');
const columnMap = ref({ nombre: '', stock_actual: '', categoria: '' });
const aliasMap = {
  nombre: ['producto', 'productos', 'nombre', 'nombre_del_producto', 'item', 'items', 'articulo', 'artículos', 'descripción', 'descripcion', 'código', 'codigo', 'sku', 'product', 'products', 'name', 'description'],
  stock_actual: ['stock', 'stock_actual', 'en_stock', 'cantidad', 'cant.', 'unidades', 'disponible', 'disponibles', 'existencia', 'existencias', 'inventario', 'quantity', 'qty', 'on_hand', 'inventory', 'available'],
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
  if (!originalData.value.length || !columnMap.value.nombre || !columnMap.value.stock_actual) return [];
  return originalData.value.map(row => ({
    nombre: row[columnMap.value.nombre],
    stock_actual: row[columnMap.value.stock_actual],
    categoria: columnMap.value.categoria ? row[columnMap.value.categoria] : null,
  }));
});
const processFile = (file) => {
  if (!file) return;
  selectedFile.value = file;
  resetFlow(false);
  loading.value = true;
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      loading.value = false;
      if (results.errors.length || !results.meta.fields) {
        error.value = 'Error al leer el archivo. Asegúrate de que es un CSV válido con encabezados.';
        resetFlow(); return;
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
const handleFileChange = (event) => processFile(event.target.files[0]);
const handleDrop = (event) => processFile(event.dataTransfer.files[0]);
const openFilePicker = () => fileInput.value.click();
const goToPreview = () => {
  if (!columnMap.value.nombre || !columnMap.value.stock_actual) {
    error.value = "Debes mapear las columnas requeridas."; return;
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
  if (clearFile && fileInput.value) fileInput.value.value = null;
  step.value = 'initial';
  error.value = '';
  successMessage.value = '';
  csvHeaders.value = [];
  originalData.value = [];
  columnMap.value = { nombre: '', stock_actual: '', categoria: '' };
};
</script>

<style scoped>
/* (El resto de tus estilos se mantienen igual) */
.import-component { background-color: #f8fafc; padding: 2.5rem; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); position: relative; overflow: hidden; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(15px); }
.step-container { width: 100%; }
.drop-zone { border: 2px dashed #e2e8f0; border-radius: 10px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.3s ease; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.drop-zone:hover { border-color: #0d9488; background-color: #f0fdfa; }
.upload-icon { width: 48px; height: 48px; color: #0d9488; margin-bottom: 1rem; }
.loading-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(255, 255, 255, 0.8); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 50; }
.spinner { border: 4px solid rgba(13, 148, 136, 0.2); border-left-color: #0d9488; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-message { color: #ef4444; background-color: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1.5rem; text-align: center; }
.step-title { font-size: 1.25rem; font-weight: 600; color: #1a202c; margin-bottom: 0.5rem; }
.step-description { color: #4a5568; margin-bottom: 2rem; }
.mapping-fields { display: grid; gap: 1.5rem; margin-bottom: 2rem; }
.field-map { display: flex; flex-direction: column; }
.field-map label { font-weight: 600; margin-bottom: 0.5rem; color: #2d3748; }
.field-map select { padding: 10px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 1rem; }
.action-buttons { display: flex; gap: 1rem; margin-top: 1.5rem; }
.btn { padding: 12px 30px; border-radius: 8px; font-weight: 700; transition: all 0.2s ease; }
.btn-primary { background-color: #0d9488; color: white; }
.btn-secondary { background-color: #e2e8f0; color: #2d3748; }
.table-responsive { overflow-x: auto; max-height: 300px; border: 1px solid #e2e8f0; border-radius: 8px; }
.preview-table { width: 100%; border-collapse: collapse; }
.preview-table th, .preview-table td { border-bottom: 1px solid #e2e8f0; padding: 12px 15px; text-align: left; }
.preview-table th { background-color: #f8fafc; font-weight: 600; position: sticky; top: 0; }
</style>