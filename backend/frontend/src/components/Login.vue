<template> 
  <div class="invex-landing">
    <Header />

    <main class="main-content">
      <div class="login-container">
        <div class="login-left">
          <h2>🚀 Bienvenido a INVEX</h2>
          <p>La forma más inteligente de gestionar tu inventario.</p>
          <ul class="benefits">
            <li>📊 Predicciones de demanda en tiempo real</li>
            <li>⚡ Automatización de reabastecimiento</li>
            <li>📈 Optimización de costos y stock</li>
          </ul>
        </div>

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
              <input 
                type="text" 
                v-model="loginForm.empresa" 
                placeholder="Nombre de la Empresa" 
                required 
              />
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

              <button type="submit" class="action-button submit" :disabled="isLoading">
                <span v-if="!isLoading">Ingresar</span>
                <span v-else class="spinner"></span>
              </button>

              <p class="fs-subtitle">
                ¿No tienes cuenta? 
                <router-link to="/registro">Crear cuenta</router-link>
                <br>
                ¿Olvidaste tu contraseña?
                <router-link to="/recuperar-password">Recupérala aquí</router-link>
              </p>
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
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const loginForm = reactive({
  email: '',
  empresa: '', 
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false) // Estado para mostrar el spinner

// Lógica del Modal
const showModal = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')
const openModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

// --- LÓGICA DE LOGIN ACTUALIZADA ---
const handleLogin = async () => {
  if (!loginForm.email || !loginForm.password || !loginForm.empresa) {
    openModal('⚠️ Campos incompletos', 'Por favor completa todos los campos.');
    return;
  }
  
  isLoading.value = true;
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      email: loginForm.email,
      password: loginForm.password,
      empresa: loginForm.empresa
    });

    // Guardamos el token y el rol en el almacenamiento local del navegador
    localStorage.setItem('authToken', response.data.access);
    localStorage.setItem('userRole', response.data.rol);

    // Redirigimos al dashboard principal
    router.push('/dashboard'); 
    
  } catch (error) {
    const detail = error.response?.data?.detail || 'No se pudo conectar con el servidor. Inténtalo más tarde.';
    openModal('❌ Error de Autenticación', detail);
    console.error('Error en el login:', error);
  } finally {
    isLoading.value = false; // Oculta el spinner al terminar
  }
}
</script>

<style scoped>
/* Tus estilos existentes... */
.invex-landing { min-height: 100vh; display: flex; flex-direction: column; background: linear-gradient(135deg, #f0fdfa, #ecfdf5); }
.main-content { flex: 1; display: flex; justify-content: center; align-items: center; padding: 3rem 1rem; }
.login-container { display: grid; grid-template-columns: 1fr 1fr; max-width: 1000px; width: 100%; background: #fff; border-radius: 16px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); overflow: hidden; }
.login-left { background: linear-gradient(135deg, #0f766e, #0d9488); color: white; padding: 3rem 2rem; display: flex; flex-direction: column; justify-content: center; }
.login-left h2 { font-size: 1.8rem; margin-bottom: 1rem; }
.login-left p { margin-bottom: 2rem; font-size: 1rem; opacity: 0.9; }
.benefits { list-style: none; padding: 0; }
.benefits li { margin-bottom: 1rem; font-size: 1rem; }
.login-right { padding: 3rem 2rem; display: flex; justify-content: center; align-items: center; }
#msform { width: 100%; max-width: 400px; }
#msform input { padding: 14px; border: 1.5px solid #e5e7eb; border-radius: 8px; margin-bottom: 15px; width: 100%; font-size: 14px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); }
#msform input:focus { border-color: #0f766e; outline: none; }
.password-container { position: relative; }
.password-container input { padding-right: 40px; }
.toggle-password { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); cursor: pointer; font-size: 1.1rem; color: #6b7280; user-select: none; transition: color 0.2s ease; }
.toggle-password:hover { color: #0f766e; }
.action-button { background: #0f766e; color: white; border: none; padding: 12px 20px; margin: 10px 0; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.2s; width: 100%; min-height: 48px; display: flex; justify-content: center; align-items: center; }
.action-button:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(15,118,110,0.3); }
.action-button:disabled { background-color: #9ca3af; cursor: not-allowed; }
.fs-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; color: #0f766e; }
.fs-subtitle { font-size: 0.9rem; color: #6b7280; margin-top: 15px; }
#msform fieldset { border: none !important; }

/* Spinner */
.spinner { display: inline-block; width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s ease-in-out infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-box { background: #fff; border-radius: 12px; padding: 2rem; max-width: 400px; width: 90%; text-align: center; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2); }
.modal-box h2 { font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; }
.modal-box p { font-size: 1rem; color: #374151; margin-bottom: 1.5rem; white-space: pre-line; }
.modal-box button { padding: 0.6rem 1.2rem; background: #2563eb; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.3s; }
.modal-box button:hover { background: #1d4ed8; }
</style>