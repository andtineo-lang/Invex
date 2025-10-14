<template>
  <div id="public-layout">
    <Header />

    <main>
      <router-view />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue' // Asegúrate que la ruta sea correcta
import Footer from '@/components/Footer.vue' // Asegúrate que la ruta sea correcta
</script>

<style scoped>
/* Puedes añadir estilos específicos para el layout público si lo necesitas */
main {
  /* Por ejemplo, un padding mínimo para que el contenido no pegue con el header/footer */
  padding-top: 60px; /* Ajusta esto a la altura de tu Header */
}
</style>