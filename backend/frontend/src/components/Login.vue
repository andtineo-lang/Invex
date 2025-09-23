<template>
  <div>
    <Header /> <!-- Menú global -->
    <form id="msform" @submit.prevent="handleLogin">
      <!-- SIN progressbar -->

      <!-- login -->
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

        <!-- opcion de crear cuentas si es que no tines una -->
        <p class="fs-subtitle">
          ¿No tienes cuenta? 
          <router-link to="/registro">Crear cuenta</router-link>
        </p>
      </fieldset>
    </form>
  </div>
</template>



<script setup>
import Header from '@/components/Header.vue'
import { reactive } from 'vue'

const loginForm = reactive({
  email: '',
  password: ''
})

const handleLogin = () => {
  if (!loginForm.email || !loginForm.password) {
    alert('Por favor completa todos los campos')
    return
  }

  // Aquí conectarías con tu API de login (ejemplo con fetch o axios)
  console.log('Iniciando sesión con:', loginForm)

  alert(`Bienvenido ${loginForm.email}`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Inter:400,600,700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', sans-serif;
  background: #f9fafb;
  color: #1f2937;
}

#msform {
  width: 450px;
  margin: 50px auto;
  text-align: center;
  position: relative;
}

#msform fieldset {
  background: #fff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  padding: 30px 40px;
  width: 100%;
}

#msform input {
  padding: 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 15px;
  width: 100%;
  font-size: 14px;
  transition: border 0.3s, box-shadow 0.3s;
}
#msform input:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2);
  outline: none;
}

.action-button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 12px 20px;
  margin: 10px 5px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(15,118,110,0.3);
}
.submit {
  width: 100%;
  background: linear-gradient(135deg, #0f766e, #0d9488);
}

.fs-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #0f766e;
}
.fs-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
  margin-top: 15px;
}
</style>
