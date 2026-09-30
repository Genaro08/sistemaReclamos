import axios from 'axios';

// URL base de la API backend en FastAPI
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const clienteAxios = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Solicitudes: Adjunta automáticamente el JWT Bearer Token si existe
clienteAxios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('tokenAcceso');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de Respuestas: Extrae de forma limpia el mensaje de error del backend
clienteAxios.interceptors.response.use(
  (response) => response,
  (error) => {
    const mensajeError =
      error.response?.data?.error ||
      error.response?.data?.mensaje ||
      'Ocurrió un error inesperado en el servidor.';
    return Promise.reject(new Error(mensajeError));
  }
);
