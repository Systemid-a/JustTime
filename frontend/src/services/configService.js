// ============================================================
// ARCHIVO: src/services/configService.js
// Módulo: Servicios
// Descripción: Servicio para gestionar configuraciones de usuario
// ============================================================

import apiClient from './api'

/**
 * Servicio de Configuraciones
 * Maneja todas las peticiones HTTP relacionadas con configuraciones
 */
const configService = {
  /**
   * Obtener todas las configuraciones (uso administrativo)
   * @returns {Promise} Lista de configuraciones
   */
  async getAllConfigs() {
    try {
      const response = await apiClient.get('/configuraciones/')
      return response.data
    } catch (error) {
      console.error('Error al obtener configuraciones:', error)
      throw error
    }
  },

  /**
   * Obtener configuración por ID
   * @param {number} configId - ID de la configuración
   * @returns {Promise} Datos de la configuración
   */
  async getConfig(configId) {
    try {
      const response = await apiClient.get(`/configuraciones/${configId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener configuración ${configId}:`, error)
      throw error
    }
  },

  /**
   * Obtener configuración de un usuario específico
   * @param {number} usuarioId - ID del usuario
   * @returns {Promise} Configuración del usuario
   */
  async getConfigByUsuario(usuarioId) {
    try {
      const response = await apiClient.get(`/configuraciones/usuario/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener configuración del usuario ${usuarioId}:`, error)
      throw error
    }
  },

  /**
   * Crear nueva configuración
   * @param {Object} configData - Datos de la configuración
   * @returns {Promise} Configuración creada
   */
  async createConfig(configData) {
    try {
      const response = await apiClient.post('/configuraciones/', configData)
      return response.data
    } catch (error) {
      console.error('Error al crear configuración:', error)
      throw error
    }
  },

  /**
   * Actualizar configuración por ID
   * @param {number} configId - ID de la configuración
   * @param {Object} configData - Datos actualizados
   * @returns {Promise} Configuración actualizada
   */
  async updateConfig(configId, configData) {
    try {
      const response = await apiClient.put(`/configuraciones/${configId}`, configData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar configuración ${configId}:`, error)
      throw error
    }
  },

  /**
   * Actualizar configuración por ID de usuario
   * @param {number} usuarioId - ID del usuario
   * @param {Object} configData - Datos actualizados
   * @returns {Promise} Configuración actualizada
   */
  async updateConfigByUsuario(usuarioId, configData) {
    try {
      const response = await apiClient.put(`/configuraciones/usuario/${usuarioId}`, configData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar configuración del usuario ${usuarioId}:`, error)
      throw error
    }
  },

  /**
   * Eliminar configuración por ID
   * @param {number} configId - ID de la configuración a eliminar
   * @returns {Promise} Confirmación de eliminación
   */
  async deleteConfig(configId) {
    try {
      const response = await apiClient.delete(`/configuraciones/${configId}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar configuración ${configId}:`, error)
      throw error
    }
  },

  /**
   * Eliminar configuración por ID de usuario
   * @param {number} usuarioId - ID del usuario
   * @returns {Promise} Confirmación de eliminación
   */
  async deleteConfigByUsuario(usuarioId) {
    try {
      const response = await apiClient.delete(`/configuraciones/usuario/${usuarioId}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar configuración del usuario ${usuarioId}:`, error)
      throw error
    }
  }
}

export default configService