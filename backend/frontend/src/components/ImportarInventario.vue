<template>
  <div class="import-container">
    <h2>Importar Inventario</h2>
    <p>Puedes subir tu inventario desde un archivo CSV o ingresarlo manualmente.</p>

    <div class="mode-selector">
      <button @click="modo = 'csv'" :class="{ active: modo === 'csv' }">Subir Archivo CSV</button>
      <button @click="modo = 'manual'" :class="{ active: modo === 'manual' }">Ingreso Manual</button>
    </div>

    <div v-if="modo === 'csv'" class="import-content">
      <CsvUploader @upload-success="handleSuccess" />
    </div>

    <div v-if="modo === 'manual'" class="import-content">
      <ManualEntry @upload-success="handleSuccess" />
    </div>
  </div>
</template>

<script>
import CsvUploader from '@/components/CsvUploader.vue';
import ManualEntry from '@/components/ManualEntry.vue';

export default {
  name: 'ImportarInventario',
  components: {
    CsvUploader,
    ManualEntry
  },
  data() {
    return {
      modo: 'csv', // Modo inicial
    };
  },
  methods: {
    handleSuccess(message) {
      // Mostrar una notificación de éxito al usuario
      console.log('Éxito:', message);
      // Aquí podrías usar una librería de notificaciones como vue-toastification
      this.$toast.success(message);
      // O redirigir al inventario
      this.$router.push('/inventario');
    }
  }
};
</script>

<style scoped>
/* Contenedor principal de la página de importación */
.import-container {
  max-width: 900px; /* Ajusta esto según el ancho deseado */
  margin: 0 auto; /* Centra el contenido */
  padding: 20px;
  background-color: #ffffff; /* Fondo blanco para el contenido de la página */
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #212121; /* Color de texto oscuro */
  margin-bottom: 0.5rem;
}

p {
  color: #555;
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

/* Estilos para el selector de modo (botones "Subir CSV" / "Ingreso Manual") */
.mode-selector {
  display: flex; /* Para que los botones estén en línea */
  gap: 10px; /* Espacio entre los botones */
  margin-bottom: 2rem; /* Espacio debajo del selector */
}

.mode-button {
  padding: 12px 25px;
  border: 2px solid #0d9488; /* Borde verde teal */
  border-radius: 8px; /* Bordes ligeramente redondeados */
  cursor: pointer;
  background-color: #e0f2f1; /* Fondo claro para los inactivos */
  color: #0d9488; /* Texto verde teal para inactivos */
  font-weight: 600;
  transition: all 0.3s ease; /* Transición suave */
  font-size: 1rem;
  white-space: nowrap; /* Evita que el texto se rompa */
}

.mode-button:hover:not(.active) {
  background-color: #b2dfdb; /* Fondo un poco más oscuro al pasar el ratón */
}

.mode-button.active {
  background-color: #0d9488; /* Fondo verde teal para el activo */
  color: white; /* Texto blanco para el activo */
  box-shadow: 0 4px 8px rgba(13, 148, 136, 0.3); /* Sombra para el activo */
  transform: translateY(-2px); /* Pequeño efecto de elevación */
}

/* Estilos para el contenido de importación (el cuadro dashed) */
.import-content {
  margin-top: 20px;
  padding: 30px;
  border: 2px dashed #b2dfdb; /* Borde dashed más integrado */
  border-radius: 10px;
  background-color: #f5fdfd; /* Fondo muy claro */
  text-align: center; /* Centrar el contenido dentro de la caja */
}
</style>