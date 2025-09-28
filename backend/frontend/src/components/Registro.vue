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
          <!-- ✅ Nueva opción para usuarios con cuenta -->
  <p class="redirect-login">
    ¿Ya tienes una cuenta? 
    <router-link to="/login">Inicia sesión aquí</router-link>
  </p>
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
          <small class="hint">Ejemplo: Farmacy Ltda.</small>
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
          <button type="button" class="action-button submit" @click="handleRegister">
            Crear Cuenta
          </button>
        </div>
      </fieldset>
    </div>

    <!-- ✅ Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-box">
        <h2>{{ modalTitle }}</h2>
        <p>{{ modalMessage }}</p>
        <button @click="showModal = false">Cerrar</button>
      </div>
    </div>

  </div> 
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref, reactive } from 'vue'

const step = ref(1)
const showModal = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')

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

// ✅ Abrir modal
const openModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

// ---------------------- VALIDACIONES ----------------------
const validarEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const validarPassword = (password) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(password)
const validarRut = (rut) => /^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$/.test(rut)

// ---------------------- NAVEGACIÓN ENTRE PASOS ----------------------
const nextStep = () => {
  if (step.value === 1) {
    if (!form.email || !form.password || !form.confirmPassword) {
      openModal('⚠️ Campos incompletos', 'Por favor completa todos los campos.')
      return
    }
    if (!validarEmail(form.email)) {
      openModal('📧 Correo inválido', 'Por favor ingresa un correo válido.')
      return
    }
    if (!validarPassword(form.password)) {
      openModal('🔐 Contraseña inválida', 'Debe tener mínimo 8 caracteres, incluir mayúscula, minúscula, número y carácter especial.')
      return
    }
    if (form.password !== form.confirmPassword) {
      openModal('❌ Contraseñas diferentes', 'Las contraseñas no coinciden.')
      return
    }
  }

  if (step.value === 2) {
    if (!form.rut || !form.company || !form.industry) {
      openModal('🏢 Datos incompletos', 'Por favor completa todos los datos de la empresa.')
      return
    }
    if (!validarRut(form.rut)) {
      openModal('🆔 RUT inválido', 'El formato debe ser como 12.345.678-9.')
      return
    }
  }

  if (step.value === 3 && !form.plan) {
    openModal('📌 Selección requerida', 'Por favor selecciona un plan antes de continuar.')
    return
  }

  if (step.value < 4) step.value++
}

const prevStep = () => {
  if (step.value > 1) step.value--
}

// ---------------------- FINALIZAR REGISTRO ----------------------
const handleRegister = () => {
  openModal(
    '✅ Registro exitoso',
    `Se ha creado la cuenta con los siguientes datos:\n\n📧 Correo: ${form.email}\n🏢 Empresa: ${form.company}\n🆔 RUT: ${form.rut}\n🏭 Rubro: ${form.industry}\n💳 Plan: ${form.plan}`
  )
}
</script>

<style scoped>
/* Mantengo todos tus estilos originales del formulario */
</style>


<style scoped>


.invex-landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0fdfa, #ecfdf5);
  padding: 2rem 1rem;
}

.registro-container {
  max-width: 800px;
  width: 100%;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  padding: 2.5rem 3rem;
  text-align: center;
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

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
  justify-items: center;
  margin-top: 2rem;
}

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

.confirm-card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 16px;
  text-align: left;
  font-size: 1rem;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .plans-grid {
    flex-direction: column;
    align-items: center;
  }
}
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* Fondo oscuro */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Caja del modal */
.modal-box {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

/* Título */
.modal-box h2 {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* Mensaje */
.modal-box p {
  font-size: 1rem;
  color: #374151;
  margin-bottom: 1.5rem;
  white-space: pre-line; /* respeta saltos de línea */
}

/* Botón */
.modal-box button {
  padding: 0.6rem 1.2rem;
  background: #2563eb; /* Azul */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.modal-box button:hover {
  background: #1d4ed8;
}

</style>
