

<template>
  <div class="invex-landing">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="nav-content">
          <div class="logo">
            <h1>INVEX</h1>
          </div>
          <div class="nav-buttons">
            <button class="btn-secondary">Iniciar Sesión</button>
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
            <button class="btn-primary btn-large">Comenzar Gratis</button>
            <button class="btn-outline btn-large">Ver Demo</button>
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
    <section class="about" ref="aboutRef">
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
    <section class="pricing" ref="pricingRef">
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

const heroRef = ref(null)
const titleRef = ref(null)
const subtitleRef = ref(null)
const buttonsRef = ref(null)
const featuresRef = ref(null)
const aboutRef = ref(null)
const pricingRef = ref(null)

gsap.registerPlugin(ScrollTrigger)

onMounted(() => {
  // Verificar si GSAP está disponible
  if (typeof gsap !== 'undefined') {
    // Animación inicial del hero
    gsap.set([titleRef.value, subtitleRef.value, buttonsRef.value], { 
      opacity: 0, 
      y: 50 
    })
    
    gsap.set(featuresRef.value.children, { 
      opacity: 0, 
      y: 30 
    })

    // Timeline de entrada
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

    // Animaciones de scroll
    if (typeof ScrollTrigger !== 'undefined') {
      // Animación de la sección About
      gsap.fromTo(aboutRef.value.querySelector('.about-content'), 
        { opacity: 0, y: 100 },
        {
          opacity: 1,
          y: 0,
          duration: 1,
          ease: "power3.out",
          scrollTrigger: {
            trigger: aboutRef.value,
            start: "top 80%",
            end: "bottom 20%",
            toggleActions: "play none none reverse"
          }
        }
      )

      // Animación de las tarjetas de precios
      gsap.fromTo(pricingRef.value.querySelectorAll('.pricing-card'), 
        { opacity: 0, y: 50, scale: 0.9 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.8,
          stagger: 0.2,
          ease: "power3.out",
          scrollTrigger: {
            trigger: pricingRef.value,
            start: "top 80%",
            end: "bottom 20%",
            toggleActions: "play none none reverse"
          }
        }
      )
    }
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.invex-landing {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.6;
  color: #1f2937;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e5e7eb;
  z-index: 1000;
  padding: 1rem 0;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f766e;
  letter-spacing: -0.02em;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(15, 118, 110, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #374151;
  border: 2px solid #d1d5db;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  border-color: #0f766e;
  color: #0f766e;
}

.btn-outline {
  background: transparent;
  color: #0f766e;
  border: 2px solid #0f766e;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: #0f766e;
  color: white;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.btn-full {
  width: 100%;
}

/* Hero Section */
.hero {
  padding: 8rem 0 4rem;
  background: linear-gradient(135deg, #f0fdfa 0%, #ecfdf5 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: #0f766e;
  margin-bottom: 1.5rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #4b5563;
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f766e;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #6b7280;
}

/* About Section */
.about {
  padding: 6rem 0;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f766e;
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.1rem;
  color: #6b7280;
}

.about-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.about-text h3 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #0f766e;
  margin-bottom: 1.5rem;
}

.about-text p {
  font-size: 1.1rem;
  color: #4b5563;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.benefits {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.benefit {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.benefit-icon {
  background: #10b981;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
  flex-shrink: 0;
}

.stats-card {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  padding: 2.5rem;
  border-radius: 20px;
  color: white;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.stat {
  text-align: center;
}

.stat h4 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.stat p {
  opacity: 0.9;
}

/* Pricing Section */
.pricing {
  padding: 6rem 0;
  background: #f9fafb;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.pricing-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  transition: transform 0.3s ease;
}

.pricing-card:hover {
  transform: translateY(-5px);
}

.pricing-card.featured {
  border: 3px solid #0f766e;
  transform: scale(1.05);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #f59e0b;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.plan-header {
  text-align: center;
  margin-bottom: 2rem;
}

.plan-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f766e;
  margin-bottom: 1rem;
}

.price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem;
}

.currency {
  font-size: 1.5rem;
  color: #6b7280;
}

.amount {
  font-size: 3rem;
  font-weight: 800;
  color: #0f766e;
}

.period {
  font-size: 1rem;
  color: #6b7280;
}

.features-list {
  list-style: none;
  margin-bottom: 2rem;
}

.features-list li {
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
  color: #4b5563;
}

.features-list li:last-child {
  border-bottom: none;
}

.features-list li::before {
  content: "✓";
  color: #10b981;
  font-weight: bold;
  margin-right: 0.75rem;
}

/* Footer */
.footer {
  background: #1f2937;
  color: white;
  padding: 3rem 0 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3,
.footer-section h4 {
  margin-bottom: 1rem;
  color: #0f766e;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #d1d5db;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: #0f766e;
}

.footer-bottom {
  border-top: 1px solid #374151;
  padding-top: 1rem;
  text-align: center;
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .about-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .nav-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .pricing-card.featured {
    transform: none;
  }
  
  .stats-card {
    grid-template-columns: 1fr;
  }
}
</style>