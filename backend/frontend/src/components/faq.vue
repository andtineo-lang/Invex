<template>
  <div class="invex-page">
    <Header />
    <section class="faq-section">
      <div class="container">
        <h2 class="title">Preguntas frecuentes</h2>
        <div class="faq-grid">
          <div 
            v-for="(item, i) in preguntas" 
            :key="i" 
            class="faq-item" 
            :class="{ 'is-open': item.open }"
            @click="toggle(i)"
          >
            <div class="faq-header">
              <h3>{{ item.q }}</h3>
              <span class="icon" :class="{ rotate: item.open }">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </span>
            </div>
            <transition name="accordion">
              <div v-show="item.open" class="faq-body">
                <p>{{ item.a }}</p>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import { ref } from 'vue'

const preguntas = ref([
  { q: '¿Qué es INVEX?', a: 'INVEX es una plataforma integral de gestión de inventario potenciada por Inteligencia Artificial que te recomienda realizar compras de tus productos que se estan agontando y recomienda cuando impulsar tus productos inactivos para optimizar tu stock.', open: false },
  { q: '¿Cómo se integra con mi sistema actual?', a: 'Disponemos de una API REST completa y plugins para los principales ERPs y plataformas de E-commerce del mercado.', open: false },
  { q: '¿Tiene costo de implementación?', a: 'No, la configuración inicial es gratuita y nuestro equipo te asiste en la migración de tus datos.', open: false },
  { q: '¿Ofrecen soporte técnico?', a: 'Sí, contamos con soporte prioritario 24/7 vía chat y correo electrónico para todos nuestros planes empresariales.', open: false },
  { q: '¿Es seguro alojar mis datos con ustedes?', a: 'Absolutamente. Usamos encriptación de grado militar y servidores redundantes para garantizar la seguridad y disponibilidad de tu información.', open: false }
])

const toggle = (i) => {
  // Opcional: Cerrar otros al abrir uno
  // preguntas.value.forEach((p, index) => {
  //   if (index !== i) p.open = false
  // })
  preguntas.value[i].open = !preguntas.value[i].open
}
</script>

<style scoped>
.invex-page {
  background-color: #f8fafc;
  min-height: 100vh;
}

.faq-section { 
    padding: 6rem 1rem; 
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

.title { 
    text-align: center; 
    font-size: 2.5rem; 
    color: #1e293b; 
    margin-bottom: 3rem;
    font-weight: 700;
}

.faq-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.faq-item { 
    background: #fff; 
    border-radius: 1rem; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); 
    cursor: pointer; 
    transition: all 0.3s ease;
    border: 1px solid transparent;
    overflow: hidden; /* Importante para la animación */
}

.faq-item:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.faq-item.is-open {
    border-color: #0f766e;
}

.faq-header { 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    padding: 1.5rem; 
    background: white;
    position: relative;
    z-index: 2;
}

.faq-header h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #334155;
    margin: 0;
}

.icon { 
    transition: transform 0.3s ease; 
    color: #0f766e; 
    display: flex;
    align-items: center;
}

.icon.rotate { 
    transform: rotate(180deg); 
}

.faq-body { 
    padding: 0 1.5rem 1.5rem 1.5rem; 
    color: #64748b; 
    line-height: 1.6;
    background: white;
}

/* Animación del Acordeón */
.accordion-enter-active, 
.accordion-leave-active { 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
    overflow: hidden; /* Crucial para que no salte */
    max-height: 200px; /* Ajusta esto si tienes respuestas muy largas */
}

.accordion-enter-from, 
.accordion-leave-to { 
    max-height: 0; 
    opacity: 0; 
    padding-top: 0;
    padding-bottom: 0;
}
</style>