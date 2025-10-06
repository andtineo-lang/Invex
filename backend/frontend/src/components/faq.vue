<template>
  <div class="faq-page">
    <Header />
    <section class="faq-section">
      <div class="container">
        <h2 class="title">Preguntas frecuentes</h2>
        <div v-for="(item, i) in preguntas" :key="i" class="faq-item" @click="toggle(i)">
          <div class="faq-header">
            <h3>{{ item.q }}</h3>
            <span :class="{ open: item.open }">⌄</span>
          </div>
          <transition name="accordion">
            <div v-show="item.open" class="faq-body">
              <p>{{ item.a }}</p>
            </div>
          </transition>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import { ref } from 'vue'

const preguntas = ref([
  { q: '¿Qué es INVEX?', a: 'Una plataforma de gestión de inventario con IA.', open: false },
  { q: '¿Cómo se usa?', a: 'Desde un panel web simple y responsive.', open: false },
  { q: '¿Tiene soporte?', a: 'Sí, soporte por chat y correo.', open: false }
])

const toggle = (i) => (preguntas.value[i].open = !preguntas.value[i].open)
</script>

<style scoped>
.faq-page { min-height: 100vh; background: #f8fafc; }
.faq-section { padding: 5rem 2rem; max-width: 800px; margin: auto; }
.title { text-align: center; font-size: 2rem; color: #064e3b; margin-bottom: 2rem; }
.faq-item { background: #fff; border-radius: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); cursor: pointer; transition: transform .2s; }
.faq-item:hover { transform: translateY(-2px); }
.faq-header { display: flex; justify-content: space-between; align-items: center; padding: 1.2rem 1.5rem; font-weight: 600; color: #111827; }
.faq-header span { transition: transform .3s; color: #10b981; font-size: 1.2rem; }
.faq-header span.open { transform: rotate(180deg); }
.faq-body { padding: 0 1.5rem 1rem; color: #4b5563; line-height: 1.5; }
.accordion-enter-active, .accordion-leave-active { transition: all .35s ease; }
.accordion-enter-from, .accordion-leave-to { max-height: 0; opacity: 0; transform: translateY(-5px); }
.accordion-enter-to, .accordion-leave-from { max-height: 200px; opacity: 1; transform: translateY(0); }
</style>
