// ============================================================
// ARCHIVO 25/31: src/stores/authStore.js (VERSIÓN CORREGIDA)
// Módulo: Stores (Pinia)
// Descripción: Estado global de autenticación con Pinia
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService'
import { ROLES } from '@/utils/constants'

export const useAuthStore = defineStore('auth', () => {
  // ============= ESTADO =============
  const user = ref(null)
  const token = ref(authService.getToken())
  const loading = ref(false)
  const error = ref(null)

  // ============= GETTERS (Computed) =============
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value
  })

  const userRole = computed(() => {
    return user.value?.rol || ROLES.USUARIO
  })

  const userName = computed(() => {
    return user.value?.nombre || 'Usuario'
  })

  const userEmail = computed(() => {
    return user.value?.email || ''
  })

  const isAdmin = computed(() => {
    return userRole.value === ROLES.ADMIN || userRole.value === 'admin'
  })

  // ============= ACTIONS =============
  
  /**
   * Iniciar sesión
   * @param {string} email
   * @param {string} password
   */
  async function login(email, password) {
    loading.value = true
    error.value = null
    
    try {
      // Llamar al servicio de autenticación
      const response = await authService.login(email, password)
      
      // Guardar token
      token.value = response.data.access_token
      
      // Obtener datos del usuario actual
      await fetchCurrentUser()
      
      return { success: true, message: response.message }
    } catch (err) {
      error.value = err.message || 'Error al iniciar sesión'
      token.value = null
      user.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Cerrar sesión
   */
  function logout() {
    // Limpiar servicio
    authService.logout()
    
    // Limpiar estado
    user.value = null
    token.value = null
    error.value = null
  }

  /**
   * Obtener información del usuario actual
   * ✅ VERSIÓN CORREGIDA - Usa el endpoint real /api/auth/me
   */
  async function fetchCurrentUser() {
    if (!token.value) {
      user.value = null
      return
    }

    loading.value = true
    try {
      // ✅ CORRECCIÓN: Obtener usuario real desde el backend
      const userData = await authService.getCurrentUser()
      
      // Asignar los datos reales del usuario
      user.value = {
        id_usuario: userData.id_usuario,
        nombre: userData.nombre,
        email: userData.email,
        rol: userData.rol || 'usuario',
        activo: userData.activo
      }
      
      console.log('✅ Usuario cargado:', user.value)
      
    } catch (err) {
      console.error('❌ Error al obtener usuario:', err)
      // Si falla la petición, limpiar sesión
      logout()
    } finally {
      loading.value = false
    }
  }

  /**
   * Verificar autenticación al cargar la app
   * Intenta obtener datos del usuario si existe token
   */
  async function checkAuth() {
    const storedToken = authService.getToken()
    
    if (storedToken) {
      token.value = storedToken
      await fetchCurrentUser()
    }
  }

  /**
   * Limpiar error
   */
  function clearError() {
    error.value = null
  }

  // ============= RETURN =============
  return {
    // Estado
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    userRole,
    userName,
    userEmail,
    isAdmin,
    
    // Actions
    login,
    logout,
    fetchCurrentUser,
    checkAuth,
    clearError
  }
})