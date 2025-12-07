<template>
  <div class="invex-landing">
    <!-- Header con menú -->
    <Header />
   
    <!-- Hero Section -->
    <section id="hero" class="hero" ref="heroRef">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title" ref="titleRef">
            Gestión de Stock Inteligente con IA
          </h1>
          <p class="hero-subtitle" ref="subtitleRef">
            Optimiza tu inventario con tecnología de inteligencia artificial.
            recomienda cuando hacer tu compra y cuando impulsar tus productos, reduce costos y maximiza eficiencia.
          </p>
          <div class="hero-buttons" ref="buttonsRef">
            <router-link to="/registro">
              <button class="btn-primary btn-large">Comenzar Gratis</button>
            </router-link>
            <button class="btn-outline btn-large" @click="scrollToSection('pricing')">
              Ver Planes
            </button>
          </div>
          <div class="features-grid" ref="featuresRef">
            <div class="feature-card">
              <div class="feature-icon">💡</div>
              <h3>Recomendación inteligente</h3>
              <p>IA que recomienda cuando hacer las compras de tus productos criticos y cuando impulsar tus productos inactivos</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">⚡</div>
              <h3>Automatización</h3>
              <p>Procesos automáticos de restock</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">📈</div>
              <h3>Optimización</h3>
              <p>Reduce costos hasta 30%</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about" ref="aboutRef">
      <div class="container">
        <div class="section-header">
          <h2>Sobre Nosotros</h2>
          <p>Revolucionando la gestión de inventarios con inteligencia artificial</p>
        </div>
        <div class="about-content">
          <div class="about-text">
            <h3>¿Qué hace INVEX?</h3>
            <p>
              INVEX es una plataforma revolucionaria que utiliza inteligencia artificial
              para transformar la gestión de inventarios. Nuestro sistema aprende de tus
              patrones de venta, predice la demanda futura y optimiza automáticamente
              tus niveles de stock.
            </p>
            <div class="benefits">
              <div class="benefit">
                <span class="benefit-icon">✓</span>
                <span>Reducción de costos operativos hasta 30%</span>
              </div>
              <div class="benefit">
                <span class="benefit-icon">✓</span>
                <span>Predicción de demanda con 95% de precisión</span>
              </div>
              <div class="benefit">
                <span class="benefit-icon">✓</span>
                <span>Automatización completa de procesos</span>
              </div>
              <div class="benefit">
                <span class="benefit-icon">✓</span>
                <span>Integración con sistemas existentes</span>
              </div>
            </div>
          </div>
          <div class="about-visual">
            <div class="stats-card">
              <div class="stat">
                <h4>500+</h4>
                <p>Empresas confían en nosotros</p>
              </div>
              <div class="stat">
                <h4>95%</h4>
                <p>Precisión en predicciones</p>
              </div>
              <div class="stat">
                <h4>30%</h4>
                <p>Reducción de costos</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
  <section id="pricing" class="pricing" ref="pricingRef">
    <div class="container">
        <div class="section-header">
            <h2>Planes de Suscripción</h2>
            <p>Elige el plan que mejor se adapte a tu negocio</p>
        </div>

        <div class="pricing-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); max-width: 900px; margin: 0 auto;">

            <div class="pricing-card">
                <div class="plan-header">
                    <h3>Plan Inicial</h3>
                    <div class="price">
                        <span class="currency">$</span>
                        <span class="amount">0</span>
                        <span class="period">/mes</span>
                    </div>
                </div>
                <ul class="features-list">
                    <li>✓ Máximo 50 productos</li>
                    <li>✓ Reportes básicos</li>
                    <li style="color: #9ca3af; opacity: 0.8;">
                        <span style="color: #ef4444; font-weight: bold; margin-right: 5px;">✕</span>
                        Sin Recomendaciones de IA
                    </li>
                    <li style="color: #9ca3af; opacity: 0.8;">
                        <span style="color: #ef4444; font-weight: bold; margin-right: 5px;">✕</span>
                        Sin predicción de demanda
                    </li>
                </ul>
                <router-link :to="{ name: 'Registro' }" class="btn-outline btn-full">
                    Comenzar Gratis
                </router-link>
            </div>

            <div class="pricing-card featured">
                <div class="popular-badge">Recomendado</div>
                <div class="plan-header">
                    <h3>Plan INVEX PRO</h3>
                    <div class="price">
                        <span class="currency">$</span>
                        <span class="amount">30.000</span>
                        <span class="period">/mes</span>
                    </div>
                </div>
                <ul class="features-list">
                    <li>✓ Productos Ilimitados</li>
                    <li>✓ IA Estratégica Completa</li>
                    <li>✓ Predicción de demanda</li>
                    <li>✓ Prioridad en soporte</li>
                </ul>
                <router-link :to="{ name: 'Registro' }" class="btn-primary btn-full">
                    Obtener Plan PRO
                </router-link>
            </div>

        </div> 
    </div> </section>
 
  </div>
</template>

<script setup>

import Header from './Header.vue'
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

gsap.registerPlugin(ScrollTrigger, ScrollToPlugin)

const heroRef = ref(null)
const titleRef = ref(null)
const subtitleRef = ref(null)
const buttonsRef = ref(null)
const featuresRef = ref(null)

const scrollToSection = (id) => {
  const section = document.getElementById(id)
  if (section) {
    gsap.to(window, {
      duration: 1,
      scrollTo: { y: section, offsetY: 80 },
      ease: "power2.inOut"
    })
  }
}

onMounted(() => {
  gsap.set([titleRef.value, subtitleRef.value, buttonsRef.value], {
    opacity: 0,
    y: 50
  })
  gsap.set(featuresRef.value.children, { opacity: 0, y: 30 })

  gsap.timeline()
    .to(titleRef.value, { opacity: 1, y: 0, duration: 1 })
    .to(subtitleRef.value, { opacity: 1, y: 0, duration: 0.8 }, "-=0.5")
    .to(buttonsRef.value, { opacity: 1, y: 0, duration: 0.8 }, "-=0.3")
    .to(featuresRef.value.children, {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.2
    }, "-=0.3")
})
</script>

<style scoped>
.nav-links {
  display: flex;
  gap: 1.5rem;
  margin-left: 2rem;
}

.nav-links a {
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #0f766e;
}
</style>
