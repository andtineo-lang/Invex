<template>
  <div class="confirm-container">
    <div v-if="loading" class="card">
      <div class="spinner"></div>
      <h2>Verificando tu pago...</h2>
      <p>Estamos confirmando la transacción con el banco.</p>
    </div>

    <div v-else-if="success" class="card success">
      <div class="icon">🎉</div>
      <h2>¡Felicidades!</h2>
      <p>Tu cuenta ha sido actualizada al <strong>Plan PRO</strong>.</p>
      <button @click="irAlInventario">Ir a mi Inventario</button>
    </div>

    <div v-else class="card error">
      <div class="icon">❌</div>
      <h2>Hubo un problema</h2>
      <p>{{ errorMsg }}</p>
      <button @click="volverAPrecios">Intentar de nuevo</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import axiosInstance from '@/api/axios';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const loading = ref(true);
const success = ref(false);
const errorMsg = ref('');

onMounted(async () => {
  const token_ws = route.query.token_ws;
  const tb_token = route.query.TB_token; // A veces Transbank lo envía así si se anula

  // 1. Validar que venga un token del banco
  if (!token_ws && !tb_token) {
    errorMsg.value = "No se recibió confirmación del banco (Token faltante).";
    loading.value = false;
    return;
  }

  if (tb_token) {
     errorMsg.value = "La transacción fue anulada por el usuario.";
     loading.value = false;
     return;
  }

  try {
    // 2. Avisar al Backend que finalice el Upgrade
    // IMPORTANTE: En un entorno real de producción, aquí deberías enviar 
    // el 'token_ws' al backend para que Django haga el 'transaction.commit()'
    await axiosInstance.post('/users/upgrade-plan/', {
        token: token_ws 
    });

    // 3. Actualizar la información del usuario en el Frontend (Store)
    // Para que el menú lateral muestre "Plan PRO" inmediatamente
    await authStore.fetchUser();
    
    success.value = true;

  } catch (error) {
    console.error("Error en upgrade:", error);
    errorMsg.value = "Tu pago pudo haber sido procesado, pero hubo un error al actualizar tu perfil. Contacta a soporte.";
  } finally {
    loading.value = false;
  }
});

const irAlInventario = () => router.push('/dashboard/inventario');
const volverAPrecios = () => router.push('/precios');
</script>

<style scoped>
.confirm-container { display: flex; justify-content: center; align-items: center; height: 100vh; background: #f8fafc; }
.card { background: white; padding: 3rem; border-radius: 1rem; text-align: center; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); max-width: 450px; width: 90%; }
.icon { font-size: 4rem; margin-bottom: 1rem; }
h2 { color: #1e293b; margin-bottom: 0.5rem; font-weight: 700; }
p { color: #64748b; margin-bottom: 2rem; }
button { background: #0f766e; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 0.5rem; cursor: pointer; font-weight: 600; font-size: 1rem; transition: background 0.2s; }
button:hover { background: #0d9488; }
.spinner { margin: 0 auto 1.5rem; width: 50px; height: 50px; border: 4px solid #e2e8f0; border-top-color: #0f766e; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.error .icon { filter: grayscale(1) hue-rotate(320deg); } /* Tono rojo */
</style>