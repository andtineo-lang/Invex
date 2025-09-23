<template> 
  <div>
    <Header /> <!-- Menú global -->

    <!-- Formulario de login -->
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

    <!-- 🔽 Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>INVEX</h3>
          <p>Gestión inteligente de inventarios con IA</p>
        </div>
        <div class="footer-section">
          <h4>Producto</h4>
          <ul>
            <li><router-link to="/caracteristicas">Características</router-link></li>
            <li><router-link to="/precios">Precios</router-link></li>
            <li><router-link to="/demo">Demo</router-link></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>Soporte</h4>
          <ul>
            <li><router-link to="/documentacion">Documentación</router-link></li>
            <li><router-link to="/contacto">Contacto</router-link></li>
            <li><router-link to="/faq">FAQ</router-link></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        © 2025 INVEX. Todos los derechos reservados.
      </div>
    </footer>
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

/* Footer */
.footer {
  background: #1f2937;
  color: white;
  padding: 3rem 0 1rem;
}

.footer-content {
  max-width: 1000px;   /* ancho fijo centrado */
  margin: 0 auto;      /* centra horizontalmente */
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
  text-align: center;  /* centra el contenido */
}

.footer-section h3,
.footer-section h4 {
  margin-bottom: 1rem;
  color: #0f766e;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #d1d5db;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: #0f766e;
}

.footer-bottom {
  border-top: 1px solid #374151;
  padding-top: 1rem;
  text-align: center;
  color: #9ca3af;
}
</style>
