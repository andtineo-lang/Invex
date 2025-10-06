<template>
  <div class="invex-page">
    <Header />
    <section class="page-section">
      <div class="container contact-container">
        <div class="section-header">
          <h2>Contáctanos</h2>
          <p>¿Tienes dudas? Estamos aquí para ayudarte</p>
        </div>

        <form class="contact-form" @submit.prevent="enviarFormulario">
          <input type="text" v-model="nombre" placeholder="Tu nombre" required />
          <input type="email" v-model="email" placeholder="Tu correo" required />
          <textarea v-model="mensaje" rows="5" placeholder="Tu mensaje" required></textarea>
          <button class="btn-primary btn-full">Enviar Mensaje</button>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import { ref } from 'vue'
import gsap from 'gsap'
import { onMounted } from 'vue'

const nombre = ref('')
const email = ref('')
const mensaje = ref('')

const enviarFormulario = () => {
  alert(`Gracias ${nombre.value}, tu mensaje ha sido enviado correctamente ✅`)
  nombre.value = ''
  email.value = ''
  mensaje.value = ''
}

onMounted(() => {
  gsap.from('.contact-form input, .contact-form textarea', { opacity: 0, y: 30, stagger: 0.1 })
})
</script>

<style scoped>
.page-section { padding: 6rem 1rem; }
.contact-container {
  max-width: 600px;
  margin: auto;
}
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
input, textarea {
  border: 1px solid #d1d5db;
  padding: 0.8rem 1rem;
  border-radius: 0.75rem;
  font-size: 1rem;
}
input:focus, textarea:focus {
  outline: none;
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2);
}
</style>
