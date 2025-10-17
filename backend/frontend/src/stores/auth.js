// src/stores/auth.js

import { defineStore } from 'pinia'
import axiosInstance from '@/api/axios.js'

export const useAuthStore = defineStore('auth', {
  // 1. STATE: Donde guardamos la información
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    userRole: localStorage.getItem('userRole') || null,
    // 💥 AÑADIDO: ID de la empresa
    empresaId: localStorage.getItem('empresaId') || null, 
  }),

  // 2. GETTERS: Propiedades computadas del estado
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    // 💥 AÑADIDO: Getter para el ID
    getEmpresaId: (state) => state.empresaId, 
  },

  // 3. ACTIONS: Métodos para cambiar el estado
  actions: {
    // MODIFICADO: Ahora acepta el idEmpresa
    loginSuccess(token, role, idEmpresa) {
      this.accessToken = token;
      this.userRole = role;
      // 💥 AÑADIDO: Guardar en estado y localStorage
      this.empresaId = idEmpresa; 

      localStorage.setItem('accessToken', token);
      localStorage.setItem('userRole', role);
      localStorage.setItem('empresaId', idEmpresa); // Guardar el ID de la empresa
      
      // Configura el encabezado de autorización para futuras peticiones
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    // Se llama para cerrar sesión o en caso de error
    logout() {
      this.accessToken = null;
      this.userRole = null;
      // 💥 AÑADIDO: Limpiar el ID
      this.empresaId = null; 

      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('empresaId'); // Limpiar el ID del storage
      
      delete axiosInstance.defaults.headers.common['Authorization'];
    },
  },
})