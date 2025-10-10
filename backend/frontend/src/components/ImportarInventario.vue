<template>
  <div class="p-4 sm:p-6 md:p-8 bg-white rounded-lg shadow-md">
    <header class="mb-6 border-b pb-4">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-800">
        Importar Inventario
      </h1>
      <p class="mt-1 text-sm text-gray-500">
        Puedes agregar productos a tu inventario subiendo un archivo CSV o ingresándolos manualmente.
      </p>
    </header>

    <div class="space-y-8">
      <section>
        <h2 class="text-xl font-semibold text-gray-700 mb-3">
          Opción 1: Subir Archivo CSV
        </h2>
        <CsvUploader @upload-success="handleSuccess" />
      </section>

      <div class="relative">
        <div class="absolute inset-0 flex items-center" aria-hidden="true">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center">
          <span class="bg-white px-2 text-sm text-gray-500">O</span>
        </div>
      </div>

      <section>
        <h2 class="text-xl font-semibold text-gray-700 mb-3">
          Opción 2: Entrada Manual
        </h2>
        <ManualEntry @entry-success="handleSuccess" />
      </section>
    </div>
  </div>
</template>

<script setup>
// Importa los componentes necesarios para la página
import CsvUploader from './CsvUploader.vue';
import ManualEntry from './ManualEntry.vue';

// NOTA: Se ha eliminado 'useRouter' del import y la constante 'router',
// ya que no se estaban utilizando en este componente.

// Función para manejar una respuesta exitosa de cualquiera de los componentes hijos
const handleSuccess = (message) => {
  console.log('Operación exitosa:', message);
  // Aquí podrías mostrar una notificación al usuario
  alert(message || '¡El inventario se ha actualizado correctamente!');
  
  // Opcionalmente, podrías recargar la lista de inventario o redirigir,
  // pero para eso necesitarías volver a importar y usar 'useRouter'.
};
</script>

<style scoped>
/* Puedes agregar estilos específicos para este componente si lo necesitas */
</style>