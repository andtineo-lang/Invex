<template>
  <div id="app">
    <Header v-if="showLayout" />
    <router-view />
    <Footer v-if="showLayout" />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Lógica mejorada: si la ruta empieza con '/app', no muestra el layout.
const showLayout = computed(() => {
  return !route.path.startsWith('/app')
})
</script>

<style>
/* ...tus estilos... */
</style>