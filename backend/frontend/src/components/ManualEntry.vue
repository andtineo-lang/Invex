<template>
  <div>
    <h4>Ingreso manual de inventario</h4>
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

    <button @click="addRow" class="btn-add-row">+ Añadir Fila</button>
    
    <hr class="my-6">
    
    <div v-if="error" class="error-message">{{ error }}</div>

    <button 
      @click="submitManualData" 
      :disabled="loading || productos.length === 0" 
      class="btn-save-manual"
    >
      {{ loading ? 'Guardando...' : 'Guardar Inventario' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// 1. Define el evento que el componente puede emitir al componente padre
const emit = defineEmits(['upload-success']);

// Variables reactivas
const productos = ref([
  { nombre: '', stock_actual: 0, unidad_medida: 'unidades' }
]);
const loading = ref(false);
const error = ref('');

// Función para añadir una nueva fila/producto
const addRow = () => {
  productos.value.push({ nombre: '', stock_actual: 0, unidad_medida: 'unidades' });
};

// Función para eliminar una fila/producto por su índice
const removeRow = (index) => {
  productos.value.splice(index, 1);
};

// Función asíncrona para enviar los datos a la API
const submitManualData = async () => {
  loading.value = true;
  error.value = '';

  // Filtra los productos para enviar solo aquellos que tienen un nombre
  const dataToSend = productos.value.filter(p => p.nombre && p.nombre.trim() !== '');
  
  // Validación: Debe haber al menos un producto con nombre
  if (dataToSend.length === 0) {
      error.value = "Añade al menos un producto con nombre para guardar.";
      loading.value = false;
      return;
  }

  // **IMPORTANTE:** Reemplaza '1' con el ID real de la empresa
  const empresaId = 1; 

  try {
    // Petición POST a la API
    const response = await axios.post(`/api/empresas/${empresaId}/importar-inventario/`, dataToSend);

    // 2. Emite el evento de éxito al componente padre
    emit('upload-success', response.data.mensaje);
    
    // Opcional: Limpiar el formulario después de un guardado exitoso
    productos.value = [{ nombre: '', stock_actual: 0, unidad_medida: 'unidades' }];
    

  } catch (err) {
    // Manejo de errores de la API
    error.value = err.response?.data?.detalles?.join(', ') || err.response?.data?.error || 'Ocurrió un error inesperado al guardar.';
  } finally {
    // Se ejecuta siempre, independientemente del éxito o fracaso
    loading.value = false;
  }
};
</script>


<style scoped>
.table-responsive {
  overflow-x: auto;
  margin-bottom: 1rem;
}
.manual-table {
  width: 100%;
  border-collapse: collapse;
}
.manual-table th, .manual-table td {
  padding: 8px;
  text-align: left;
}
.manual-table input {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.actions-column {
  width: 50px;
  text-align: center;
}
.btn-danger {
  background-color: #d9534f;
  color: white;
  border: none;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: 50%;
}
.btn-secondary {
  margin-bottom: 1rem;
}
hr {
  margin: 1.5rem 0;
}
.error-message {
  color: #d9534f;
  margin-bottom: 1rem;
}
</style>