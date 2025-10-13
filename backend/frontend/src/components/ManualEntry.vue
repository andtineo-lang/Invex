<template>
  <div class="import-component">
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Guardando...</p>
    </div>

    <div class="table-responsive">
      <table class="manual-table">
        <thead>
          <tr>
            <th>Nombre del Producto *</th>
            <th>Stock Actual</th>
            <th>Unidad de Medida</th>
            <th class="actions-column"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(producto, index) in productos" :key="index">
            <td>
              <input type="text" v-model="producto.nombre" placeholder="Ej: Tornillos 5mm">
            </td>
            <td>
              <input type="number" v-model.number="producto.stock_actual" placeholder="0" min="0">
            </td>
            <td>
              <input type="text" v-model="producto.unidad_medida" placeholder="unidades">
            </td>
            <td class="actions-column">
              <button @click="removeRow(index)" class="btn-remove-row" title="Eliminar fila">&times;</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="action-buttons">
      <button @click="addRow" class="btn btn-secondary">+ Añadir Fila</button>
    </div>
    
    <hr class="separator">
    
    <div v-if="error" class="error-message">{{ error }}</div>

    <div class="action-buttons justify-start">
      <button @click="submitManualData" :disabled="loading || productos.length === 0" class="btn btn-primary">
        {{ loading ? 'Guardando...' : 'Guardar Inventario' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['upload-success']);

const productos = ref([
  { nombre: '', stock_actual: 0, unidad_medida: 'unidades' }
]);
const loading = ref(false);
const error = ref('');

const addRow = () => {
  productos.value.push({ nombre: '', stock_actual: 0, unidad_medida: 'unidades' });
};

const removeRow = (index) => {
  productos.value.splice(index, 1);
};

const submitManualData = async () => {
  loading.value = true;
  error.value = '';

  const dataToSend = productos.value.filter(p => p.nombre && p.nombre.trim() !== '');
  
  if (dataToSend.length === 0) {
      error.value = "Añade al menos un producto con nombre para guardar.";
      loading.value = false;
      return;
  }

  const empresaId = 1;

  try {
    const response = await axios.post(`/api/empresas/${empresaId}/importar-inventario/`, dataToSend);
    emit('upload-success', response.data.mensaje);
    productos.value = [{ nombre: '', stock_actual: 0, unidad_medida: 'unidades' }];
  } catch (err) {
    error.value = err.response?.data?.detalles?.join(', ') || err.response?.data?.error || 'Ocurrió un error inesperado al guardar.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* (Tus estilos se mantienen igual) */
.import-component { background-color: #f8fafc; padding: 2.5rem; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); position: relative; }
.loading-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(255, 255, 255, 0.8); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 50; }
.spinner { border: 4px solid rgba(13, 148, 136, 0.2); border-left-color: #0d9488; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.table-responsive { overflow-x: auto; border: 1px solid #e2e8f0; border-radius: 8px; }
.manual-table { width: 100%; border-collapse: collapse; }
.manual-table th, .manual-table td { border-bottom: 1px solid #e2e8f0; padding: 0.75rem 1rem; text-align: left; }
.manual-table th { background-color: #f8fafc; font-weight: 600; color: #4a5568; font-size: 0.8rem; text-transform: uppercase; }
.manual-table input { width: 100%; padding: 8px; border: 1px solid #dcdcdc; border-radius: 6px; }
.actions-column { width: 60px; text-align: center; }
.btn-remove-row { background-color: #ef4444; color: white; border: none; cursor: pointer; width: 28px; height: 28px; border-radius: 50%; font-size: 1rem; font-weight: bold; transition: background-color 0.2s; }
.btn-remove-row:hover { background-color: #dc2626; }
.separator { border-top: 1px solid #e2e8f0; margin: 2rem 0; }
.action-buttons { display: flex; gap: 1rem; margin-top: 1.5rem; }
.btn { padding: 12px 30px; border-radius: 8px; cursor: pointer; font-weight: 700; transition: all 0.2s ease; }
.btn-primary { background-color: #0d9488; color: white; }
.btn-secondary { background-color: #e2e8f0; color: #2d3748; }
.error-message { color: #ef4444; background-color: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1.5rem; text-align: center; }
</style>