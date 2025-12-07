<template>
  <div class="invex-landing">
    <Header />
    <main class="main-content">
      <div class="contact-container">
        
        <div class="contact-left">
          <h2>💬 Contáctanos</h2>
          <p>Estamos aquí para ayudarte con cualquier duda sobre INVEX.</p>
          <ul class="benefits">
            <li>📞 Respuesta rápida en menos de 24h</li>
            <li>✉️ Atención personalizada</li>
            <li>⚡ Resolución efectiva de problemas</li>
          </ul>
        </div>

        <div class="contact-right">
          <form id="contactForm" @submit.prevent="handleSubmit">
            <fieldset>
              <h2 class="fs-title">Enviar Mensaje</h2>
              
              <input 
                type="text" 
                v-model="form.nombre" 
                placeholder="Tu nombre completo" 
                required 
              />
              
              <input 
                type="email" 
                v-model="form.email" 
                placeholder="Tu correo electrónico" 
                required 
              />
              
              <input 
                type="text" 
                v-model="form.asunto" 
                placeholder="Asunto" 
                required 
              />

              <textarea 
                v-model="form.mensaje" 
                placeholder="Escribe tu mensaje aquí..." 
                rows="4"
                required
              ></textarea>
              
              <button type="submit" class="action-button submit" :disabled="isLoading">
                <span v-if="!isLoading">Enviar</span>
                <span v-else class="spinner"></span>
              </button>
            </fieldset>
          </form>
        </div>
      </div>
    </main>

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

// Estado del formulario
const form = reactive({
  nombre: '',
  email: '',
  asunto: '',
  mensaje: ''
})

const isLoading = ref(false)
const showModal = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')

// Función para abrir modal
const openModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

// Manejo del envío
const handleSubmit = async () => {
  if (!form.nombre || !form.email || !form.asunto || !form.mensaje) {
    openModal('⚠️ Campos incompletos', 'Por favor completa todos los campos.');
    return;
  }

  isLoading.value = true
  
  try {
    // Simulación de envío (Aquí conectarías con tu backend/API)
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Éxito
    openModal('✅ ¡Mensaje Enviado!', 'Hemos recibido tu mensaje correctamente. Te responderemos pronto.')
    
    // Limpiar formulario
    form.nombre = ''
    form.email = ''
    form.asunto = ''
    form.mensaje = ''

  } catch (error) {
    openModal('❌ Error', 'Hubo un problema al enviar el mensaje. Intenta nuevamente.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ESTILOS IDÉNTICOS AL LOGIN 
   (Solo se cambiaron nombres de clases contenedoras para semántica, 
   pero los valores son los mismos)
*/

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

/* Contenedor principal (Igual a .login-container) */
.contact-container { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  max-width: 1000px; 
  width: 100%; 
  background: #fff; 
  border-radius: 16px; 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); 
  overflow: hidden; 
}

/* Lado Izquierdo (Igual a .login-left) */
.contact-left { 
  background: linear-gradient(135deg, #0f766e, #0d9488); 
  color: white; 
  padding: 3rem 2rem; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
}

.contact-left h2 { font-size: 1.8rem; margin-bottom: 1rem; }
.contact-left p { margin-bottom: 2rem; font-size: 1rem; opacity: 0.9; }

.benefits { list-style: none; padding: 0; }
.benefits li { margin-bottom: 1rem; font-size: 1rem; }

/* Lado Derecho (Igual a .login-right) */
.contact-right { 
  padding: 3rem 2rem; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

#contactForm { width: 100%; max-width: 400px; }
#contactForm fieldset { border: none !important; }

/* Inputs y Textarea */
#contactForm input,
#contactForm textarea { 
  padding: 14px; 
  border: 1.5px solid #e5e7eb; 
  border-radius: 8px; 
  margin-bottom: 15px; 
  width: 100%; 
  font-size: 14px; 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); 
  font-family: inherit; /* Para que el textarea herede la fuente */
  box-sizing: border-box; /* Asegura que el padding no rompa el ancho */
}

#contactForm textarea {
  resize: vertical; /* Permite redimensionar solo verticalmente */
  min-height: 100px;
}

#contactForm input:focus,
#contactForm textarea:focus { 
  border-color: #0f766e; 
  outline: none; 
}

/* Botón y Títulos */
.action-button { 
  background: #0f766e; 
  color: white; 
  border: none; 
  padding: 12px 20px; 
  margin: 10px 0; 
  border-radius: 8px; 
  cursor: pointer; 
  font-weight: 600; 
  transition: all 0.2s; 
  width: 100%; 
  min-height: 48px; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.action-button:hover:not(:disabled) { 
  transform: translateY(-2px); 
  box-shadow: 0 6px 15px rgba(15,118,110,0.3); 
}

.action-button:disabled { 
  background-color: #9ca3af; 
  cursor: not-allowed; 
}

.fs-title { 
  font-size: 1.5rem; 
  font-weight: 700; 
  margin-bottom: 20px; 
  color: #0f766e; 
}

/* Spinner */
.spinner { 
  display: inline-block; 
  width: 24px; 
  height: 24px; 
  border: 3px solid rgba(255,255,255,0.3); 
  border-radius: 50%; 
  border-top-color: #fff; 
  animation: spin 1s ease-in-out infinite; 
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Modal */
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

.modal-box h2 { font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; }
.modal-box p { font-size: 1rem; color: #374151; margin-bottom: 1.5rem; white-space: pre-line; }
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
.modal-box button:hover { background: #1d4ed8; }

/* Responsive */
@media (max-width: 768px) {
  .contact-container { grid-template-columns: 1fr; }
  .contact-left { padding: 2rem; }
  .contact-right { padding: 2rem; }
}
</style>