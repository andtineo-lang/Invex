<template>
  <form id="msform" @submit.prevent="handleSubmit">
    <!-- Progressbar -->
    <ul id="progressbar">
      <li :class="{ active: step >= 1 }">Cuenta</li>
      <li :class="{ active: step >= 2 }">Empresa</li>
      <li :class="{ active: step >= 3 }">Confirmación</li>
    </ul>

    <!-- Step 1 -->
    <fieldset v-if="step === 1">
      <h2 class="fs-title">Crear tu cuenta</h2>
      <h3 class="fs-subtitle">Paso 1</h3>
      <input type="email" v-model="form.email" placeholder="Correo electrónico" required />
      <input type="password" v-model="form.password" placeholder="Contraseña" required />
      <input type="password" v-model="form.confirmPassword" placeholder="Confirmar contraseña" required />
      <button type="button" class="action-button" @click="nextStep">Siguiente</button>
    </fieldset>

    <!-- Step 2 -->
    <fieldset v-if="step === 2">
      <h2 class="fs-title">Datos de la Empresa</h2>
      <h3 class="fs-subtitle">Paso 2</h3>
      <input type="text" v-model="form.company" placeholder="Nombre de la empresa" required />
      <input type="text" v-model="form.industry" placeholder="Industria (ej: Retail, Alimentos...)" />
      <select v-model="form.plan" required>
        <option value="">Selecciona un plan</option>
        <option value="mensual">Mensual - $29</option>
        <option value="semestral">Semestral - $149</option>
        <option value="anual">Anual - $299</option>
      </select>
      <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
      <button type="button" class="action-button" @click="nextStep">Siguiente</button>
    </fieldset>

    <!-- Step 3 -->
    <fieldset v-if="step === 3">
      <h2 class="fs-title">Confirmación</h2>
      <h3 class="fs-subtitle">Revisa tus datos</h3>
      <p><strong>Correo:</strong> {{ form.email }}</p>
      <p><strong>Empresa:</strong> {{ form.company }}</p>
      <p><strong>Plan:</strong> {{ form.plan }}</p>
      <button type="button" class="action-button secondary" @click="prevStep">Atrás</button>
      <button type="submit" class="action-button submit">Crear Cuenta</button>
    </fieldset>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const step = ref(1)

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  company: '',
  industry: '',
  plan: ''
})

const nextStep = () => {
  if (step.value < 3) step.value++
}

const prevStep = () => {
  if (step.value > 1) step.value--
}

const handleSubmit = () => {
  if (form.password !== form.confirmPassword) {
    alert('Las contraseñas no coinciden')
    return
  }
  console.log('Formulario enviado:', form)
  alert('🎉 Cuenta creada con éxito')
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Inter:400,600,700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', sans-serif;
  background: #f9fafb;
  color: #1f2937;
}

/* Form container */
#msform {
  width: 450px;
  margin: 50px auto;
  text-align: center;
  position: relative;
}

/* Steps */
#msform fieldset {
  background: #fff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  padding: 30px 40px;
  width: 100%;
  position: relative;
}
#msform fieldset:not(:first-of-type) {
  display: none;
}

/* Inputs */
#msform input, #msform select, #msform textarea {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 14px;
  transition: border 0.3s, box-shadow 0.3s;
}
#msform input:focus, #msform select:focus, #msform textarea:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2);
  outline: none;
}

/* Buttons */
.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 20px;
  margin: 10px 5px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}
.action-button.secondary {
  background: #d1d5db;
  color: #374151;
}
.submit {
  width: 100%;
  background: linear-gradient(135deg, #0f766e, #0d9488);
}

/* Titles */
.fs-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #0f766e;
}
.fs-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 20px;
}

/* Progressbar */
#progressbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  counter-reset: step;
}
#progressbar li {
  list-style: none;
  text-transform: uppercase;
  font-size: 0.7rem;
  flex: 1;
  position: relative;
  color: #9ca3af;
}
#progressbar li:before {
  content: counter(step);
  counter-increment: step;
  width: 28px;
  height: 28px;
  line-height: 28px;
  display: block;
  margin: 0 auto 8px auto;
  border-radius: 50%;
  background: #e5e7eb;
  color: #374151;
  font-weight: bold;
}
#progressbar li:after {
  content: '';
  position: absolute;
  width: 100%;
  height: 3px;
  background: #e5e7eb;
  top: 12px;
  left: -50%;
  z-index: -1;
}
#progressbar li:first-child:after { content: none; }

/* Active step */
#progressbar li.active {
  color: #0f766e;
}
#progressbar li.active:before {
  background: #0f766e;
  color: white;
}
#progressbar li.active + li:after {
  background: #0f766e;
}
</style>
