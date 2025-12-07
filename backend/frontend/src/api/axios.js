import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000, // Aumentado a 30 segundos para importaciones grandes
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// --- 1. INTERCEPTOR DE SOLICITUD ---
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

// --- 2. INTERCEPTOR DE RESPUESTA ---
// Maneja los errores de token expirado (401) automáticamente.
axiosInstance.interceptors.response.use( 
  // (A) Si la respuesta es exitosa (2xx), no hace nada.
  response => response,

  // (B) Si la respuesta es un error (4xx o 5xx)...
  async error => {
    const originalRequest = error.config;

    // CORREGIDO: Verificar que error.response existe antes de acceder a .status
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try { 
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (!refreshToken) {
          throw new Error('No hay refresh token disponible');
        }

        const response = await axiosInstance.post('/auth/token/refresh/', {
          refresh: refreshToken
        });

      
        const newAccessToken = response.data.access; 
        localStorage.setItem('access_token', newAccessToken);
 
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
        return axiosInstance(originalRequest);

      } catch (refreshError) { 
        console.error("No se pudo refrescar el token. Deslogueando...", refreshError);
         
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        window.location.href = '/login';
        
        return Promise.reject(refreshError);
      }
    }

    // CORREGIDO: Mejorar el manejo de errores sin response
    if (!error.response) {
      // Error de red, timeout, o servidor no disponible
      console.error('Error de red:', error.message);
      error.message = 'Error de conexión. Verifica tu red o intenta más tarde.';
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;