// ============================================================
// ARCHIVO 32/33: src/services/analyticsService.js
// Módulo: Servicios
// Descripción: Servicio HTTP para módulo de análisis y reportes
// ============================================================

import apiClient from './api'

/**
 * Servicio para analytics y reportes
 * Consume endpoints de estadísticas y análisis de casos
 */
const analyticsService = {
  /**
   * Obtener casos agrupados por categoría
   * @returns {Promise<Object>} Estadísticas por categoría
   */
  async getCasosPorCategoria() {
    try {
      const response = await apiClient.get('/analytics/casos-por-categoria')
      return response.data
    } catch (error) {
      console.error('Error al obtener casos por categoría:', error)
      throw error
    }
  },

  /**
   * Obtener casos agrupados por estado
   * @returns {Promise<Object>} Estadísticas por estado con porcentajes
   */
  async getCasosPorEstado() {
    try {
      const response = await apiClient.get('/analytics/casos-por-estado')
      return response.data
    } catch (error) {
      console.error('Error al obtener casos por estado:', error)
      throw error
    }
  },

  /**
   * Obtener top contactos con más casos
   * @param {Number} limit - Cantidad máxima de contactos (default: 10)
   * @returns {Promise<Object>} Lista de contactos ordenados por cantidad de casos
   */
  async getCasosPorContacto(limit = 10) {
    try {
      const response = await apiClient.get('/analytics/casos-por-contacto', {
        params: { limit }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener casos por contacto:', error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de un contacto específico
   * @param {Number} contactoId - ID del contacto
   * @returns {Promise<Object>} Estadísticas del contacto
   */
  async getCasosContactoEspecifico(contactoId) {
    try {
      const response = await apiClient.get(`/analytics/casos-contacto/${contactoId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener casos del contacto ${contactoId}:`, error)
      throw error
    }
  },

  /**
   * Obtener resumen completo con todas las estadísticas
   * @returns {Promise<Object>} Resumen completo de analytics
   */
  async getResumenCompleto() {
    try {
      const response = await apiClient.get('/analytics/resumen-completo')
      return response.data
    } catch (error) {
      console.error('Error al obtener resumen completo:', error)
      throw error
    }
  }
}

export default analyticsService