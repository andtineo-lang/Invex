<template>
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
</template>

<style scoped>
.footer {
  background: #111827;
  color: white;
  padding: 2.5rem 2rem 1.5rem;
  margin-top: auto;
}
.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}
.footer-section h3,
.footer-section h4 {
  margin-bottom: 1rem;
  font-weight: 700;
  color: #10b981;
}
.footer-bottom {
  border-top: 1px solid #374151;
  padding-top: 1rem;
  text-align: center;
  color: #9ca3af;
  font-size: 0.9rem;
}
</style>
