<template>
  <div class="invex-page">
    <Header />
    
    <section class="pricing-container">
      <div class="text-center max-w-4xl mx-auto mb-10">
      <h1 class="text-3xl font-extrabold text-teal-800 sm:text-4xl">
        Mejora tu Suscripción
      </h1>
      <p class="mt-3 text-lg text-gray-600">
        Pasa al siguiente nivel con <span class="font-bold text-gray-800">INVEX PRO</span>
      </p>
    </div>

      <div class="plans-wrapper">
        <div class="plan-card current">
          <div class="badge">Tu Plan Actual</div>
          <h2>Plan Inicial</h2>
          <div class="price">$0 <span class="period">/mes</span></div>
          <ul class="features">
            <li><span class="check">✓</span> Máximo 50 productos</li>
            <li><span class="check">✓</span> Reportes básicos</li>
            <li><span class="cross">❌</span> Sin Inteligencia Artificial</li>
            <li><span class="cross">❌</span> Sin predicción de demanda</li>
          </ul>
          <button disabled class="btn-disabled">Plan Activo</button>
        </div>

        <div class="plan-card pro featured">
          <div class="popular-badge">Recomendado</div>
          <h2>Plan INVEX PRO</h2>
          <div class="price">$30.000 <span class="period">/mes</span></div>
          <ul class="features">
            <li><span class="check">✓</span> <strong>Productos Ilimitados</strong></li>
            <li><span class="check">✓</span> <strong>IA Estratégica Completa</strong></li>
            <li><span class="check">✓</span> Predicción de demanda</li>
            <li><span class="check">✓</span> Prioridad en soporte</li>
          </ul>
          
          <button 
            @click="iniciarPagoPro" 
            :disabled="isLoading" 
            class="btn-primary btn-upgrade"
          >
            <span v-if="!isLoading">Actualizar a PRO ahora</span>
            <span v-else class="spinner"></span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import { ref } from 'vue';
import axiosInstance from '@/api/axios'; 

const isLoading = ref(false);

const iniciarPagoPro = async () => {
  if (isLoading.value) return;
  isLoading.value = true;

  try {
    const { data } = await axiosInstance.post('/pagos/iniciar-upgrade/');

    if (data.url && data.token) {
        window.location.href = `${data.url}?token_ws=${data.token}`;
    } else {
        alert('Error: La respuesta del banco no contiene los datos de redirección.');
    }

  } catch (error) {
    console.error('Error al iniciar pago:', error);
    alert('Ocurrió un error al conectar con el servicio de pagos.');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.invex-page { min-height: 100vh; background-color: #f8fafc; }
.pricing-container { padding: 4rem 2rem; max-width: 900px; margin: 0 auto; text-align: center; }
.header h1 { color: #0f766e; font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 800; }
.header p { color: #64748b; margin-bottom: 3rem; font-size: 1.1rem; }
.plans-wrapper { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center; }
.plan-card { background: white; border-radius: 1.5rem; padding: 2.5rem 2rem; position: relative; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; text-align: left; height: 100%; display: flex; flex-direction: column;}
.plan-card.pro { border: 2px solid #8b5cf6; box-shadow: 0 20px 25px -5px rgba(139, 92, 246, 0.15); transform: scale(1.05); z-index: 10; }
.badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #e5e7eb; padding: 0.5rem 1.5rem; border-radius: 20px; font-size: 0.9rem; font-weight: 700; color: #374151; }
.popular-badge { background: #8b5cf6; color: #fff; position: absolute; top: -16px; left: 50%; transform: translateX(-50%); padding: 0.5rem 1.5rem; border-radius: 20px; font-size: 0.9rem; font-weight: 700; }
h2 { font-size: 1.5rem; color: #1e293b; margin-bottom: 0.5rem; font-weight: 700; text-align: center; }
.price { font-size: 2.5rem; font-weight: 800; color: #0f766e; margin: 1.5rem 0; display: flex; justify-content: center; align-items: baseline; gap: 5px; }
.period { font-size: 1rem; color: #64748b; font-weight: 400; }
ul.features { list-style: none; padding: 0; margin: 1rem 0 2rem 0; flex-grow: 1; }
ul.features li { margin-bottom: 1rem; color: #4b5563; display: flex; align-items: center; font-size: 0.95rem; }
.check { color: #10b981; margin-right: 12px; font-weight: bold; }
.cross { color: #ef4444; margin-right: 12px; font-weight: bold; }
button { width: 100%; padding: 0.9rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: all 0.2s; font-size: 1rem; margin-top: auto; }
.btn-disabled { background: #f1f5f9; color: #94a3b8; border: 1px solid #e2e8f0; cursor: not-allowed; }
.btn-primary { background-color: #8b5cf6; color: white; border: none; }
.btn-primary:hover { background-color: #7c3aed; transform: translateY(-2px); }
.spinner { display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: white; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) { .plans-wrapper { grid-template-columns: 1fr; } }
</style>