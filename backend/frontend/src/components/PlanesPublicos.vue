<template>
  <div class="invex-page">
    
    <section class="pricing-container">
      <div class="header">
        <h1 class="animate-fade-in">Planes y Precios</h1>
        <p>Elige la potencia que tu negocio necesita</p>
      </div>

      <div class="plans-wrapper">
        <!-- PLAN GRATUITO -->
        <div class="plan-card">
          <div class="badge-free">GRATIS</div>
          <h2>Plan Inicial</h2>
          <div class="price">$0 <span class="period">/mes</span></div>
          
          <ul class="features">
            <li><span class="check">✓</span> Máximo 50 productos</li>
            <li><span class="check">✓</span> Reportes básicos</li>
            <li><span class="cross">❌</span> Sin Inteligencia Artificial</li>
            <li><span class="cross">❌</span> Sin predicción de demanda</li>
          </ul>

          <!-- Botón redirige a Registro para nuevos usuarios -->
          <router-link :to="{ name: 'Registro' }" class="btn-secondary">
            Comenzar Gratis
          </router-link>
        </div>

        <!-- PLAN PRO -->
        <div class="plan-card pro featured">
          <div class="popular-badge">Recomendado</div>
          <h2>Plan INVEX PRO</h2>
          <div class="price">$30.000 <span class="period">/mes</span></div>
          
          <ul class="features">
            <li><span class="check">✓</span> <strong>Productos Ilimitados</strong></li>
            <li><span class="check">✓</span> <strong>IA Estratégica Completa</strong></li>
            <li><span class="check">✓</span> Predicción de demanda</li>
            <li><span class="check">✓</span> Prioridad en soporte</li>
          </ul>
          
          <!-- Botón redirige a Registro para nuevos usuarios -->
          <router-link :to="{ name: 'Registro' }" class="btn-primary btn-upgrade">
            Obtener Plan PRO
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Lógica de presentación para la vista pública
</script>

<style scoped>
/* --- ESTILOS VISUALES (Copiados y adaptados de tu referencia) --- */
.invex-page { 
  min-height: 100vh; 
  background-color: #f8fafc; 
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pricing-container { 
  padding: 4rem 2rem; 
  max-width: 900px; 
  margin: 0 auto; 
  text-align: center; 
  width: 100%;
}

.header h1 { 
  color: #0f766e; 
  font-size: 2.5rem; 
  margin-bottom: 0.5rem; 
  font-weight: 800; 
}

.header p { 
  color: #64748b; 
  margin-bottom: 3rem; 
  font-size: 1.1rem; 
}

.plans-wrapper { 
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
  gap: 2rem; 
  align-items: center; 
  justify-content: center;
}

/* Tarjeta Base */
.plan-card { 
  background: white; 
  border-radius: 1.5rem; 
  padding: 2.5rem 2rem; 
  position: relative; 
  box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
  border: 1px solid #e2e8f0; 
  text-align: left; 
  height: 100%; 
  display: flex; 
  flex-direction: column;
}

/* Tarjeta PRO (Destacada) */
.plan-card.pro { 
  border: 2px solid #8b5cf6; 
  box-shadow: 0 20px 25px -5px rgba(139, 92, 246, 0.15); 
  transform: scale(1.05); 
  z-index: 10; 
}

/* Badges */
.badge-free { 
  position: absolute; 
  top: -12px; 
  left: 50%; 
  transform: translateX(-50%); 
  background: #e5e7eb; 
  padding: 0.5rem 1.5rem; 
  border-radius: 20px; 
  font-size: 0.9rem; 
  font-weight: 700; 
  color: #374151; 
}

.popular-badge { 
  background: #8b5cf6; 
  color: #fff; 
  position: absolute; 
  top: -16px; 
  left: 50%; 
  transform: translateX(-50%); 
  padding: 0.5rem 1.5rem; 
  border-radius: 20px; 
  font-size: 0.9rem; 
  font-weight: 700; 
}

h2 { 
  font-size: 1.5rem; 
  color: #1e293b; 
  margin-bottom: 0.5rem; 
  font-weight: 700; 
  text-align: center; 
}

.price { 
  font-size: 2.5rem; 
  font-weight: 800; 
  color: #0f766e; 
  margin: 1.5rem 0; 
  display: flex; 
  justify-content: center; 
  align-items: baseline; 
  gap: 5px; 
}

.period { 
  font-size: 1rem; 
  color: #64748b; 
  font-weight: 400; 
}

ul.features { 
  list-style: none; 
  padding: 0; 
  margin: 1rem 0 2rem 0; 
  flex-grow: 1; 
}

ul.features li { 
  margin-bottom: 1rem; 
  color: #4b5563; 
  display: flex; 
  align-items: center; 
  font-size: 0.95rem; 
}

.check { 
  color: #10b981; 
  margin-right: 12px; 
  font-weight: bold; 
}

.cross { 
  color: #ef4444; 
  margin-right: 12px; 
  font-weight: bold; 
}

/* Botones */
.btn-primary, .btn-secondary { 
  display: block;
  width: 100%; 
  padding: 0.9rem; 
  border-radius: 0.5rem; 
  font-weight: 600; 
  cursor: pointer; 
  transition: all 0.2s; 
  font-size: 1rem; 
  margin-top: auto; 
  text-align: center;
  text-decoration: none;
}

/* Estilo botón PRO */
.btn-primary { 
  background-color: #8b5cf6; 
  color: white; 
  border: none; 
}

.btn-primary:hover { 
  background-color: #7c3aed; 
  transform: translateY(-2px); 
}

/* Estilo botón Gratis (adaptado para que parezca botón) */
.btn-secondary {
  background: #fff; 
  color: #4b5563; 
  border: 2px solid #e2e8f0; 
}

.btn-secondary:hover {
  border-color: #94a3b8;
  background-color: #f8fafc;
}

@media (max-width: 768px) { 
  .plans-wrapper { 
    grid-template-columns: 1fr; 
    max-width: 400px;
    margin: 0 auto;
  } 
  
  .plan-card.pro {
    transform: none;
    margin-top: 1rem;
  }
}
</style>