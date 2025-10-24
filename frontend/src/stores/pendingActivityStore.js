// ============================================================
// ARCHIVO: src/stores/pendingActivityStore.js
// Módulo: Stores (Pinia)
// Descripción: Store para gestión de estado de actividades pendientes
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import pendingActivityService from '@/services/pendingActivityService'

export const usePendingActivityStore = defineStore('pendingActivity', () => {
  // ============= STATE =============
  const activities = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedActivity = ref(null)

  // ============= GETTERS (COMPUTED) =============

  /**
   * Actividades pendientes (no completadas)
   */
  const activitiesPendientes = computed(() => {
    return activities.value.filter(a => !a.completada)
  })

  /**
   * Actividades completadas
   */
  const activitiesCompletadas = computed(() => {
    return activities.value.filter(a => a.completada)
  })

  /**
   * Actividades vencidas (fecha pasada y no completadas)
   */
  const activitiesVencidas = computed(() => {
    const now = new Date()
    return activities.value.filter(a => {
      if (a.completada) return false
      if (!a.fecha_vencimiento) return false
      return new Date(a.fecha_vencimiento) < now
    })
  })

  /**
   * Actividades por prioridad alta (pendientes)
   */
  const activitiesPrioridadAlta = computed(() => {
    return activitiesPendientes.value.filter(a => a.prioridad === 'alta')
  })

  /**
   * Contar actividades por prioridad
   */
  const contadorPorPrioridad = computed(() => {
    const pendientes = activitiesPendientes.value
    return {
      alta: pendientes.filter(a => a.prioridad === 'alta').length,
      media: pendientes.filter(a => a.prioridad === 'media').length,
      baja: pendientes.filter(a => a.prioridad === 'baja').length
    }
  })

  /**
   * Estadísticas generales
   */
  const estadisticas = computed(() => {
    const total = activities.value.length
    const pendientes = activitiesPendientes.value.length
    const completadas = activitiesCompletadas.value.length
    const vencidas = activitiesVencidas.value.length

    return {
      total,
      pendientes,
      completadas,
      vencidas,
      porcentajeCompletado: total > 0 ? Math.round((completadas / total) * 100) : 0
    }
  })

  /**
   * Actividades de hoy (vencen hoy)
   */
  const activitiesHoy = computed(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    return activitiesPendientes.value.filter(a => {
      if (!a.fecha_vencimiento) return false
      const dueDate = new Date(a.fecha_vencimiento)
      return dueDate >= today && dueDate < tomorrow
    })
  })

  /**
   * Actividades próximas (próximos 7 días)
   */
  const activitiesProximas = computed(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    const nextWeek = new Date(today)
    nextWeek.setDate(nextWeek.getDate() + 7)

    return activitiesPendientes.value.filter(a => {
      if (!a.fecha_vencimiento) return false
      const dueDate = new Date(a.fecha_vencimiento)
      return dueDate >= today && dueDate <= nextWeek
    })
  })

  // ============= ACTIONS =============

  /**
   * Obtener todas las actividades
   */
  async function fetchActivities(params = {}) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getActivities(params)
      
      if (response.success && response.data) {
        activities.value = response.data
      } else {
        throw new Error(response.message || 'Error al cargar actividades')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchActivities:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener actividades pendientes
   */
  async function fetchPendientes(usuarioId = null) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getPendientes(usuarioId)
      
      if (response.success && response.data) {
        activities.value = response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchPendientes:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener actividades completadas
   */
  async function fetchCompletadas(usuarioId = null) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getCompletadas(usuarioId)
      
      if (response.success && response.data) {
        activities.value = response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchCompletadas:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener actividades vencidas
   */
  async function fetchVencidas(usuarioId = null) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getVencidas(usuarioId)
      
      if (response.success && response.data) {
        activities.value = response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchVencidas:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener actividades por usuario
   */
  async function fetchByUsuario(usuarioId) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getByUsuario(usuarioId)
      
      if (response.success && response.data) {
        activities.value = response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchByUsuario:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener actividades por proyecto
   */
  async function fetchByProyecto(proyectoId) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getByProyecto(proyectoId)
      
      if (response.success && response.data) {
        activities.value = response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchByProyecto:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener una actividad específica
   */
  async function fetchActivity(activityId) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.getActivity(activityId)
      
      if (response.success && response.data) {
        selectedActivity.value = response.data
        return response.data
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en fetchActivity:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear nueva actividad
   */
  async function createActivity(activityData) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.createActivity(activityData)
      
      if (response.success && response.data) {
        // Agregar la nueva actividad al array
        activities.value.unshift(response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al crear actividad')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en createActivity:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar actividad existente
   */
  async function updateActivity(activityId, activityData) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.updateActivity(activityId, activityData)
      
      if (response.success && response.data) {
        // Actualizar en el array
        const index = activities.value.findIndex(a => a.id_actividad_pendiente === activityId)
        if (index !== -1) {
          activities.value[index] = response.data
        }
        return response.data
      } else {
        throw new Error(response.message || 'Error al actualizar actividad')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en updateActivity:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Marcar actividad como completada o pendiente
   */
  async function toggleCompletada(activityId, completada = true) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.marcarCompletada(activityId, completada)
      
      if (response.success && response.data) {
        // Actualizar en el array
        const index = activities.value.findIndex(a => a.id_actividad_pendiente === activityId)
        if (index !== -1) {
          activities.value[index].completada = completada
        }
        return response.data
      } else {
        throw new Error(response.message || 'Error al marcar actividad')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en toggleCompletada:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar actividad
   */
  async function deleteActivity(activityId) {
    loading.value = true
    error.value = null

    try {
      const response = await pendingActivityService.deleteActivity(activityId)
      
      if (response.success) {
        // Remover del array
        activities.value = activities.value.filter(a => a.id_actividad_pendiente !== activityId)
        return true
      } else {
        throw new Error(response.message || 'Error al eliminar actividad')
      }
    } catch (err) {
      error.value = err.message
      console.error('Error en deleteActivity:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Limpiar error
   */
  function clearError() {
    error.value = null
  }

  /**
   * Limpiar actividad seleccionada
   */
  function clearSelectedActivity() {
    selectedActivity.value = null
  }

  /**
   * Resetear store
   */
  function $reset() {
    activities.value = []
    loading.value = false
    error.value = null
    selectedActivity.value = null
  }

  // ============= RETURN (EXPONER) =============
  return {
    // State
    activities,
    loading,
    error,
    selectedActivity,

    // Getters
    activitiesPendientes,
    activitiesCompletadas,
    activitiesVencidas,
    activitiesPrioridadAlta,
    contadorPorPrioridad,
    estadisticas,
    activitiesHoy,
    activitiesProximas,

    // Actions
    fetchActivities,
    fetchPendientes,
    fetchCompletadas,
    fetchVencidas,
    fetchByUsuario,
    fetchByProyecto,
    fetchActivity,
    createActivity,
    updateActivity,
    toggleCompletada,
    deleteActivity,
    clearError,
    clearSelectedActivity,
    $reset
  }
})