<template>
  <div id="app">
    <!-- Header global -->
    <Header />

    <!-- Aquí se renderiza cada página -->
    <router-view />

    <!-- Footer global -->
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Para que el contenido empuje al footer hacia abajo */
router-view {
  flex: 1;
  display: block;
}
</style>
