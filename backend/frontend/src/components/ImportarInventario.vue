<template>
  <div class="import-container">
    
      <h2>Importar Inventario</h2>
      <p>Puedes subir tu inventario desde un archivo CSV o ingresarlo manualmente.</p>
   

    <div class="mode-selector">
      <button 
        @click="modo = 'csv'" 
        :class="['mode-button', { 'active': modo === 'csv' }]"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        Subir Archivo CSV
      </button>
      <button 
        @click="modo = 'manual'" 
        :class="['mode-button', { 'active': modo === 'manual' }]"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
        Ingreso Manual
      </button>
    </div>

    <div class="content-wrapper">
      <CsvUploader v-if="modo === 'csv'" @upload-success="handleSuccess" />
      <ManualEntry v-if="modo === 'manual'" @upload-success="handleSuccess" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CsvUploader from '@/components/CsvUploader.vue';
import ManualEntry from '@/components/ManualEntry.vue';

const modo = ref('csv');

const handleSuccess = (message) => {
  console.log('Éxito:', message);
  alert(message || '¡El inventario se ha actualizado correctamente!');
};
</script>

<style scoped>
.import-container {
  max-width: 900px;
  margin: 0 auto;
}
.header {
  text-align: center;
  margin-bottom: 2rem;
}
h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
}
p {
  color: #4a5568;
  font-size: 1.1rem;
}
.mode-selector {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}
.mode-button {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  background-color: #f1f5f9;
  color: #475569;
  font-weight: 600;
  transition: all 0.3s ease;
}
.mode-button:hover:not(.active) {
  background-color: #e2e8f0;
  color: #1e293b;
}
.mode-button.active {
  background-color: #f0fdfa;
  color: #0d9488;
  border-color: #0d9488;
  box-shadow: 0 4px 10px rgba(13, 148, 136, 0.2);
  transform: translateY(-2px);
}
</style>