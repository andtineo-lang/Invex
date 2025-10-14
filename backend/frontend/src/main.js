// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vClickOutside from 'v-click-outside'
import axios from 'axios' // <-- 1. Importa axios
import { createPinia } from 'pinia'

// Importar CSS global
import './assets/global.css'

// ------------------------------------------------------------------
// CONFIGURACIÓN GLOBAL DE AXIOS (AÑADIR ESTE BLOQUE)
// ------------------------------------------------------------------
// Busca el token de acceso en el localStorage del navegador.
const accessToken = localStorage.getItem('accessToken');

// Si encuentra un token, lo configura como el encabezado de autorización
// por defecto para TODAS las futuras peticiones de axios en tu aplicación.
if (accessToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}
// ------------------------------------------------------------------

// 1. Crea la app y guárdala en una variable
const app = createApp(App)
app.use(createPinia())
// 2. Usa los plugins que necesites
app.use(router)
app.use(vClickOutside)

// 3. Monta la app
app.mount('#app')