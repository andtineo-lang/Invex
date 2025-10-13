<template>
  <div class="confirmation-container">
    <div v-if="isLoading" class="status-card loading">
      <div class="spinner"></div>
      <h2>Procesando...</h2>
      <p>{{ statusMessage }}</p>
    </div>

    <div v-else-if="paymentResult.status === 'AUTHORIZED'" class="status-card success">
      <div class="icon">✔️</div>
      <h2>¡Cuenta Creada y Activada!</h2>
      <p>Tu suscripción está lista. ¡Bienvenido a Invex!</p>
      <div class="details">
        <p><strong>Monto Pagado:</strong> ${{ paymentResult.amount }}</p>
        <p><strong>Orden de Compra:</strong> {{ paymentResult.buy_order }}</p>
      </div>
      <button @click="goToDashboard" class="action-button">Ir a mi Inventario</button>
    </div>

    <div v-else class="status-card cancelled">
        <div class="icon">⚠️</div>
        <h2>Proceso Interrumpido</h2>
        <p>{{ statusMessage }}</p>
        <button @click="goToRegister" class="action-button">Volver a Intentar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isLoading = ref(true);
const statusMessage = ref('Confirmando tu pago, por favor espera...');
const paymentResult = reactive({});

onMounted(async () => {
  // El token que Transbank añade a la URL de retorno
  const token_ws = route.query.token_ws;

  if (!token_ws) {
    statusMessage.value = 'Token de transacción no encontrado. No se puede verificar el pago.';
    Object.assign(paymentResult, { status: 'CANCELLED' });
    isLoading.value = false;
    return;
  }

  try {
    // ✅ PASO 1: Confirmar el estado de la transacción con el backend
    const confirmResponse = await fetch('http://127.0.0.1:5000/api/confirm-transaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token_ws }),
    });
    
    const paymentData = await confirmResponse.json();
    Object.assign(paymentResult, paymentData);

    if (paymentData.status !== 'AUTHORIZED') {
      throw new Error('El pago fue rechazado o cancelado.');
    }
    
    statusMessage.value = 'Pago confirmado. Creando tu cuenta...';
    
    // ✅ PASO 2: Recuperar los datos de registro guardados
    const pendingData = JSON.parse(sessionStorage.getItem('pendingRegistrationData'));
    if (!pendingData) {
      throw new Error('No se encontraron datos de registro para finalizar la creación de la cuenta.');
    }

    // ✅ PASO 3: Enviar los datos al backend para crear y activar la cuenta
    const registerResponse = await fetch('http://127.0.0.1:8000/api/auth/register-and-activate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            registration: pendingData, // Todos los datos del formulario
            payment: paymentData       // Información del pago exitoso
        })
    });

    if (!registerResponse.ok) {
        const errorData = await registerResponse.json();
        throw new Error(errorData.detail || 'Hubo un problema al crear tu cuenta después del pago.');
    }

    const userData = await registerResponse.json();

    // ✅ PASO 4: Guardar el token REAL y limpiar
    localStorage.setItem('authToken', userData.token); // El token JWT real del backend
    sessionStorage.removeItem('pendingRegistrationData'); // Limpiar datos temporales

  } catch (error) {
    console.error('Error en la confirmación:', error);
    statusMessage.value = error.message;
    Object.assign(paymentResult, { status: 'ERROR_APP' });
  } finally {
    isLoading.value = false;
  }
});

const goToDashboard = () => router.push('/dashboard/inventario');
const goToRegister = () => router.push('/registro');
</script>

<style scoped>
/* Tus estilos existentes... */
.confirmation-container { display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #f9fafb; padding: 2rem; }
.status-card { background: white; padding: 2.5rem 3rem; border-radius: 1rem; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 100%; }
.icon { font-size: 3.5rem; margin-bottom: 1rem; }
.status-card h2 { font-size: 2rem; font-weight: 700; margin-bottom: 0.75rem; }
.success h2 { color: #10b981; }
.cancelled h2 { color: #f59e0b; }
.details { background: #f3f4f6; padding: 1.25rem; margin: 2rem 0; border-radius: 0.75rem; text-align: left; }
.action-button { background-color: #0f766e; color: white; border: none; padding: 0.9rem 2rem; border-radius: 0.5rem; cursor: pointer; font-size: 1rem; margin-top: 1.5rem; }
.spinner { width: 56px; height: 56px; border: 6px solid #e5e7eb; border-top-color: #0f766e; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 2rem; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>

