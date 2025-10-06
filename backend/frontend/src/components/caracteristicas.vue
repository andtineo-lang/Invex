<template>
  <div class="invex-page">
    <Header />
    <section class="page-section">
      <div class="container">
        <div class="section-header">
          <h2>Características de INVEX</h2>
          <p>Todo lo que tu empresa necesita para gestionar inventario de forma inteligente</p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>Inteligencia Artificial Predictiva</h3>
            <p>Predice la demanda de productos con base en tus históricos y tendencias del mercado.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📦</div>
            <h3>Gestión Automática de Stock</h3>
            <p>Control total del inventario en tiempo real. Evita quiebres o exceso de stock.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Reportes Avanzados</h3>
            <p>Obtén reportes dinámicos con gráficos e indicadores de rendimiento.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <h3>Integración con ERP y E-commerce</h3>
            <p>Sincroniza automáticamente tus ventas y compras desde sistemas externos.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import gsap from 'gsap'
import { onMounted } from 'vue'

onMounted(() => {
  gsap.from('.feature-card', { opacity: 0, y: 30, stagger: 0.2, duration: 0.8 })
})
</script>

<style scoped>
.page-section {
  padding: 6rem 1rem;
}
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}
.feature-card {
  background: #fff;
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-5px);
}
.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}
</style>
