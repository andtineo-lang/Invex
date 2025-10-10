<template>
  <div id="app">
    <!-- Header condicional: solo se muestra en algunas rutas -->
    <Header v-if="showLayout" />

    <!-- Aquí se renderiza cada página -->
      <main>
      <router-view />
    </main>

    <!-- Footer condicional: solo se muestra en algunas rutas -->
    <Footer v-if="showLayout" />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Define en qué rutas NO quieres mostrar Header y Footer
const routesWithoutLayout = [
  '/app/inventario',
  '/app/inventario/importar',
  '/app/proyecciones',
  '/app/reportes',
  '/app/usuarios',
  '/app/configuracion'
]
// --- 3. Lógica reactivada para que funcione el v-if ---
const showLayout = computed(() => {
  // Si la ruta actual NO está en la lista, muestra el layout.
  return !routesWithoutLayout.includes(route.path)
})
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