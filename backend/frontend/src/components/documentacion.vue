<template>
  <div class="invex-page">
    <Header />
    <section class="page-section">
      <div class="container">
        <div class="section-header">
          <h2>Documentación de INVEX</h2>
          <p>Aprende cómo usar e integrar nuestra plataforma fácilmente</p>
        </div>

        <div class="docs-content">
          <div class="doc-section">
            <h3>Introducción</h3>
            <p>INVEX ofrece una API REST que permite integrar la gestión de inventario con tus sistemas ERP o e-commerce.</p>
          </div>

          <div class="doc-section">
            <h3>Autenticación</h3>
            <pre><code>POST /api/login
{
  "usuario": "tu_email",
  "contraseña": "tu_password"
}</code></pre>
          </div>

          <div class="doc-section">
            <h3>Consultar Inventario</h3>
            <pre><code>GET /api/inventario
Headers: Authorization: Bearer token</code></pre>
          </div>

          <div class="doc-section">
            <h3>Agregar Nuevo Producto</h3>
            <pre><code>POST /api/productos
{
  "nombre": "Producto A",
  "stock": 50
}</code></pre>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import gsap from 'gsap'
import { onMounted } from 'vue'

onMounted(() => {
  gsap.from('.doc-section', { opacity: 0, y: 30, stagger: 0.2 })
})
</script>

<style scoped>
.page-section { padding: 6rem 1rem; }
.docs-content {
  background: #fff;
  padding: 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.doc-section { margin-bottom: 2rem; }
pre {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.75rem;
  overflow-x: auto;
}
code { font-family: 'Courier New', monospace; }
</style>
