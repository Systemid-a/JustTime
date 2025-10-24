// ============================================================
// ARCHIVO 25/31: src/stores/authStore.js - VERSIÓN FINAL ✅
// Módulo: Stores (Pinia)
// Descripción: Estado global de autenticación con Pinia
// ✅ IMPLEMENTADO: Guarda rol, idioma y tema + persistencia en localStorage
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService'
import { ROLES, TOKEN_KEY } from '@/utils/constants'

export const useAuthStore = defineStore('auth', () => {
  // ============= ESTADO =============
  const user = ref(null)
  const token = ref(authService.getToken())
  const loading = ref(false)
  const error = ref(null)

  // ============= GETTERS (Computed) =============
  
  /**
   * Verificar si el usuario está autenticado
   */
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value
  })

  /**
   * Obtener rol del usuario
   */
  const userRole = computed(() => {
    return user.value?.rol || ROLES.USUARIO
  })

  /**
   * Obtener nombre del usuario
   */
  const userName = computed(() => {
    return user.value?.nombre || 'Usuario'
  })

  /**
   * Obtener email del usuario
   */
  const userEmail = computed(() => {
    return user.value?.email || ''
  })

  /**
   * Verificar si el usuario es administrador
   */
  const isAdmin = computed(() => {
    return userRole.value === ROLES.ADMIN || userRole.value === 'admin'
  })

  /**
   * ⭐ NUEVO: Obtener idioma del usuario
   */
  const userLanguage = computed(() => {
    return user.value?.idioma || 'es'
  })

  /**
   * ⭐ NUEVO: Obtener tema del usuario
   */
  const userTheme = computed(() => {
    return user.value?.tema || 'claro'
  })

  /**
   * ⭐ NUEVO: Nombre del rol (para mostrar en UI)
   */
  const userRoleName = computed(() => {
    return isAdmin.value ? 'Administrador' : 'Usuario'
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
      
      // Limpiar localStorage en caso de error
      localStorage.removeItem('justtime_user')
      localStorage.removeItem(TOKEN_KEY)
      
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
    
    // ⭐ NUEVO: Limpiar localStorage
    localStorage.removeItem('justtime_user')
    localStorage.removeItem(TOKEN_KEY)
    
    console.log('✅ Sesión cerrada correctamente')
  }

  /**
   * Obtener información del usuario actual
   * ✅ VERSIÓN MEJORADA - Incluye rol, idioma y tema
   */
  async function fetchCurrentUser() {
    if (!token.value) {
      user.value = null
      return
    }

    loading.value = true
    try {
      // Obtener usuario real desde el backend
      const userData = await authService.getCurrentUser()
      
      // ⭐ MEJORADO: Asignar TODOS los datos del usuario (incluyendo idioma y tema)
      user.value = {
        id_usuario: userData.id_usuario,
        nombre: userData.nombre,
        email: userData.email,
        rol: userData.rol || 'usuario',
        idioma: userData.idioma || 'es',      // ⭐ NUEVO
        tema: userData.tema || 'claro',       // ⭐ NUEVO
        activo: userData.activo
      }
      
      // ⭐ NUEVO: Guardar usuario en localStorage para persistencia
      localStorage.setItem('justtime_user', JSON.stringify(user.value))
      
      console.log('✅ Usuario cargado:', {
        nombre: user.value.nombre,
        rol: user.value.rol,
        idioma: user.value.idioma,
        tema: user.value.tema
      })
      
    } catch (err) {
      console.error('❌ Error al obtener usuario:', err)
      // Si falla la petición, limpiar sesión
      logout()
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * ⭐ MEJORADO: Verificar autenticación al cargar la app
   * Restaura datos desde localStorage si existen
   */
  async function checkAuth() {
    const storedToken = authService.getToken()
    const storedUser = localStorage.getItem('justtime_user')
    
    if (storedToken) {
      token.value = storedToken
      
      // Si hay usuario en localStorage, cargarlo primero
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
          console.log('✅ Usuario restaurado desde localStorage')
        } catch (e) {
          console.warn('⚠️ Error al parsear usuario de localStorage')
        }
      }
      
      // Luego actualizar desde el backend
      try {
        await fetchCurrentUser()
      } catch (err) {
        console.error('❌ Error al verificar autenticación:', err)
        logout()
      }
    } else {
      // No hay token, asegurar que todo esté limpio
      user.value = null
      token.value = null
      localStorage.removeItem('justtime_user')
    }
  }

  /**
   * ⭐ NUEVO: Actualizar configuración del usuario (idioma, tema, etc)
   * @param {Object} config - { idioma?, tema?, rol? }
   */
  async function updateUserConfig(config) {
    if (!user.value) {
      throw new Error('No hay usuario autenticado')
    }

    try {
      // Actualizar localmente primero (UX optimista)
      const updatedUser = {
        ...user.value,
        ...config
      }
      user.value = updatedUser
      
      // Guardar en localStorage
      localStorage.setItem('justtime_user', JSON.stringify(user.value))
      
      console.log('✅ Configuración actualizada:', config)
      
      // Aquí podrías llamar al backend para persistir los cambios
      // await apiClient.put(`/configuraciones/usuario/${user.value.id_usuario}`, config)
      
      return { success: true }
    } catch (err) {
      console.error('❌ Error al actualizar configuración:', err)
      throw err
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
    userLanguage,     // ⭐ NUEVO
    userTheme,        // ⭐ NUEVO
    userRoleName,     // ⭐ NUEVO
    
    // Actions
    login,
    logout,
    fetchCurrentUser,
    checkAuth,
    updateUserConfig, // ⭐ NUEVO
    clearError
  }
})