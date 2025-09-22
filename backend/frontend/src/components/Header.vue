<template>
  <header class="header">
    <div class="container">
      <div class="nav-content">
        <div class="logo">
          <router-link to="/" class="logo-link">
            <h1>INVEX</h1>
          </router-link>
        </div>
        <div class="nav-buttons">
          <router-link to="/login">
            <button class="btn-secondary">Iniciar Sesión</button>
          </router-link>
          <router-link to="/registro">
            <button class="btn-primary">Crear Cuenta</button>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
// No necesitas lógica especial aquí, solo se reutiliza el header.
</script>

<style scoped>
.logo-link {
  text-decoration: none;
}
</style>
