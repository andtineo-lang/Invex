// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vClickOutside from 'v-click-outside'
import { createPinia } from 'pinia'

// Importar CSS global
import './assets/global.css'

// El bloque de configuración de Axios ha sido eliminado de aquí.

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vClickOutside)
app.mount('#app')