<template>
  <main class="main-content">
    <div class="login-container">
      <div class="login-left">
        <h2>🔑 Crea tu nueva clave</h2>
        <p>Casi listo. Define una nueva contraseña segura para tu cuenta.</p>
        <ul class="benefits">
          <li>🔒 Mínimo 8 caracteres</li>
          <li>👀 Asegúrate de que coincidan</li>
          <li>🚀 Guarda y vuelve a ingresar</li>
        </ul>
      </div>

      <div class="login-right">
        <form id="msform" @submit.prevent="handleResetPassword" v-if="!successMessage">
          <fieldset>
            <h2 class="fs-title">Establecer nueva contraseña</h2>
            <p class="fs-subtitle" style="text-align: center; margin-bottom: 20px;">
              Por favor, ingresa tu nueva contraseña.
            </p>

            <div class="password-container">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="form.new_password" 
                placeholder="Nueva Contraseña" 
                required 
              />
              <span class="toggle-password" @click="showPassword = !showPassword" :title="showPassword ? 'Ocultar' : 'Mostrar'">
                {{ showPassword ? '🙈' : '👁️' }}
              </span>
            </div>

            <div class="password-container">
              <input 
                :type="showPassword2 ? 'text' : 'password'" 
                v-model="form.confirm_password" 
                placeholder="Confirmar Contraseña" 
                required 
              />
              <span class="toggle-password" @click="showPassword2 = !showPassword2" :title="showPassword2 ? 'Ocultar' : 'Mostrar'">
                {{ showPassword2 ? '🙈' : '👁️' }}
              </span>
            </div>
            
            <button type="submit" class="action-button submit" :disabled="isLoading">
              <span v-if="!isLoading">Guardar nueva contraseña</span>
              <span v-else class="spinner"></span>
            </button>
          </fieldset>
        </form>

        <div v-if="successMessage" class="success-message-box">
          <h2 class="fs-title">✅ ¡Éxito!</h2>
          <p>{{ successMessage }}</p>
          <router-link to="/login" class="action-button submit" style="text-decoration: none; max-width: 200px; display: inline-flex;">
            Ir a Inicio de Sesión
          </router-link>
        </div>
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
</template>
<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router'; // 1. Quitamos 'useRouter' de aquí
import axiosInstance from '@/api/axios.js'; 

// --- Estado del Componente ---
// const router = useRouter(); // <--- 2. ESTA LÍNEA SE BORRA
const route = useRoute();

const form = reactive({
  new_password: '',
  confirm_password: '',
  uidb64: null,
  token: null,
});

const isLoading = ref(false);
const successMessage = ref('');
const showPassword = ref(false);
const showPassword2 = ref(false);

// --- Estado del Modal ---
const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');

const openModal = (title, message) => {
  modalTitle.value = title;
  modalMessage.value = message;
  showModal.value = true;
};

// --- Lógica de Envío ---
const handleResetPassword = async () => {
  // Validaciones locales
  if (!form.new_password || !form.confirm_password) {
    openModal('⚠️ Campos incompletos', 'Por favor, completa ambos campos de contraseña.');
    return;
  }
  if (form.new_password !== form.confirm_password) {
    openModal('⚠️ Error', 'Las contraseñas no coinciden.');
    return;
  }
  if (form.new_password.length < 8) {
    openModal('⚠️ Contraseña corta', 'La contraseña debe tener al menos 8 caracteres.');
    return;
  }

  isLoading.value = true;

  try {
    // Enviamos los datos al backend
    await axiosInstance.post('/auth/reset-password-confirm/', {
      uidb64: form.uidb64,
      token: form.token,
      new_password: form.new_password,
      new_password_confirm: form.confirm_password 
    });

    // Éxito
    successMessage.value = '¡Contraseña actualizada con éxito! Ya puedes iniciar sesión.';

  } catch (error) {
    console.error("❌ Error al confirmar reseteo:", error);
    
    let detail = 'Ocurrió un error inesperado.';
    if (error.response?.data) {
        const data = error.response.data;
        if (data.token) detail = data.token[0];
        else if (data.new_password) detail = data.new_password[0];
        else if (data.detail) detail = data.detail;
        else detail = JSON.stringify(data);
    } else {
        detail = 'El enlace de reseteo no es válido o ha expirado. Por favor, solicita uno nuevo.';
    }

    openModal('❌ Error', detail);
  } finally {
    isLoading.value = false;
  }
};

// --- Carga Inicial ---
onMounted(() => {
  // Leemos los parámetros de la URL usando 'route' (no router)
  form.uidb64 = route.query.uid || route.query.uidb64; 
  form.token = route.query.token;

  if (!form.uidb64 || !form.token) {
    openModal('❌ Enlace Inválido', 'El enlace de recuperación está incompleto o malformado. Revisa tu correo nuevamente.');
  }
});
</script>

<style scoped>
/* Estilos consistentes con tu diseño de Login */
.success-message-box {
  width: 100%; 
  max-width: 400px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.success-message-box p {
  font-size: 1rem;
  color: #374151;
  margin-bottom: 1.5rem;
  white-space: pre-line;
}

.main-content { flex: 1; display: flex; justify-content: center; align-items: center; padding: 3rem 1rem; min-height: 100vh; background: linear-gradient(135deg, #f0fdfa, #ecfdf5); }
.login-container { display: grid; grid-template-columns: 1fr 1fr; max-width: 1000px; width: 100%; background: #fff; border-radius: 16px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); overflow: hidden; }
.login-left { background: linear-gradient(135deg, #0f766e, #0d9488); color: white; padding: 3rem 2rem; display: flex; flex-direction: column; justify-content: center; }
.login-left h2 { font-size: 1.8rem; margin-bottom: 1rem; }
.login-left p { margin-bottom: 2rem; font-size: 1rem; opacity: 0.9; }
.benefits { list-style: none; padding: 0; }
.benefits li { margin-bottom: 1rem; font-size: 1rem; }
.login-right { padding: 3rem 2rem; display: flex; justify-content: center; align-items: center; }

/* Responsive para móviles */
@media (max-width: 768px) {
  .login-container { grid-template-columns: 1fr; }
  .login-left { display: none; }
}

#msform { width: 100%; max-width: 400px; }
#msform input { padding: 14px; border: 1.5px solid #e5e7eb; border-radius: 8px; margin-bottom: 15px; width: 100%; font-size: 14px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); }
#msform input:focus { border-color: #0f766e; outline: none; }
.password-container { position: relative; }
.password-container input { padding-right: 40px; }
.toggle-password { position: absolute; right: 12px; top: 35%; transform: translateY(-50%); cursor: pointer; font-size: 1.1rem; color: #6b7280; user-select: none; transition: color 0.2s ease; }
.toggle-password:hover { color: #0f766e; }
.action-button { background: #0f766e; color: white; border: none; padding: 12px 20px; margin: 10px 0; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.2s; width: 100%; min-height: 48px; display: flex; justify-content: center; align-items: center; }
.action-button:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(15,118,110,0.3); }
.action-button:disabled { background-color: #9ca3af; cursor: not-allowed; }
.fs-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; color: #0f766e; text-align: center; }
.fs-subtitle { font-size: 0.9rem; color: #6b7280; margin-top: 15px; text-align: center; }
#msform fieldset { border: none !important; padding: 0; margin: 0; }

/* Spinner */
.spinner { display: inline-block; width: 24px; height: 24px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s ease-in-out infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.modal-box { background: #fff; border-radius: 12px; padding: 2rem; max-width: 400px; width: 90%; text-align: center; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2); }
.modal-box h2 { font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; color: #dc2626; }
.modal-box p { font-size: 1rem; color: #374151; margin-bottom: 1.5rem; white-space: pre-line; }
.modal-box button { padding: 0.6rem 1.2rem; background: #2563eb; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.3s; }
.modal-box button:hover { background: #1d4ed8; }
</style>