// ============================================================
// ARCHIVO 23/31: src/services/projectService.js
// Módulo: Servicios
// Descripción: Servicio HTTP para gestión de proyectos jurídicos
// ============================================================

import apiClient from './api'

/**
 * Servicio para gestión de proyectos
 * Incluye CRUD completo y métodos especializados
 */
const projectService = {
  /**
   * Obtener lista de todos los proyectos
   * @param {Object} params - Parámetros de filtrado opcionales
   * @returns {Promise<Array>} Lista de proyectos
   */
  async getProjects(params = {}) {
    try {
      const response = await apiClient.get('/projects/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener proyectos:', error)
      throw error
    }
  },

  /**
   * Obtener proyecto específico por ID
   * @param {Number} id - ID del proyecto
   * @returns {Promise<Object>} Datos del proyecto
   */
  async getProject(id) {
    try {
      const response = await apiClient.get(`/projects/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener proyecto ${id}:`, error)
      throw error
    }
  },

  /**
   * Crear nuevo proyecto
   * @param {Object} projectData - Datos del proyecto
   * @returns {Promise<Object>} Proyecto creado
   */
  async createProject(projectData) {
    try {
      const response = await apiClient.post('/projects/', projectData)
      return response.data
    } catch (error) {
      console.error('Error al crear proyecto:', error)
      throw error
    }
  },

  /**
   * Actualizar proyecto existente
   * @param {Number} id - ID del proyecto
   * @param {Object} projectData - Datos actualizados
   * @returns {Promise<Object>} Proyecto actualizado
   */
  async updateProject(id, projectData) {
    try {
      const response = await apiClient.put(`/projects/${id}`, projectData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar proyecto ${id}:`, error)
      throw error
    }
  },

  /**
   * Eliminar proyecto
   * @param {Number} id - ID del proyecto
   * @returns {Promise<Object>} Respuesta de confirmación
   */
  async deleteProject(id) {
    try {
      const response = await apiClient.delete(`/projects/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar proyecto ${id}:`, error)
      throw error
    }
  },

  /**
   * Obtener solo proyectos activos
   * @returns {Promise<Array>} Lista de proyectos activos
   */
  async getActiveProjects() {
    try {
      const response = await apiClient.get('/projects/activos')
      return response.data
    } catch (error) {
      console.error('Error al obtener proyectos activos:', error)
      throw error
    }
  },

  /**
   * Finalizar proyecto (cambiar estado a finalizado)
   * @param {Number} id - ID del proyecto
   * @returns {Promise<Object>} Proyecto finalizado
   */
  async finalizeProject(id) {
    try {
      const response = await apiClient.patch(`/projects/${id}/finalizar`)
      return response.data
    } catch (error) {
      console.error(`Error al finalizar proyecto ${id}:`, error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de proyectos para dashboard
   * @returns {Promise<Object>} Estadísticas de proyectos
   */
  async getProjectStats() {
    try {
      const response = await apiClient.get('/projects/dashboard/stats')
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de proyectos:', error)
      throw error
    }
  },

  /**
   * Filtrar proyectos por estado
   * @param {String} estado - Estado del proyecto (activo, pausado, finalizado)
   * @returns {Promise<Array>} Proyectos filtrados
   */
  async getProjectsByStatus(estado) {
    try {
      const response = await apiClient.get('/projects/', {
        params: { estado }
      })
      return response.data
    } catch (error) {
      console.error(`Error al filtrar proyectos por estado ${estado}:`, error)
      throw error
    }
  },

  /**
   * Filtrar proyectos por categoría
   * @param {Number} categoriaId - ID de la categoría
   * @returns {Promise<Array>} Proyectos filtrados
   */
  async getProjectsByCategory(categoriaId) {
    try {
      const response = await apiClient.get('/projects/', {
        params: { categoria_id: categoriaId }
      })
      return response.data
    } catch (error) {
      console.error(`Error al filtrar proyectos por categoría ${categoriaId}:`, error)
      throw error
    }
  }
}

export default projectService