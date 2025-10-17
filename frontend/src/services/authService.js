// ============================================================
// ARCHIVO 21/31: src/services/authService.js
// Módulo: Servicios
// Descripción: Servicio de autenticación - CORREGIDO
// ============================================================

import apiClient from './api'
import { TOKEN_KEY } from '@/utils/constants'

// ============= SERVICIO DE AUTENTICACIÓN =============
const authService = {
  /**
   * Iniciar sesión con email y password
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @returns {Promise} - Token y datos del usuario
   */
  async login(email, password) {
    try {
      const response = await apiClient.post('/auth/login', {
        email,
        password
      })
      
      // El backend retorna: { data: { access_token, token_type }, message, status }
      const { access_token } = response.data.data
      
      // Guardar token en localStorage
      if (access_token) {
        localStorage.setItem(TOKEN_KEY, access_token)
      }
      
      return response.data
    } catch (error) {
      // Propagar el error para que el componente lo maneje
      throw error
    }
  },

  /**
   * Cerrar sesión y limpiar token
   */
  logout() {
    // Eliminar token del localStorage
    localStorage.removeItem(TOKEN_KEY)
  },

  /**
   * Obtener información del usuario actual autenticado
   * Decodifica el JWT para extraer los datos del usuario
   * @returns {Promise} - Datos del usuario
   */
  async getCurrentUser() {
    try {
      // OPCIÓN 1: Intentar obtener desde endpoint /api/auth/me
      try {
        const response = await apiClient.get('/auth/me')
        if (response.data?.data) {
          return response.data.data
        }
      } catch (err) {
        console.log('Endpoint /auth/me no disponible, usando JWT decode')
      }
      
      // OPCIÓN 2: Decodificar el JWT manualmente
      const token = this.getToken()
      if (!token) return null
      
      // Decodificar JWT (sin verificar firma, solo leer datos)
      const payload = this.decodeJWT(token)
      
      if (payload) {
        // El JWT debe contener: sub (id_usuario), email, nombre, rol
        return {
          id_usuario: payload.sub || payload.id_usuario,
          nombre: payload.nombre || payload.name || 'Usuario',
          email: payload.email || '',
          rol: payload.rol || payload.role || 'usuario',
          activo: true
        }
      }
      
      return null
    } catch (error) {
      console.error('Error al obtener usuario actual:', error)
      throw error
    }
  },

  /**
   * Decodificar JWT manualmente (solo lectura del payload)
   * @param {string} token - JWT token
   * @returns {object|null} - Payload del token
   */
  decodeJWT(token) {
    try {
      // JWT tiene 3 partes: header.payload.signature
      const parts = token.split('.')
      if (parts.length !== 3) return null
      
      // Decodificar el payload (segunda parte)
      const payload = parts[1]
      
      // Decodificar base64url
      const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )
      
      return JSON.parse(jsonPayload)
    } catch (error) {
      console.error('Error al decodificar JWT:', error)
      return null
    }
  },

  /**
   * Verificar si existe un token en localStorage
   * @returns {boolean}
   */
  isAuthenticated() {
    const token = localStorage.getItem(TOKEN_KEY)
    return !!token
  },

  /**
   * Obtener token del localStorage
   * @returns {string|null}
   */
  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },

  /**
   * Verificar validez del token con el backend
   * @returns {Promise<boolean>}
   */
  async verifyToken() {
    try {
      const token = this.getToken()
      if (!token) return false
      
      const response = await apiClient.post('/auth/verify-token', { token })
      return response.data.data ? response.data.data.valid : false
    } catch (error) {
      console.error('Error al verificar token:', error)
      return false
    }
  }
}

export default authService