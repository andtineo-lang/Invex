<template>
  <div class="confirmation-container">
    <!-- Estado de Carga -->
    <div v-if="isLoading" class="status-card loading">
      <div class="spinner"></div>
      <h2>Confirmando tu pago, por favor espera...</h2>
      <p>Estamos verificando la transacción con Transbank.</p>
    </div>

    <!-- Pago Aprobado -->
    <div v-else-if="paymentResult.status === 'AUTHORIZED'" class="status-card success">
      <div class="icon">✔️</div>
      <h2>¡Pago Aprobado!</h2>
      <p>Tu suscripción ha sido activada correctamente. ¡Bienvenido a Invex!</p>
      <div class="details">
        <p><strong>Monto Pagado:</strong> ${{ paymentResult.amount }}</p>
        <p><strong>Orden de Compra:</strong> {{ paymentResult.buy_order }}</p>
        <p><strong>Últimos 4 dígitos:</strong> {{ paymentResult.card_detail.card_number }}</p>
      </div>
      <!-- ✅ Botón corregido -->
      <button @click="goToDashboard" class="action-button">Ir a mi Inventario</button>
    </div>

    <!-- Otros estados (rechazado, cancelado...) -->
    <div v-else class="status-card cancelled">
        <div class="icon">⚠️</div>
        <h2>Proceso Interrumpido</h2>
        <p>El proceso de pago fue cancelado o no se pudo verificar.</p>
        <button @click="goToRegister" class="action-button">Volver al Registro</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isLoading = ref(true);
const paymentResult = reactive({});

onMounted(async () => {
  const token = route.query.token_ws;
  if (!token) {
    isLoading.value = false;
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/confirm-transaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    });
    const data = await response.json();
    Object.assign(paymentResult, data);

    // ✅ LÓGICA AÑADIDA: Si el pago es exitoso, crea el token de sesión.
    if (data.status === 'AUTHORIZED') {
      localStorage.setItem('authToken', 'fake-jwt-token-after-payment');
      localStorage.setItem('userRole', 'admin'); // Asignar un rol por defecto
    }

  } catch (error) {
    console.error('Error en la confirmación:', error);
    Object.assign(paymentResult, { status: 'ERROR_APP' });
  } finally {
    isLoading.value = false;
  }
});

// ✅ FUNCIÓN CORREGIDA: Redirige a la ruta correcta del dashboard.
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

