// src/stores/auth.js

import { defineStore } from 'pinia'
import axiosInstance from '@/api/axios.js'

export const useAuthStore = defineStore('auth', {
  // 1. STATE: Donde guardamos la información
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    userRole: localStorage.getItem('userRole') || null,
  }),

  // 2. GETTERS: Propiedades computadas del estado
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  // 3. ACTIONS: Métodos para cambiar el estado
  actions: {
    // Se llama cuando el login es exitoso
    loginSuccess(token, role) {
      this.accessToken = token;
      this.userRole = role;
      localStorage.setItem('accessToken', token);
      localStorage.setItem('userRole', role);
      // Configura el encabezado de autorización para futuras peticiones
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    // Se llama para cerrar sesión o en caso de error
    logout() {
      this.accessToken = null;
      this.userRole = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
      delete axiosInstance.defaults.headers.common['Authorization'];
    },
  },
})