<template> 
  <div class="invex-landing">
    <!-- Header -->
    <Header />

    <!-- Main -->
    <main class="main-content">
      <div class="login-container">
        <!-- Columna izquierda con branding -->
        <div class="login-left">
          <h2>🚀 Bienvenido a INVEX</h2>
          <p>La forma más inteligente de gestionar tu inventario.</p>
          <ul class="benefits">
            <li>📊 Predicciones de demanda en tiempo real</li>
            <li>⚡ Automatización de reabastecimiento</li>
            <li>📈 Optimización de costos y stock</li>
          </ul>
        </div>

        <!-- Columna derecha con formulario -->
        <div class="login-right">
          <form id="msform" @submit.prevent="handleLogin">
            <fieldset>
              <h2 class="fs-title">Inicia Sesión</h2>

              <input 
                type="email" 
                v-model="loginForm.email" 
                placeholder="Correo electrónico" 
                required 
              />

              <!--campo Empresa -->
              <input 
                type="text" 
                v-model="loginForm.empresa" 
                placeholder="Empresa" 
                required 
              />

              <!-- Campo contraseña con icono -->
              <div class="password-container">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  v-model="loginForm.password" 
                  placeholder="Contraseña" 
                  required 
                />
                <span 
                  class="toggle-password" 
                  @click="showPassword = !showPassword"
                  :title="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                >
                  {{ showPassword ? '🙈' : '👁️' }}
                </span>
              </div>

              <button type="submit" class="action-button submit">Ingresar</button>
              <p class="fs-subtitle">
                ¿No tienes cuenta? 
                <router-link to="/registro">Crear cuenta</router-link>
                ¿Olvidaste tu contraseña?
                <router-link to="/recuperar-password">Recupérala aquí</router-link>
              </p>
            </fieldset>
          </form>
        </div>
      </div>
    </main>

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
import { reactive, ref } from 'vue'

const loginForm = reactive({
  email: '',
  empresa: '', 
  password: ''
})

// 👁️ Control para mostrar/ocultar la contraseña
const showPassword = ref(false)

// Modal
const showModal = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')

const openModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

const validarPassword = (password) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$/
  return regex.test(password)
}

const handleLogin = () => {
  if (!loginForm.email || !loginForm.password || !loginForm.empresa) {
    openModal('⚠️ Campos incompletos', 'Por favor completa todos los campos')
    return
  }

  if (!validarPassword(loginForm.password)) {
    openModal('🔐 Contraseña inválida', 'Debe tener mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula y 1 carácter especial.')
    return
  }

  openModal('✅ Bienvenido', `Inicio de sesión correcto para ${loginForm.email} en la empresa ${loginForm.empresa}`)
}
</script>

<style scoped>
/* 🔹 Mantengo todos tus estilos originales */
.invex-landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0fdfa, #ecfdf5);
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* Columna izquierda */
.login-left {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-left h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.login-left p {
  margin-bottom: 2rem;
  font-size: 1rem;
  opacity: 0.9;
}

.benefits {
  list-style: none;
  padding: 0;
}

.benefits li {
  margin-bottom: 1rem;
  font-size: 1rem;
}

/* Columna derecha */
.login-right {
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

#msform {
  width: 100%;
  max-width: 400px;
}

#msform input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

#msform input:focus {
  border-color: #0f766e;
  outline: none;
}

/* 👁️ Estilo para el icono de ver contraseña */
.password-container {
  position: relative;
}

.password-container input {
  padding-right: 40px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 1.1rem;
  color: #6b7280;
  user-select: none;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #0f766e;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 20px;
  margin: 10px 0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 100%;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}

.fs-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #0f766e;
}

.fs-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 15px;
}

#msform fieldset {
  border: none !important; 
}

/* ✅ Modal */
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
