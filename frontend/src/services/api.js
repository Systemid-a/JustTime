// ============================================================
// ARCHIVO 20/31: src/services/api.js
// Módulo: Servicios
// Descripción: Cliente HTTP Axios con interceptores JWT
// ============================================================

import axios from 'axios'
import { API_BASE_URL, TOKEN_KEY, MENSAJES_ERROR } from '@/utils/constants'

// ============= CREAR INSTANCIA DE AXIOS =============
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// ============= INTERCEPTOR DE REQUEST =============
// Agrega automáticamente el token JWT a todas las peticiones
apiClient.interceptors.request.use(
  (config) => {
    // Obtener token del localStorage
    const token = localStorage.getItem(TOKEN_KEY)
    
    // Si existe token, agregarlo al header Authorization
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// ============= INTERCEPTOR DE RESPONSE =============
// Maneja errores de autenticación y respuestas del servidor
apiClient.interceptors.response.use(
  (response) => {
    // Respuesta exitosa, retornarla directamente
    return response
  },
  (error) => {
    // Manejo de errores HTTP
    if (error.response) {
      const status = error.response.status
      
      switch (status) {
        case 401:
          // Token inválido o expirado
          // Limpiar token del localStorage
          localStorage.removeItem(TOKEN_KEY)
          
          // Redirigir al login solo si no estamos ya en esa ruta
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
          
          return Promise.reject({
            message: MENSAJES_ERROR.SESION_EXPIRADA,
            status: 401
          })
          
        case 403:
          // Sin permisos
          return Promise.reject({
            message: MENSAJES_ERROR.NO_AUTORIZADO,
            status: 403
          })
          
        case 404:
          // Recurso no encontrado
          return Promise.reject({
            message: 'Recurso no encontrado',
            status: 404
          })
          
        case 500:
          // Error del servidor
          return Promise.reject({
            message: MENSAJES_ERROR.SERVIDOR,
            status: 500
          })
          
        default:
          // Otros errores HTTP
          return Promise.reject({
            message: error.response.data?.detail || 'Error en la petición',
            status: status
          })
      }
    } else if (error.request) {
      // Error de red (sin respuesta del servidor)
      return Promise.reject({
        message: MENSAJES_ERROR.RED,
        status: 0
      })
    } else {
      // Error en la configuración de la petición
      return Promise.reject({
        message: 'Error al configurar la petición',
        status: -1
      })
    }
  }
)

// ============= EXPORTAR CLIENTE API =============
export default apiClient