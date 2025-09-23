<template>
  <div class="invex-landing">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="nav-content">
          <div class="logo">
            <h1>INVEX</h1>
          </div>

          <!-- Menú Navegación -->
          <nav class="nav-links">
            <a @click.prevent="scrollToSection('about')">Sobre Nosotros</a>
            <a @click.prevent="scrollToSection('pricing')">Planes de Suscripción</a>
          </nav>

          <div class="nav-buttons">
            <router-link to="/login">
            <button class="btn-secondary">Iniciar Sesión</button>
            </router-link>
            <router-link to="/registro">
              <button class="btn-primary">Crear Cuenta</button>
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero" ref="heroRef">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title" ref="titleRef">
            Gestión de Stock Inteligente con IA
          </h1>
          <p class="hero-subtitle" ref="subtitleRef">
            Optimiza tu inventario con tecnología de inteligencia artificial.
            Predice demanda, reduce costos y maximiza eficiencia.
          </p>
          <div class="hero-buttons" ref="buttonsRef">
            <router-link to="/registro">
              <button class="btn-primary btn-large">Comenzar Gratis</button>
            </router-link>
            <button class="btn-outline btn-large" @click="scrollToSection('pricing')">Ver Planes</button>
          </div>
          <div class="features-grid" ref="featuresRef">
            <div class="feature-card">
              <div class="feature-icon">📊</div>
              <h3>Análisis Predictivo</h3>
              <p>IA que predice demanda futura</p>
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
        <div class="pricing-grid">
          <div class="pricing-card">
            <div class="plan-header">
              <h3>Plan Trimestral</h3>
              <div class="price">
                <span class="currency">$</span>
                <span class="amount">299</span>
                <span class="period">/3 meses</span>
              </div>
            </div>
            <ul class="features-list">
              <li>Hasta 1,000 productos</li>
              <li>Análisis básico de IA</li>
              <li>Reportes mensuales</li>
              <li>Soporte por email</li>
            </ul>
            <button class="btn-outline btn-full">Comenzar</button>
          </div>

          <div class="pricing-card featured">
            <div class="popular-badge">Más Popular</div>
            <div class="plan-header">
              <h3>Plan Semestral</h3>
              <div class="price">
                <span class="currency">$</span>
                <span class="amount">499</span>
                <span class="period">/6 meses</span>
              </div>
            </div>
            <ul class="features-list">
              <li>Hasta 5,000 productos</li>
              <li>IA avanzada predictiva</li>
              <li>Reportes semanales</li>
              <li>Soporte prioritario</li>
              <li>Integraciones API</li>
            </ul>
            <button class="btn-primary btn-full">Comenzar</button>
          </div>

          <div class="pricing-card">
            <div class="plan-header">
              <h3>Plan Anual</h3>
              <div class="price">
                <span class="currency">$</span>
                <span class="amount">899</span>
                <span class="period">/año</span>
              </div>
            </div>
            <ul class="features-list">
              <li>Productos ilimitados</li>
              <li>IA empresarial completa</li>
              <li>Reportes en tiempo real</li>
              <li>Soporte 24/7</li>
              <li>Consultoría personalizada</li>
            </ul>
            <button class="btn-outline btn-full">Comenzar</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>INVEX</h3>
            <p>Gestión inteligente de inventarios con IA</p>
          </div>
          <div class="footer-section">
            <h4>Producto</h4>
            <ul>
              <li><a href="#">Características</a></li>
              <li><a href="#">Precios</a></li>
              <li><a href="#">Demo</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>Soporte</h4>
            <ul>
              <li><a href="#">Documentación</a></li>
              <li><a href="#">Contacto</a></li>
              <li><a href="#">FAQ</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 INVEX. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

const heroRef = ref(null)
const titleRef = ref(null)
const subtitleRef = ref(null)
const buttonsRef = ref(null)
const featuresRef = ref(null)
const aboutRef = ref(null)
const pricingRef = ref(null)

gsap.registerPlugin(ScrollTrigger, ScrollToPlugin)

// Método para hacer scroll animado
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
  if (typeof gsap !== 'undefined') {
    gsap.set([titleRef.value, subtitleRef.value, buttonsRef.value], {
      opacity: 0,
      y: 50
    })

    gsap.set(featuresRef.value.children, {
      opacity: 0,
      y: 30
    })

    const tl = gsap.timeline()

    tl.to(titleRef.value, {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out"
    })
      .to(subtitleRef.value, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out"
      }, "-=0.5")
      .to(buttonsRef.value, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out"
      }, "-=0.3")
      .to(featuresRef.value.children, {
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger: 0.2,
        ease: "power3.out"
      }, "-=0.3")
  }
})
</script>

<style scoped>
/* Aquí puedes pegar el mismo CSS que ya tienes (lo de header, hero, about, pricing, etc.) */
/* IMPORTANTE: agrega estilos para el nuevo menú de navegación */
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
