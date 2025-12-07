// src/stores/auth.js

import { defineStore } from 'pinia'
import axiosInstance from '@/api/axios.js'

export const useAuthStore = defineStore('auth', {
  // 1. STATE: Donde guardamos la información
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    userRole: localStorage.getItem('userRole') || null,
    empresaId: localStorage.getItem('empresaId') || null,
    
    // 🔥 AÑADIDO: Aquí guardaremos el perfil completo (incluyendo el plan)
    user: null, 
  }),

  // 2. GETTERS: Propiedades computadas del estado
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getEmpresaId: (state) => state.empresaId,
    // Helper para obtener el plan fácilmente
    userPlan: (state) => state.user?.subscription_status || null,
  },

  // 3. ACTIONS: Métodos para cambiar el estado
  actions: {
    loginSuccess(token, role, idEmpresa) {
      this.accessToken = token;
      this.userRole = role;
      this.empresaId = idEmpresa;

      localStorage.setItem('accessToken', token);
      localStorage.setItem('userRole', role);
      localStorage.setItem('empresaId', idEmpresa);
      
      // Configura el encabezado de autorización
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // 🔥 AÑADIDO: Cargar datos del usuario inmediatamente al loguearse
      this.fetchUser();
    },

    // 🔥 NUEVA ACCIÓN: Cargar datos del usuario desde el Backend
    async fetchUser() {
        if (!this.accessToken) return;
        try {
            const response = await axiosInstance.get('/users/me/');
            // Guardamos TODA la info del usuario (nombre, email, PLAN) en el store
            this.user = response.data; 
        } catch (error) {
            console.error('Error cargando perfil de usuario:', error);
            // Si el token es inválido, podríamos cerrar sesión aquí
        }
    },

    logout() {
      this.accessToken = null;
      this.userRole = null;
      this.empresaId = null;
      this.user = null; // 🔥 Limpiar usuario al salir

      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('empresaId');
      
      delete axiosInstance.defaults.headers.common['Authorization'];
    },
  },
})