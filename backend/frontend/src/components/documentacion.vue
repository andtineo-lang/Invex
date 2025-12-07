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
            <p>INVEX ofrece una API REST que permite integrar la gestión de inventario con tus sistemas ERP o e-commerce de forma segura y escalable.</p>
          </div>

          <div class="doc-section">
            <h3>Autenticación</h3>
            <p>Para acceder a los recursos privados, necesitas obtener un token JWT.</p>
            <pre><code>POST /api/login
{
  "usuario": "tu_email@empresa.com",
  "contraseña": "tu_password_segura"
}</code></pre>
          </div>

          <div class="doc-section">
            <h3>Consultar Inventario</h3>
            <p>Obtén el listado completo de productos con paginación.</p>
            <pre><code>GET /api/inventario?page=1&amp;limit=20
Headers: 
  Authorization: Bearer &lt;tu_token_aqui&gt;</code></pre>
          </div>

          <div class="doc-section">
            <h3>Agregar Nuevo Producto</h3>
            <p>Registra un nuevo SKU en tu base de datos.</p>
            <pre><code>POST /api/productos
{
  "nombre": "Producto A",
  "sku": "PROD-001",
  "precio": 150.00,
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
  gsap.from('.doc-section', { 
    opacity: 0, 
    y: 20, 
    stagger: 0.2, 
    duration: 0.8,
    ease: "power2.out"
  })
})
</script>

<style scoped>
.page-section { 
    padding: 6rem 1rem; 
}

.container {
    max-width: 900px; /* Ancho optimizado para lectura */
    margin: 0 auto;
    padding: 0 1rem;
}

.section-header {
    text-align: center;
    margin-bottom: 3rem;
}

.section-header h2 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 0.5rem;
}

.docs-content {
  background: #fff;
  padding: 3rem;
  border-radius: 1.5rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  border: 1px solid #f0f0f0;
}

.doc-section { 
    margin-bottom: 3rem; 
}

.doc-section:last-child {
    margin-bottom: 0;
}

.doc-section h3 {
    color: #0f766e;
    margin-bottom: 1rem;
    font-size: 1.5rem;
}

pre {
  background: #1e293b; /* Fondo oscuro para código se ve más pro */
  color: #e2e8f0;
  padding: 1.5rem;
  border-radius: 0.75rem;
  overflow-x: auto;
  font-size: 0.9rem;
  line-height: 1.5;
}

code { 
    font-family: 'Courier New', monospace; 
}
</style>