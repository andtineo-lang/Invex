<template>
  <div class="invex-landing">
    <!-- Header -->
    <Header />

    <!-- Main -->
    <main class="main-content">
      <div class="login-container">
        <!-- Columna izquierda con branding -->
        <div class="login-left">
          <h2>🚀 Bienvenido a INVEX</h2>
          <p>La forma más inteligente de gestionar tu inventario.</p>
          <ul class="benefits">
            <li>📊 Predicciones de demanda en tiempo real</li>
            <li>⚡ Automatización de reabastecimiento</li>
            <li>📈 Optimización de costos y stock</li>
          </ul>
        </div>

        <!-- Columna derecha con formulario -->
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
                type="password" 
                v-model="loginForm.password" 
                placeholder="Contraseña" 
                required 
              />
              <button type="submit" class="action-button submit">Ingresar</button>
              <p class="fs-subtitle">
                ¿No tienes cuenta? 
                <router-link to="/registro">Crear cuenta</router-link>
              </p>
            </fieldset>
          </form>
        </div>
      </div>
    </main>

   
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { reactive } from 'vue'

const loginForm = reactive({
  email: '',
  password: ''
})

const validarPassword = (password) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$/
  return regex.test(password)
}

const handleLogin = () => {
  if (!loginForm.email || !loginForm.password) {
    alert('Por favor completa todos los campos')
    return
  }

  if (!validarPassword(loginForm.password)) {
    alert('La contraseña debe tener mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula y 1 carácter especial.')
    return
  }

  console.log('Iniciando sesión con:', loginForm)
  alert(`Bienvenido ${loginForm.email}`)
}
</script>

<style scoped>
.invex-landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0fdfa, #ecfdf5); /* Fondo elegante */
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); /* más leve */
  overflow: hidden;
}

/* Columna izquierda */
.login-left {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-left h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.login-left p {
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
}

/* Columna derecha */
.login-right {
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

#msform {
  width: 100%;
  max-width: 400px;
}

#msform input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); /* más leve */
}

#msform input:focus {
  border-color: #0f766e;
box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); /* más leve */
  outline: none;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 20px;
  margin: 10px 0;
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
  margin-bottom: 20px;
  color: #0f766e;
}

.fs-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 15px;
}



/* eliminación de el borde gris feo */
#msform fieldset {
  border: none !important; 
}


/* Responsive */
@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  .login-left {
    display: none; /* Ocultar branding en móvil */
  }
}

.login-container {
  animation: fadeInUp 0.8s ease-in-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.benefits li {
  transition: transform 0.2s ease, color 0.2s ease;
}
.benefits li:hover {
  transform: translateX(5px);
  color: #facc15; /* amarillo elegante */
}

#msform {
 box-shadow: none !important; /* elimina la sombra */
  background: transparent !important; /* asegura que no quede fondo */
}



</style>
