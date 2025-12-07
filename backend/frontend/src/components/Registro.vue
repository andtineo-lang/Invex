<template>
  <div class="invex-landing">
    <Header />

    <div class="registro-container">
      <ul id="progressbar">
        <li :class="{ active: step >= 1 }">Cuenta</li>
        <li :class="{ active: step >= 2 }">Empresa</li>
        <li :class="{ active: step >= 3 }">Plan</li>
        <li :class="{ active: step >= 4 }">Confirmación</li>
        <li :class="{ active: step >= 5 }">Finalizar</li>
      </ul>

      <fieldset v-if="step === 1">
        <h2 class="fs-title">Crear tu cuenta</h2>
        <input 
          type="text" 
          v-model="form.name" 
          placeholder="Nombre completo" 
          required 
        />
        <input 
          type="email" 
          v-model="form.email" 
          placeholder="Correo electrónico" 
          required 
        />
        
        <div class="password-container">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="form.password" 
            placeholder="Contraseña" 
            required 
          />
          <span class="toggle-icon" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </span>
        </div>

        <div class="password-container">
          <input 
            :type="showConfirm ? 'text' : 'password'" 
            v-model="form.confirmPassword" 
            placeholder="Confirmar contraseña" 
            required 
          />
          <span class="toggle-icon" @click="showConfirm = !showConfirm">
            {{ showConfirm ? '🙈' : '👁️' }}
          </span>
        </div>

        <button type="button" class="action-button" @click="nextStep">Siguiente</button>
        
        <p class="redirect-login">
          ¿Ya tienes una cuenta? 
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </fieldset>

      <fieldset v-if="step === 2">
        <h2 class="fs-title">Datos de la Empresa</h2>
        <div class="input-group">
          <input 
            type="text" 
            :value="form.rut" 
            @input="handleRutInput" 
            placeholder="RUT de la empresa" 
            required 
            maxlength="12"
          />
        </div>
        <div class="input-group">
          <input 
            type="text" 
            v-model="form.company" 
            placeholder="Nombre de la empresa" 
            required 
          />
        </div>
        <div class="input-group">
          <input 
            type="text" 
            v-model="form.industry" 
            placeholder="Rubro (ej: Retail, Alimentos...)" 
            required 
          />
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="button" class="action-button" @click="nextStep">Siguiente</button>
        </div>
      </fieldset>

      <fieldset v-if="step === 3">
        <h2 class="fs-title">Selecciona un plan</h2>
        <div class="plans-grid">
          <div
            v-for="p in plans"
            :key="p.id"
            :class="['plan-card', { selected: form.planId === p.id }]"
            @click="selectPlan(p)"
          >
            <span v-if="p.popular" class="badge">Recomendado</span>
            <h3>{{ p.name }}</h3>
            <p class="price">
              {{ p.price === 0 ? 'Gratis' : '$' + p.price }} 
              <span v-if="p.price > 0">/mes</span>
            </p>
            <ul>
              <li v-for="feature in p.features" :key="feature">{{ feature }}</li>
            </ul>
            <button type="button">
              {{ form.planId === p.id ? 'Seleccionado' : 'Elegir plan' }}
            </button>
          </div>
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="button" class="action-button" @click="nextStep">Siguiente</button>
        </div>
      </fieldset>

      <fieldset v-if="step === 4">
        <h2 class="fs-title">Confirmación</h2>
        <div class="confirm-card">
          <p><strong>Nombre:</strong> {{ form.name }}</p>
          <p><strong>Empresa:</strong> {{ form.company }}</p>
          <p><strong>Plan seleccionado:</strong> {{ getPlanName(form.planId) }}</p>
          <p><strong>Costo:</strong> {{ selectedPlanPrice === 0 ? 'GRATIS' : '$' + selectedPlanPrice }}</p>
        </div>
        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
          <button type="button" class="action-button submit" @click="nextStep">
            {{ selectedPlanPrice === 0 ? 'Finalizar Registro' : 'Ir a Pagar' }}
          </button>
        </div>
      </fieldset>

      <fieldset v-if="step === 5">
        <h2 class="fs-title">
          {{ selectedPlanPrice === 0 ? 'Creando Cuenta' : 'Confirmar Pago' }}
        </h2>
        
        <div class="payment-summary">
          <p>Estás suscribiéndote al plan <strong>{{ getPlanName(form.planId) }}</strong>.</p>
          <p class="total-amount">
            Total a pagar: <strong>{{ selectedPlanPrice === 0 ? '$0' : '$' + selectedPlanPrice }}</strong>
          </p>
          
          <p v-if="selectedPlanPrice > 0" class="redirect-message">
            Serás redirigido a Webpay (Transbank) para completar la suscripción.
          </p>
          <p v-else class="redirect-message">
            Estamos configurando tu cuenta gratuita, esto tomará unos segundos.
          </p>
        </div>

        <div class="buttons">
          <button type="button" class="action-button secondary" @click="prevStep" :disabled="isLoading">Atrás</button>
          <button type="button" class="action-button submit" @click="handleFinalProcess" :disabled="isLoading">
            <span v-if="!isLoading">
              {{ selectedPlanPrice === 0 ? 'Crear Cuenta' : 'Pagar Ahora' }}
            </span>
            <span v-else class="spinner"></span>
          </button>
        </div>
      </fieldset>
    </div>

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
import Header from '@/components/Header.vue';
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const step = ref(1);
const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');
const isLoading = ref(false);
const showPassword = ref(false);
const showConfirm = ref(false);

// 1. DEFINICIÓN DE LOS 2 PLANES
const plans = [
  { 
    id: 'free',
    name: 'Plan Inicial', 
    price: 0, 
    features: [
        'Máximo 50 productos', 
        'Gestión de inventario básica',
        'Soporte por correo'
    ] 
  },
  { 
    id: 'pro',
    name: 'Plan INVEX Pro', 
    price: 15000, 
    popular: true,
    features: [
        'Productos Ilimitados',
        'IA Predictiva de Stock',
        'Reportes Avanzados',
        'Soporte Prioritario 24/7'
    ] 
  }
];

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  rut: '',
  company: '',
  industry: '',
  planId: '', 
});

// Helpers para Rut y Planes
const handleRutInput = (event) => {
  let value = event.target.value.replace(/[^\dkK]/g, '');
  if (!value) { form.rut = ''; return; }
  value = value.replace(/[.-]/g, '');
  const body = value.slice(0, -1);
  const dv = value.slice(-1).toUpperCase();
  form.rut = body ? `${body.replace(/\B(?=(\d{3})+(?!\d))/g, ".")}-${dv}` : dv;
};

const selectPlan = (plan) => {
    form.planId = plan.id;
};

const getPlanName = (id) => {
    const p = plans.find(plan => plan.id === id);
    return p ? p.name : '';
};

const selectedPlanPrice = computed(() => {
    const selectedPlan = plans.find(p => p.id === form.planId);
    return selectedPlan ? selectedPlan.price : 0;
});

const openModal = (title, message) => {
  modalTitle.value = title;
  modalMessage.value = message;
  showModal.value = true;
};

// Validaciones
const validarEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
const validarPassword = (password) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/.test(password);
const validarRut = (rut) => /^\d{1,2}(\.\d{3}){2}-[\dkK]$/.test(rut);

const nextStep = () => {
  // PASO 1: Validar Usuario
  if (step.value === 1) {
    if (!form.name || !form.email || !form.password || !form.confirmPassword) {
        return openModal('⚠️ Campos incompletos', 'Por favor completa todos los campos.');
    }
    if (!validarEmail(form.email)) return openModal('📧 Correo inválido', 'Revisa tu correo.');
    if (!validarPassword(form.password)) return openModal('🔐 Contraseña débil', 'Debe tener min 8 caracteres, mayúscula, número y símbolo.');
    if (form.password !== form.confirmPassword) return openModal('❌ Error', 'Las contraseñas no coinciden.');
  }

  // PASO 2: Validar Empresa
  if (step.value === 2) {
    if (!form.rut || !form.company) return openModal('🏢 Datos incompletos', 'Faltan datos de la empresa.');
    if (!validarRut(form.rut)) return openModal('🆔 RUT inválido', 'Formato incorrecto (ej: 12.345.678-9).');
  }

  // PASO 3: Validar Plan
  if (step.value === 3 && !form.planId) return openModal('📌 Selección requerida', 'Debes elegir un plan.');
  
  if (step.value < 5) step.value++;
};

const prevStep = () => { if (step.value > 1) step.value--; };

// --- LÓGICA PRINCIPAL (CORREGIDO NOMBRE DE CAMPOS) ---
const handleFinalProcess = async () => {
    if (isLoading.value) return;
    isLoading.value = true;

    try {
        // Opción A: Es GRATIS -> Registrar directamente
        if (selectedPlanPrice.value === 0) {
            
            // MAPEO DE DATOS CORREGIDO:
            const payload = {
                // Campos de Usuario (Django User)
                email: form.email,
                username: form.email,
                first_name: form.name,
                password: form.password,
                re_password: form.confirmPassword,
                
                // Campos de Empresa (CORREGIDOS PARA TU BACKEND)
                rut: form.rut,
                empresa_nombre: form.company, // <--- AQUÍ ESTABA EL ERROR (antes decía 'company')
                rubro: form.industry,         // <--- CAMBIAMOS 'industry' POR 'rubro' (por si acaso)
                
                is_active: true,
                subscription_status: 'free'
            };

            // Usamos la URL que vimos que funcionó (la que dio error 400 es la correcta porque el servidor respondió)
            const response = await fetch('http://127.0.0.1:8000/api/auth/registro/', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload) 
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                // Limpiamos el mensaje de error para que se vea bonito en el modal
                const errorMsg = JSON.stringify(errorData, null, 2).replace(/["{}[\]]/g, '').trim(); 
                throw new Error(errorMsg || 'Error al crear usuario gratuito');
            }
            
            // Éxito
            openModal('✅ Cuenta Creada', 'Tu cuenta gratuita ha sido creada. Inicia sesión.');
            setTimeout(() => {
                router.push('/login');
            }, 2000);

        } 
        // Opción B: Es DE PAGO -> Transbank
        else {
            sessionStorage.setItem('pendingRegistrationData', JSON.stringify(form));
            
            const response = await fetch('http://127.0.0.1:5000/api/create-transaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    buy_order: `bo_invex_${Date.now()}`,
                    session_id: `sid_invex_${Date.now()}`,
                    amount: selectedPlanPrice.value,
                    return_url: 'http://localhost:8080/pago/confirmacion' 
                }),
            });
            
            const data = await response.json();
            
            if (response.ok && data.url_redirect) {
                window.location.href = data.url_redirect;
            } else {
                throw new Error(data.error || 'Error iniciando pago');
            }
        }
    } catch (error) {
        console.error('Error detallado:', error);
        openModal('❌ Error de Registro', `Detalle: ${error.message}`);
    } finally {
        if (!window.location.href.includes('webpay')) {
             isLoading.value = false;
        }
    }
};
</script>

<style scoped>
/* GENERAL */
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
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* PROGRESS BAR */
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

#progressbar li:first-child:after { content: none; }
#progressbar li.active { color: #0f766e; }
#progressbar li.active:before { background: linear-gradient(135deg, #0f766e, #0d9488); color: #fff; }
#progressbar li.active + li:after { background: #0f766e; }

/* FORM ELEMENTS */
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

.password-container { position: relative; }
.toggle-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  user-select: none;
}

/* BUTTONS */
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

.action-button.secondary { background: #e5e7eb; color: #374151; }
.action-button:disabled { background: #9ca3af; cursor: not-allowed; }
.submit { width: 100%; background: linear-gradient(135deg, #0f766e, #0d9488); }

/* PLAN CARDS */
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

/* CONFIRM & PAYMENT */
.confirm-card {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 16px;
  text-align: left;
  font-size: 1rem;
  line-height: 1.6;
}

.payment-summary {
  text-align: center;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 10px;
}

.redirect-message {
  margin-top: 1rem;
  font-style: italic;
  color: #6b7280;
}

.total-amount {
  font-size: 1.25rem;
  color: #0f766e;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-box {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.modal-box h2 {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.modal-box p {
  font-size: 1rem;
  color: #374151;
  margin-bottom: 1.5rem;
  white-space: pre-line;
}

.modal-box button {
  padding: 0.6rem 1.2rem;
  background: #2563eb;
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