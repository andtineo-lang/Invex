<template>
  <div class="invex-landing">
    <Header />

    <!-- Contenedor principal -->
    <div class="registro-container">
      <!-- Progressbar -->
      <ul id="progressbar">
        <li :class="{ active: step >= 1 }">Cuenta</li>
        <li :class="{ active: step >= 2 }">Empresa</li>
        <li :class="{ active: step >= 3 }">Plan</li>
        <li :class="{ active: step >= 4 }">Confirmación</li>
      </ul>

      <!-- Step 1 -->
      <fieldset v-if="step === 1">
        <h2 class="fs-title">Crear tu cuenta</h2>
        <input type="email" v-model="form.email" placeholder="Correo electrónico" required />
        <input type="password" v-model="form.password" placeholder="Contraseña" required />
        <input type="password" v-model="form.confirmPassword" placeholder="Confirmar contraseña" required />
        <button type="button" class="action-button" @click="nextStep">Siguiente</button>
      </fieldset>

      <!-- Step 2 -->
      <fieldset v-if="step === 2">
        <h2 class="fs-title">Datos de la Empresa</h2>
        <div class="input-group">
          <input type="text" v-model="form.rut" placeholder="RUT de la empresa" required />
          <small class="hint">Ejemplo: 76.543.210-K</small>
        </div>
        <div class="input-group">
          <input type="text" v-model="form.company" placeholder="Nombre de la empresa" required />
          <small class="hint">Ejemplo: Agroprodel Ltda.</small>
        </div>
        <div class="input-group">
          <input type="text" v-model="form.industry" placeholder="Rubro (ej: Retail, Alimentos...)" required />
          <small class="hint">Indica el sector en el que opera tu empresa</small>
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="button" class="action-button" @click="nextStep">Siguiente</button>
        </div>
      </fieldset>

          <!-- Step 3 -->
      <fieldset v-if="step === 3">
        <h2 class="fs-title">Selecciona un plan</h2>
        <div class="plans-grid">
          <div
            v-for="p in plans"
            :key="p.name"
            :class="['plan-card', { selected: form.plan === p.name }]"
          >
            <span v-if="p.popular" class="badge">Más Popular</span>
            <h3>{{ p.name }}</h3>
            <p class="price">${{ p.price }} <span>/{{ p.duration }}</span></p>
            <ul>
              <li v-for="feature in p.features" :key="feature">{{ feature }}</li>
            </ul>
            <button type="button" @click="form.plan = p.name">Elegir plan</button>
          </div>
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="button" class="action-button" @click="nextStep">Siguiente</button>
        </div>
      </fieldset>


      <!-- Step 4 -->
      <fieldset v-if="step === 4">
        <h2 class="fs-title">Confirmación</h2>
        <div class="confirm-card">
          <p><strong>Correo:</strong> {{ form.email }}</p>
          <p><strong>Empresa:</strong> {{ form.company }}</p>
          <p><strong>RUT:</strong> {{ form.rut }}</p>
          <p><strong>Rubro:</strong> {{ form.industry }}</p>
          <p><strong>Plan:</strong> {{ form.plan }}</p>
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="submit" class="action-button submit">Crear Cuenta</button>
        </div>
      </fieldset>
    </div>

 
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref, reactive } from 'vue'

const step = ref(1)

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  rut: '',
  company: '',
  industry: '',
  plan: ''
})

const plans = [
  {
    name: 'Plan Trimestral',
    price: 299,
    duration: '3 meses',
    features: ['Hasta 1,000 productos', 'Análisis básico de IA', 'Reportes mensuales', 'Soporte por email']
  },
  {
    name: 'Plan Semestral',
    price: 499,
    duration: '6 meses',
    features: ['Hasta 5,000 productos', 'IA avanzada predictiva', 'Reportes semanales', 'Soporte prioritario', 'Integraciones API'],
    popular: true
  },
  {
    name: 'Plan Anual',
    price: 899,
    duration: 'año',
    features: ['Productos ilimitados', 'IA empresarial completa', 'Reportes en tiempo real', 'Soporte 24/7', 'Consultoría personalizada']
  }
]

const nextStep = () => {
  if (step.value < 4) step.value++
}
const prevStep = () => {
  if (step.value > 1) step.value--
}
</script>

<style scoped>

.invex-landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;   /* Centra verticalmente */
  align-items: center;       /* Centra horizontalmente */
  background: linear-gradient(135deg, #f0fdfa, #ecfdf5);
  padding: 2rem 1rem;        /* espacio de seguridad en pantallas pequeñas */
}

.registro-container {
  max-width: 800px;
  width: 100%;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  padding: 2.5rem 3rem;
  text-align: center;

  /* Animación como login */
  animation: fadeInUp 0.8s ease-in-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


/* Progressbar */
#progressbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  counter-reset: step;
  padding: 0;
}

#progressbar li {
  list-style: none;
  flex: 1;
  text-align: center;
  font-size: 0.9rem;
  text-transform: uppercase;
  position: relative;
  color: #9ca3af;
}

#progressbar li:before {
  content: counter(step);
  counter-increment: step;
  width: 36px;
  height: 36px;
  line-height: 36px;
  display: block;
  margin: 0 auto 10px;
  border-radius: 50%;
  background: #e5e7eb;
  color: #374151;
  font-weight: bold;
  z-index: 2;
  position: relative;
}

#progressbar li:after {
  content: '';
  position: absolute;
  width: 100%;
  height: 3px;
  background: #e5e7eb;
  top: 17px;
  left: -50%;
  z-index: 1;
}

#progressbar li:first-child:after {
  content: none;
}

/* Paso activo */
#progressbar li.active {
  color: #0f766e;
}
#progressbar li.active:before {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: #fff;
}
#progressbar li.active + li:after {
  background: #0f766e;
}

/* Fieldsets como tarjetas */
.registro-container fieldset {
  border: none;
  outline: none;
  background: #fff;
  border-radius: 16px;
  padding: 2rem;
  text-align: left;
}

.fs-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f766e;
  margin-bottom: 1.5rem;
  text-align: center;
}

/* Inputs */
input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  margin-bottom: 1rem;
  width: 100%;
  font-size: 1rem;
}
input:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15);
  outline: none;
}

/* Botones */
.buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}
.action-button.secondary {
  background: #e5e7eb;
  color: #374151;
}
.submit {
  width: 100%;
  background: linear-gradient(135deg, #0f766e, #0d9488);
}

/* Planes */
/* Contenedor de planes */
.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
  justify-items: center;
  margin-top: 2rem;
}

/* Tarjeta de plan */
.plan-card {
  background: #fff;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem 1.5rem;
  text-align: center;
  width: 100%;
  max-width: 300px;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.plan-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.plan-card.selected {
  border-color: #0f766e;
  box-shadow: 0 12px 30px rgba(15,118,110,0.25);
}

/* Badge */
.badge {
  background: #f59e0b;
  color: #fff;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

/* Títulos y precios */
.plan-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #111827;
}

.price {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f766e;
  margin-bottom: 1rem;
}

.price span {
  font-size: 0.9rem;
  font-weight: 400;
  color: #6b7280;
}

/* Lista de características */
.plan-card ul {
  list-style: none;
  padding: 0;
  margin: 1rem 0 1.5rem;
  text-align: left;
}

.plan-card ul li {
  display: flex;
  align-items: center;
  margin-bottom: 0.6rem;
  font-size: 0.95rem;
  color: #374151;
}

.plan-card ul li::before {
  content: "✔";
  color: #10b981;
  font-weight: bold;
  margin-right: 0.5rem;
}

/* Botón dentro de tarjeta */
.plan-card button {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.plan-card button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}

/* Confirmación */
.confirm-card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 16px;
  text-align: left;
  font-size: 1rem;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .plans-grid {
    flex-direction: column;
    align-items: center;
  }
}


</style>
