<template>
  <div class="invex-landing">
    <!-- Header -->
    <Header />

    <!-- Main -->
    <main class="main-content">
      <div class="recover-card">
        <!-- Lado izquierdo (branding con íconos grandes) -->
        <div class="recover-left">
          <h2>🔑 Recupera tu acceso</h2>
          <p>No te preocupes, a todos nos pasa 😅</p>
          <ul class="benefits">
            <li>📩 Recibirás un correo seguro</li>
            <li>🔒 Podrás crear una nueva contraseña</li>
            <li>⚡ Acceso rápido y protegido</li>
          </ul>
        </div>

        <!-- Lado derecho (formulario más elegante) -->
        <div class="recover-right">
          <form @submit.prevent="handleRecover" class="form-box">
            <h2 class="fs-title">Recuperar Contraseña</h2>
            <p class="fs-subtitle">Ingresa tu correo electrónico y te enviaremos un enlace.</p>

            <input 
              type="email" 
              v-model="email" 
              placeholder="Correo electrónico" 
              required
            />
            <button type="submit" class="action-button">Enviar correo</button>

            <p class="fs-subtitle">
              ¿Recordaste tu contraseña?  
              <router-link to="/login" class="link">Inicia sesión</router-link>
            </p>
          </form>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-box">
        <h2>{{ modalTitle }}</h2>
        <p>{{ modalMessage }}</p>
        <button @click="showModal = false" class="close-btn">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { ref } from 'vue'

const email = ref('')
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
  padding: 2rem;
}

/* Card principal */
.recover-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 950px;
  width: 100%;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  overflow: hidden;
  animation: fadeIn 0.6s ease;
}

/* Lado izquierdo */
.recover-left {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.recover-left h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}
.recover-left p {
  margin-bottom: 2rem;
  font-size: 1.1rem;
  opacity: 0.95;
}
.benefits li {
  margin-bottom: 1rem;
  font-size: 1rem;
  transition: transform 0.2s ease;
}
.benefits li:hover {
  transform: translateX(6px);
  color: #facc15;
}

/* Lado derecho */
.recover-right {
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}
.form-box {
  width: 100%;
  max-width: 380px;
}
.fs-title {
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #0f766e;
}
.fs-subtitle {
  font-size: 0.95rem;
  color: #6b7280;
  margin: 10px 0 20px;
}
.link {
  color: #0d9488;
  font-weight: 600;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}

/* Inputs */
.recover-right input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 15px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.recover-right input:focus {
  border-color: #0d9488;
  outline: none;
  box-shadow: 0 0 0 3px rgba(13,148,136,0.2);
}

/* Botón */
.action-button {
  background: #0d9488;
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 100%;
}
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(13,148,136,0.3);
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
  border-radius: 16px;
  padding: 2rem;
  max-width: 420px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.close-btn {
  margin-top: 1rem;
  background: #0d9488;
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}
.close-btn:hover {
  background: #0f766e;
}

/* Animación */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
