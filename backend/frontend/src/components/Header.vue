<template>
  <header class="header">
    <div class="container">
      <div class="nav-content">
        <!-- Logo -->
        <div class="logo">
          <router-link to="/" class="logo-link">
            <h1>INVEX</h1>
          </router-link>
        </div>

        <!-- Menú normal (desktop) -->
        <nav class="nav-links desktop-menu">
          <a @click.prevent="navigateTo('hero')">Inicio</a>
          <a @click.prevent="navigateTo('about')">Sobre Nosotros</a>
          <a @click.prevent="navigateTo('pricing')">Planes</a>
        </nav>

        <!-- Botones (desktop) -->
        <div class="nav-buttons desktop-menu">
          <router-link to="/login">
            <button class="btn-secondary">Iniciar Sesión</button>
          </router-link>
          <router-link to="/registro">
            <button class="btn-primary">Crear Cuenta</button>
          </router-link>
        </div>

        <!-- Botón hamburguesa (móvil) -->
        <button class="menu-toggle" @click="toggleMenu">
          ☰
        </button>
      </div>
    </div>

    <!-- Menú móvil desplegable -->
    <transition name="slide">
      <div v-if="isMenuOpen" class="mobile-menu">
        <a @click.prevent="navigateTo('hero'); closeMenu()">Inicio</a>
        <a @click.prevent="navigateTo('about'); closeMenu()">Sobre Nosotros</a>
        <a @click.prevent="navigateTo('pricing'); closeMenu()">Planes</a>
        <router-link to="/login" @click="closeMenu">
          <button class="btn-secondary">Iniciar Sesión</button>
        </router-link>
        <router-link to="/registro" @click="closeMenu">
          <button class="btn-primary">Crear Cuenta</button>
        </router-link>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import gsap from 'gsap'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

gsap.registerPlugin(ScrollToPlugin)

const router = useRouter()
const route = useRoute()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
const closeMenu = () => {
  isMenuOpen.value = false
}

// Navegación con scroll animado
const navigateTo = (id) => {
  if (route.path !== '/') {
    router.push('/').then(() => {
      setTimeout(() => {
        const el = document.getElementById(id)
        if (el) {
          gsap.to(window, { duration: 1, scrollTo: { y: el, offsetY: 80 } })
        }
      }, 300)
    })
  } else {
    const el = document.getElementById(id)
    if (el) {
      gsap.to(window, { duration: 1, scrollTo: { y: el, offsetY: 80 } })
    }
  }
}
</script>

<style scoped>
/* Hamburguesa oculta en desktop */
.menu-toggle {
  display: none;
  font-size: 1.8rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #0f766e;
}

/* Menú móvil */
.mobile-menu {
    display: block;
    flex-direction: column;
    gap: 1rem;
    background: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-top: 1rem;
    animation: fadeIn 0.3s ease-in-out;
  }

  .mobile-menu a {
    font-size: 1rem;
    font-weight: 500;
    color: #374151;
    text-decoration: none;
  }

  .mobile-menu a:hover {
    color: #0f766e;
  }

  .mobile-menu .btn-primary,
  .mobile-menu .btn-secondary {
    width: 100%;
  }


/* Animación para el desplegable */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links,
  .nav-buttons {
    display: none; /* Oculta los links de arriba en móvil */
  }
}

.nav-links {
  display: flex;
  gap: 1.5rem; /* <-- Espacio entre los links */
  margin-left: 2rem;
  align-items: center;
}

.nav-links a {
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #0f766e;
}


</style>
