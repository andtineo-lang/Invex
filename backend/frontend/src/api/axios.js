import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');

    // Rutas donde NO queremos enviar el Bearer (login/registro)
    const authFreePaths = [
      '/auth/login',
      '/auth/register',
      '/auth/register-and-activate'
    ];

    const isAuthUrl =
      config.url && authFreePaths.some(path => config.url.includes(path));

    if (token && !isAuthUrl) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }

    return config;
  },
  error => Promise.reject(error)
);

export default axiosInstance;
