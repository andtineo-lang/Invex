<template>
  <div class="invex-page">
    <Header />
    <section class="page-section">
      <div class="container">
        <div class="section-header">
          <h2>Planes y Precios</h2>
          <p>Elige el plan que se adapte al crecimiento de tu empresa</p>
        </div>

        <div class="pricing-grid">
          <div class="pricing-card">
            <h3>Básico</h3>
            <div class="price">$199 / 3 meses</div>
            <ul>
              <li>500 productos</li>
              <li>Reportes mensuales</li>
              <li>Soporte por correo</li>
            </ul>
            <button class="btn-outline">Seleccionar</button>
          </div>

          <div class="pricing-card featured">
            <div class="popular-badge">Más Popular</div>
            <h3>Pro</h3>
            <div class="price">$399 / 6 meses</div>
            <ul>
              <li>5,000 productos</li>
              <li>IA avanzada</li>
              <li>Soporte prioritario</li>
            </ul>
            <button class="btn-primary">Seleccionar</button>
          </div>

          <div class="pricing-card">
            <h3>Empresarial</h3>
            <div class="price">$699 / año</div>
            <ul>
              <li>Productos ilimitados</li>
              <li>Consultoría personalizada</li>
              <li>Integraciones API</li>
            </ul>
            <button class="btn-outline">Seleccionar</button>
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
  gsap.from('.pricing-card', { opacity: 0, y: 40, duration: 0.6, stagger: 0.3 })
})
</script>

<style scoped>
.page-section { padding: 6rem 1rem; text-align: center; }
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}
.pricing-card {
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 4px 14px rgba(0,0,0,0.05);
  padding: 2rem;
  position: relative;
  transition: transform 0.3s ease;
}
.pricing-card:hover { transform: translateY(-8px); }
.popular-badge {
  background: #0f766e;
  color: #fff;
  position: absolute;
  top: -12px;
  right: 20px;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-size: 0.8rem;
}
.price {
  font-size: 1.8rem;
  margin: 1rem 0;
}
</style>
