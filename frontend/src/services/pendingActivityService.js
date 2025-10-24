// ============================================================
// ARCHIVO: src/services/pendingActivityService.js
// Módulo: Servicios
// Descripción: Servicio para gestionar operaciones CRUD de actividades pendientes
// ============================================================

import apiClient from './api'

/**
 * Servicio de Actividades Pendientes
 * Maneja todas las peticiones HTTP relacionadas con recordatorios y actividades
 */
const pendingActivityService = {
  /**
   * Obtener todas las actividades pendientes
   * @param {Object} params - Parámetros de filtro opcionales
   * @returns {Promise} Lista de actividades
   */
  async getActivities(params = {}) {
    try {
      const response = await apiClient.get('/pending-activities/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener actividades:', error)
      throw error
    }
  },

  /**
   * Obtener solo actividades pendientes (no completadas)
   * @param {number} usuarioId - ID del usuario (opcional)
   * @returns {Promise} Lista de actividades pendientes
   */
  async getPendientes(usuarioId = null) {
    try {
      const params = usuarioId ? { usuario_id: usuarioId } : {}
      const response = await apiClient.get('/pending-activities/pendientes', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener actividades pendientes:', error)
      throw error
    }
  },

  /**
   * Obtener solo actividades completadas
   * @param {number} usuarioId - ID del usuario (opcional)
   * @returns {Promise} Lista de actividades completadas
   */
  async getCompletadas(usuarioId = null) {
    try {
      const params = usuarioId ? { usuario_id: usuarioId } : {}
      const response = await apiClient.get('/pending-activities/completadas', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener actividades completadas:', error)
      throw error
    }
  },

  /**
   * Obtener actividades vencidas (fecha pasada y no completadas)
   * @param {number} usuarioId - ID del usuario (opcional)
   * @returns {Promise} Lista de actividades vencidas
   */
  async getVencidas(usuarioId = null) {
    try {
      const params = usuarioId ? { usuario_id: usuarioId } : {}
      const response = await apiClient.get('/pending-activities/vencidas', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener actividades vencidas:', error)
      throw error
    }
  },

  /**
   * Obtener actividades de un usuario específico
   * @param {number} usuarioId - ID del usuario
   * @returns {Promise} Lista de actividades del usuario
   */
  async getByUsuario(usuarioId) {
    try {
      const response = await apiClient.get(`/pending-activities/usuario/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener actividades del usuario ${usuarioId}:`, error)
      throw error
    }
  },

  /**
   * Obtener actividades de un proyecto específico
   * @param {number} proyectoId - ID del proyecto
   * @returns {Promise} Lista de actividades del proyecto
   */
  async getByProyecto(proyectoId) {
    try {
      const response = await apiClient.get(`/pending-activities/proyecto/${proyectoId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener actividades del proyecto ${proyectoId}:`, error)
      throw error
    }
  },

  /**
   * Obtener una actividad específica por ID
   * @param {number} activityId - ID de la actividad
   * @returns {Promise} Datos de la actividad
   */
  async getActivity(activityId) {
    try {
      const response = await apiClient.get(`/pending-activities/${activityId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener actividad ${activityId}:`, error)
      throw error
    }
  },

  /**
   * Crear una nueva actividad pendiente
   * @param {Object} activityData - Datos de la actividad a crear
   * @returns {Promise} Actividad creada
   */
  async createActivity(activityData) {
    try {
      const response = await apiClient.post('/pending-activities/', activityData)
      return response.data
    } catch (error) {
      console.error('Error al crear actividad:', error)
      throw error
    }
  },

  /**
   * Actualizar una actividad existente
   * @param {number} activityId - ID de la actividad
   * @param {Object} activityData - Datos actualizados
   * @returns {Promise} Actividad actualizada
   */
  async updateActivity(activityId, activityData) {
    try {
      const response = await apiClient.put(`/pending-activities/${activityId}`, activityData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar actividad ${activityId}:`, error)
      throw error
    }
  },

  /**
   * Marcar actividad como completada o pendiente
   * @param {number} activityId - ID de la actividad
   * @param {boolean} completada - true para completada, false para pendiente
   * @returns {Promise} Actividad actualizada
   */
  async marcarCompletada(activityId, completada = true) {
    try {
      const response = await apiClient.patch(
        `/pending-activities/${activityId}/completar`,
        null,
        { params: { completada } }
      )
      return response.data
    } catch (error) {
      console.error(`Error al marcar actividad ${activityId}:`, error)
      throw error
    }
  },

  /**
   * Eliminar una actividad
   * @param {number} activityId - ID de la actividad a eliminar
   * @returns {Promise} Confirmación de eliminación
   */
  async deleteActivity(activityId) {
    try {
      const response = await apiClient.delete(`/pending-activities/${activityId}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar actividad ${activityId}:`, error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de actividades
   * @param {number} usuarioId - ID del usuario (opcional)
   * @returns {Object} Estadísticas calculadas
   */
  async getEstadisticas(usuarioId = null) {
    try {
      // Obtener todas las actividades del usuario
      const response = usuarioId 
        ? await this.getByUsuario(usuarioId)
        : await this.getActivities()
      
      const activities = response.data || []
      
      // Calcular estadísticas
      const total = activities.length
      const pendientes = activities.filter(a => !a.completada).length
      const completadas = activities.filter(a => a.completada).length
      const vencidas = activities.filter(a => {
        if (a.completada) return false
        if (!a.fecha_vencimiento) return false
        return new Date(a.fecha_vencimiento) < new Date()
      }).length
      
      const porPrioridad = {
        alta: activities.filter(a => a.prioridad === 'alta' && !a.completada).length,
        media: activities.filter(a => a.prioridad === 'media' && !a.completada).length,
        baja: activities.filter(a => a.prioridad === 'baja' && !a.completada).length
      }
      
      return {
        total,
        pendientes,
        completadas,
        vencidas,
        porPrioridad,
        porcentajeCompletado: total > 0 ? Math.round((completadas / total) * 100) : 0
      }
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  }
}

export default pendingActivityService