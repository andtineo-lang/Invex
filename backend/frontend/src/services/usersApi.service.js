// src/services/usersApi.service.js
import apiClient from '../api/axios.js'; // Importamos la instancia central de Axios

// Creamos el objeto de servicio directamente y lo exportamos
const userService = {
  list() {
    return apiClient.get('usuarios/');
  },

  create(userData) {
    return apiClient.post('usuarios/', userData);
  },

  update(userId, data) {
    return apiClient.patch(`usuarios/${userId}/`, data);
  },

  remove(userId) {
    return apiClient.delete(`usuarios/${userId}/`);
  }
};

export default userService;