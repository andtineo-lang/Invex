import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: '/api', // Tu baseURL está correcta
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// --- 1. INTERCEPTOR DE SOLICITUD (El que ya tenías) ---
// Añade el token de acceso a cada solicitud saliente.
axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  error => Promise.reject(error)
);

// --- 2. INTERCEPTOR DE RESPUESTA (¡El nuevo!) ---
// Maneja los errores de token expirado (401) automáticamente.
axiosInstance.interceptors.response.use(
  
  // (A) Si la respuesta es exitosa (2xx), no hace nada.
  response => response,

  // (B) Si la respuesta es un error (4xx o 5xx)...
  async error => {
    const originalRequest = error.config;
    
    // Comprueba si es un error 401 (No autorizado) y si no es un reintento.
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Marca este request para no reintentarlo infinitamente

      try {
        // 3. Intenta obtener un nuevo token de acceso usando el 'refresh_token'
        const refreshToken = localStorage.getItem('refresh_token');
        
        const response = await axiosInstance.post('/auth/token/refresh/', {
          refresh: refreshToken
        });

        // 4. Éxito: Se obtuvo un nuevo token de acceso
        const newAccessToken = response.data.access;

        // 5. Guarda el nuevo token en localStorage
        localStorage.setItem('access_token', newAccessToken);

        // 6. Actualiza el header de la solicitud original y la reintenta
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
        return axiosInstance(originalRequest);

      } catch (refreshError) {
        // 7. Fracaso: El 'refresh_token' es inválido o también expiró
        console.error("No se pudo refrescar el token. Deslogueando...", refreshError);
        
        // 8. Limpia todo y envía al usuario al login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // (Opcional, si estás fuera de un componente Vue)
        window.location.href = '/login'; 
        
        return Promise.reject(refreshError);
      }
    }

    // Para cualquier otro error (404, 500, etc.), simplemente rechaza la promesa.
    return Promise.reject(error);
  }
);

export default axiosInstance;