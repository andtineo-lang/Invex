<template>
  <div class="confirm-container">
    <!-- Estado de Carga -->
    <div v-if="loading" class="spinner-container">
      <div class="spinner"></div>
      <p>Confirmando tu pago, por favor espera...</p>
    </div>

    <!-- Resultados del Pago -->
    <div v-if="!loading && paymentResult" class="result-card">
      
      <!-- Caso: PAGO APROBADO -->
      <template v-if="paymentResult.status === 'AUTHORIZED'">
        <div class="icon success">✔</div>
        <h2 class="success-text">¡Pago Aprobado!</h2>
        <div class="details">
          <p><strong>Monto:</strong> ${{ formatAmount(paymentResult.amount) }}</p>
          <p><strong>Orden de Compra:</strong> {{ paymentResult.buy_order }}</p>
          <p><strong>Fecha de Transacción:</strong> {{ formatDate(paymentResult.transaction_date) }}</p>
          <p><strong>Últimos 4 dígitos:</strong> **** {{ paymentResult.card_detail.card_number }}</p>
        </div>
        <!-- CORREGIDO: La ruta al inventario es anidada, la ruta completa es /app/inventario -->
        <router-link to="/app/inventario">
          <button class="action-button">Ir al Dashboard</button>
        </router-link>
      </template>

      <!-- Caso: PAGO CANCELADO -->
      <template v-else-if="paymentResult.status === 'CANCELLED'">
        <div class="icon warning">!</div>
        <h2 class="warning-text">Pago Cancelado</h2>
        <p class="message">Has cancelado el proceso de pago. Puedes volver a intentarlo cuando quieras.</p>
        <router-link to="/registro">
          <button class="action-button secondary">Volver al Registro</button>
        </router-link>
      </template>

      <!-- Caso: PAGO RECHAZADO O ERROR -->
      <template v-else>
        <div class="icon error">✖</div>
        <h2 class="error-text">Pago Rechazado</h2>
          <div class="details">
          <p><strong>Monto:</strong> ${{ formatAmount(paymentResult.amount) }}</p>
          <p><strong>Orden de Compra:</strong> {{ paymentResult.buy_order }}</p>
          <p><strong>Respuesta:</strong> {{ paymentResult.response_code === -1 ? 'Rechazado por el banco' : 'Transacción fallida' }}</p>
        </div>
        <router-link to="/registro">
           <button class="action-button secondary">Intentar Nuevamente</button>
        </router-link>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const loading = ref(true);
const paymentResult = ref(null);

const confirmPayment = async (token) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/confirm-transaction', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token }),
    });

    if (!response.ok) {
      throw new Error('Error al conectar con el servidor para confirmar.');
    }

    const data = await response.json();
    paymentResult.value = data;

  } catch (error) {
    console.error('Error:', error);
    paymentResult.value = { status: 'ERROR', message: error.message };
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const token = route.query.token_ws;

  // Si hay un token, se intenta confirmar el pago.
  if (token) {
    confirmPayment(token);
  } else {
    // Si NO hay token, significa que el usuario canceló.
    console.log("Pago cancelado por el usuario.");
    loading.value = false;
    paymentResult.value = { status: 'CANCELLED' };
  }
});

// --- Funciones de formato ---
const formatAmount = (amount) => {
  return new Intl.NumberFormat('es-CL').format(amount);
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('es-CL');
};
</script>

<style scoped>
.confirm-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f0fdfa;
  padding: 2rem;
}

.spinner-container {
  text-align: center;
  color: #374151;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border-left-color: #0f766e;
  animation: spin 1s ease infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.result-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 450px;
  width: 100%;
}

.icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  color: white;
}

.icon.success { background-color: #10b981; }
.icon.error { background-color: #ef4444; }
.icon.warning { background-color: #f59e0b; }

.success-text { color: #10b981; }
.error-text { color: #ef4444; }
.warning-text { color: #f59e0b; }

h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.details {
  text-align: left;
  margin-bottom: 2rem;
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.details p {
  margin-bottom: 0.75rem;
  color: #374151;
  line-height: 1.5;
}
.details p:last-child {
  margin-bottom: 0;
}

.message {
  color: #374151;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  text-decoration: none;
  font-size: 1rem;
}
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}

.action-button.secondary {
  background-color: #6b7280;
}
.action-button.secondary:hover {
   box-shadow: 0 6px 15px rgba(107,114,128,0.3);
}
</style>
