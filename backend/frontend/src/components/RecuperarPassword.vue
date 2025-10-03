<template>
  <div class="invex-landing">
    <!-- Header -->
    <Header />

    <!-- Main -->
    <main class="main-content">
      <div class="recover-container">
        <!-- Columna izquierda (branding) -->
        <div class="recover-left">
          <h2>🔑 Recupera tu acceso</h2>
          <p>No te preocupes, todos olvidamos contraseñas.</p>
          <ul class="benefits">
            <li>📩 Te enviaremos un correo seguro</li>
            <li>🔒 Podrás crear una nueva contraseña</li>
            <li>⚡ Acceso rápido y protegido</li>
          </ul>
        </div>

        <!-- Columna derecha (formulario) -->
        <div class="recover-right">
          <form @submit.prevent="handleRecover">
            <fieldset>
              <h2 class="fs-title">Recuperar Contraseña</h2>
              <p class="fs-subtitle">Ingresa tu correo electrónico y recibirás un enlace.</p>

              <input 
                type="email" 
                v-model="email" 
                placeholder="Correo electrónico" 
                required
              />
              <button type="submit" class="action-button">Enviar correo</button>

              <p class="fs-subtitle">
                ¿Recordaste tu contraseña? 
                <router-link to="/login">Inicia sesión</router-link>
              </p>
            </fieldset>
          </form>
        </div>
      </div>
    </main>

    <!-- Modal -->
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
import { ref } from 'vue'

const email = ref('')

// Modal
const showModal = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')

const openModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

const handleRecover = () => {
  if (!email.value) {
    openModal("⚠️ Campo vacío", "Por favor ingresa tu correo electrónico")
    return
  }
  openModal("✅ Correo enviado", `Hemos enviado un enlace de recuperación a ${email.value}`)
}
</script>

<style scoped>
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

.recover-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  overflow: hidden;
}

/* Columna izquierda */
.recover-left {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.recover-left h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}
.recover-left p {
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
  transition: transform 0.2s ease, color 0.2s ease;
}
.benefits li:hover {
  transform: translateX(5px);
  color: #facc15;
}

/* Columna derecha */
.recover-right {
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}
.recover-right form {
  width: 100%;
  max-width: 400px;
}
.recover-right input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 14px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.recover-right input:focus {
  border-color: #0f766e;
  outline: none;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 20px;
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
  margin-bottom: 10px;
  color: #0f766e;
}
.fs-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 15px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.modal-box {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  text-align: center;
}
</style>
