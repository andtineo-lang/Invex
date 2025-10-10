// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vClickOutside from 'v-click-outside'
// Importar CSS global
import './assets/global.css'

// 1. Crea la app y guárdala en una variable
const app = createApp(App)

// 2. Usa los plugins que necesites
app.use(router)
app.use(vClickOutside) 

// 3. Monta la app
app.mount('#app')