// ============================================================
// ARCHIVO: src/stores/configStore.js
// Módulo: Stores (Pinia)
// Descripción: Estado global de configuraciones con Pinia
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import configService from '@/services/configService'

export const useConfigStore = defineStore('config', () => {
  // ============= ESTADO =============
  const currentConfig = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // ============= GETTERS (Computed) =============
  
  /**
   * Verificar si hay una configuración cargada
   */
  const hasConfig = computed(() => {
    return currentConfig.value !== null
  })

  /**
   * Obtener idioma actual
   */
  const currentLanguage = computed(() => {
    return currentConfig.value?.idioma || 'es'
  })

  /**
   * Obtener rol actual
   */
  const currentRole = computed(() => {
    return currentConfig.value?.rol || 'usuario'
  })

  /**
   * Obtener tema actual
   */
  const currentTheme = computed(() => {
    return currentConfig.value?.tema || 'claro'
  })

  /**
   * Verificar si el usuario es administrador
   */
  const isAdmin = computed(() => {
    return currentConfig.value?.rol === 'admin'
  })

  /**
   * Verificar si el tema es oscuro
   */
  const isDarkTheme = computed(() => {
    return currentConfig.value?.tema === 'oscuro'
  })

  // ============= ACTIONS =============

  /**
   * Obtener configuración del usuario actual
   */
  async function fetchUserConfig(usuarioId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await configService.getConfigByUsuario(usuarioId)
      
      if (response.success && response.data) {
        currentConfig.value = response.data
        
        // Aplicar tema al documento
        applyTheme(response.data.tema)
        
        // Aplicar idioma (si tienes i18n configurado)
        // applyLanguage(response.data.idioma)
        
        console.log('✅ Configuración cargada:', response.data)
      } else {
        throw new Error(response.message || 'Error al cargar configuración')
      }
      
      return currentConfig.value
    } catch (err) {
      error.value = err.message || 'Error al cargar configuración'
      console.error('Error en fetchUserConfig:', err)
      
      // 🆕 Si no existe configuración, crearla automáticamente
      if (err.response?.status === 404) {
        console.log('ℹ️ No hay configuración, creando una por defecto...')
        try {
          await createConfig({
            usuario_id_fk: usuarioId,
            idioma: 'es',
            rol: 'usuario',
            tema: 'claro'
          })
          console.log('✅ Configuración creada exitosamente')
          return currentConfig.value
        } catch (createError) {
          console.error('Error al crear configuración:', createError)
          // Usar valores por defecto sin guardar
          currentConfig.value = {
            usuario_id_fk: usuarioId,
            idioma: 'es',
            rol: 'usuario',
            tema: 'claro'
          }
        }
      }
      
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear configuración para un nuevo usuario
   */
  async function createConfig(configData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await configService.createConfig(configData)
      
      if (response.success && response.data) {
        currentConfig.value = response.data
        applyTheme(response.data.tema)
        console.log('✅ Configuración creada:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al crear configuración')
      }
    } catch (err) {
      error.value = err.message || 'Error al crear configuración'
      console.error('Error en createConfig:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar configuración del usuario actual
   */
  async function updateUserConfig(usuarioId, configData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await configService.updateConfigByUsuario(usuarioId, configData)
      
      if (response.success && response.data) {
        currentConfig.value = response.data
        
        // Aplicar cambios inmediatamente
        if (configData.tema) {
          applyTheme(configData.tema)
        }
        
        console.log('✅ Configuración actualizada:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al actualizar configuración')
      }
    } catch (err) {
      // Si el error es 404, significa que no existe configuración
      if (err.response?.status === 404) {
        console.log('⚠️ Configuración no encontrada, creando una nueva...')
        
        // Crear configuración nueva con los datos proporcionados
        const newConfigData = {
          usuario_id_fk: usuarioId,
          idioma: configData.idioma || 'es',
          rol: configData.rol || 'usuario',
          tema: configData.tema || 'claro'
        }
        
        return await createConfig(newConfigData)
      }
      
      error.value = err.message || 'Error al actualizar configuración'
      console.error('Error en updateUserConfig:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Cambiar idioma
   */
  async function changeLanguage(usuarioId, newLanguage) {
    try {
      // Si no hay configuración, crearla primero
      if (!currentConfig.value) {
        console.log('⚠️ No hay configuración, creando una primero...')
        await createConfig({
          usuario_id_fk: usuarioId,
          idioma: newLanguage,
          rol: 'usuario',
          tema: 'claro'
        })
        return true
      }
      
      await updateUserConfig(usuarioId, { idioma: newLanguage })
      console.log(`✅ Idioma cambiado a: ${newLanguage}`)
      return true
    } catch (err) {
      console.error('Error al cambiar idioma:', err)
      throw err
    }
  }

  /**
   * Cambiar tema
   */
  async function changeTheme(usuarioId, newTheme) {
    try {
      // Si no hay configuración, crearla primero
      if (!currentConfig.value) {
        console.log('⚠️ No hay configuración, creando una primero...')
        await createConfig({
          usuario_id_fk: usuarioId,
          idioma: 'es',
          rol: 'usuario',
          tema: newTheme
        })
        return true
      }
      
      await updateUserConfig(usuarioId, { tema: newTheme })
      console.log(`✅ Tema cambiado a: ${newTheme}`)
      return true
    } catch (err) {
      console.error('Error al cambiar tema:', err)
      throw err
    }
  }

  /**
   * Cambiar rol (solo admin puede hacer esto)
   */
  async function changeRole(usuarioId, newRole) {
    try {
      await updateUserConfig(usuarioId, { rol: newRole })
      console.log(`✅ Rol cambiado a: ${newRole}`)
      return true
    } catch (err) {
      console.error('Error al cambiar rol:', err)
      throw err
    }
  }

  /**
   * Aplicar tema al documento HTML
   */
  function applyTheme(theme) {
    console.log('🎨 Aplicando tema:', theme)
    const html = document.documentElement
    
    if (theme === 'oscuro') {
      html.classList.add('dark')
      localStorage.setItem('theme', 'oscuro')
      console.log('✅ Tema oscuro aplicado - Clases HTML:', html.className)
    } else {
      html.classList.remove('dark')
      localStorage.setItem('theme', 'claro')
      console.log('✅ Tema claro aplicado - Clases HTML:', html.className)
    }
    
    // Forzar re-render
    document.body.style.backgroundColor = theme === 'oscuro' ? '#1a1a1a' : '#f9fafb'
  }

  /**
   * Inicializar tema desde localStorage (útil al cargar la app)
   */
  function initializeThemeFromStorage() {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      applyTheme(savedTheme)
    }
  }

  /**
   * Limpiar errores
   */
  function clearError() {
    error.value = null
  }

  /**
   * Resetear el store completo
   */
  function $reset() {
    currentConfig.value = null
    loading.value = false
    error.value = null
  }

  // ============= RETORNAR API PÚBLICA =============
  return {
    // Estado
    currentConfig,
    loading,
    error,
    
    // Getters
    hasConfig,
    currentLanguage,
    currentRole,
    currentTheme,
    isAdmin,
    isDarkTheme,
    
    // Actions
    fetchUserConfig,
    createConfig,
    updateUserConfig,
    changeLanguage,
    changeTheme,
    changeRole,
    applyTheme,
    initializeThemeFromStorage,
    clearError,
    $reset
  }
})