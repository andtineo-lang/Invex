<template>
  <div id="app">
    <!-- Header (menú siempre visible) -->
    <header class="header">
      <div class="container">
        <div class="nav-content">
          <div class="logo">
            <!-- Logo siempre va al Home -->
            <router-link to="/" class="logo-link">
              <h1>INVEX</h1>
            </router-link>
          </div>
          <div class="nav-buttons">
            <button class="btn-secondary">Iniciar Sesión</button>
            <router-link to="/registro">
              <button class="btn-primary">Crear Cuenta</button>
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Aquí se cargan las vistas -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
/* Header fijo */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e5e7eb;
  z-index: 1000;
  padding: 1rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  text-decoration: none;
  color: inherit;
}

.logo-link h1 {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f766e;
  letter-spacing: -0.02em;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

/* Botones */
.btn-primary {
  background: linear-gradient(135deg, #0f766e, #0d9488);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(15, 118, 110, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #374151;
  border: 2px solid #d1d5db;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  border-color: #0f766e;
  color: #0f766e;
}

/* Para que el contenido no se tape con el header */
#app {
  padding-top: 80px;
}
</style>
