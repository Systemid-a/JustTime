// ============================================================
// ARCHIVO 22/31: src/services/taskService.js
// Módulo: Servicios
// Descripción: Servicio para gestionar operaciones CRUD de tareas
// ============================================================

import apiClient from './api'

/**
 * Servicio de Tareas
 * Maneja todas las peticiones HTTP relacionadas con tareas
 */
const taskService = {
  /**
   * Obtener todas las tareas
   * @param {Object} params - Parámetros de filtro opcionales
   * @returns {Promise} Lista de tareas
   */
  async getTasks(params = {}) {
    try {
      const response = await apiClient.get('/tasks/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener tareas:', error)
      throw error
    }
  },

  /**
   * Obtener tablero Kanban con tareas organizadas por estado
   * @returns {Promise} Tareas organizadas en formato Kanban
   */
  async getKanbanBoard() {
    try {
      const response = await apiClient.get('/tasks/kanban')
      return response.data
    } catch (error) {
      console.error('Error al obtener tablero Kanban:', error)
      throw error
    }
  },

  /**
   * Obtener una tarea específica por ID
   * @param {number} taskId - ID de la tarea
   * @returns {Promise} Datos de la tarea
   */
  async getTask(taskId) {
    try {
      const response = await apiClient.get(`/tasks/${taskId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener tarea ${taskId}:`, error)
      throw error
    }
  },

  /**
   * Crear una nueva tarea
   * @param {Object} taskData - Datos de la tarea a crear
   * @returns {Promise} Tarea creada
   */
  async createTask(taskData) {
    try {
      const response = await apiClient.post('/tasks/', taskData)
      return response.data
    } catch (error) {
      console.error('Error al crear tarea:', error)
      throw error
    }
  },

  /**
   * Actualizar una tarea existente
   * @param {number} taskId - ID de la tarea
   * @param {Object} taskData - Datos actualizados de la tarea
   * @returns {Promise} Tarea actualizada
   */
  async updateTask(taskId, taskData) {
    try {
      const response = await apiClient.put(`/tasks/${taskId}`, taskData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar tarea ${taskId}:`, error)
      throw error
    }
  },

  /**
   * Actualizar solo el estado de una tarea (para drag & drop en Kanban)
   * @param {number} taskId - ID de la tarea
   * @param {string} newStatus - Nuevo estado (nuevo, en_progreso, finalizado)
   * @returns {Promise} Tarea con estado actualizado
   */
  async updateTaskStatus(taskId, newStatus) {
    try {
      const response = await apiClient.patch(`/tasks/${taskId}/estado`, {
        estado: newStatus
      })
      return response.data
    } catch (error) {
      console.error(`Error al actualizar estado de tarea ${taskId}:`, error)
      throw error
    }
  },

  /**
   * Eliminar una tarea
   * @param {number} taskId - ID de la tarea a eliminar
   * @returns {Promise} Confirmación de eliminación
   */
  async deleteTask(taskId) {
    try {
      const response = await apiClient.delete(`/tasks/${taskId}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar tarea ${taskId}:`, error)
      throw error
    }
  },

  /**
   * Obtener tareas filtradas por proyecto
   * @param {number} projectId - ID del proyecto
   * @returns {Promise} Lista de tareas del proyecto
   */
  async getTasksByProject(projectId) {
    try {
      const response = await apiClient.get('/tasks/', {
        params: { proyecto_id: projectId }
      })
      return response.data
    } catch (error) {
      console.error(`Error al obtener tareas del proyecto ${projectId}:`, error)
      throw error
    }
  },

  /**
   * Obtener tareas filtradas por estado
   * @param {string} status - Estado de las tareas (nuevo, en_progreso, finalizado)
   * @returns {Promise} Lista de tareas con el estado especificado
   */
  async getTasksByStatus(status) {
    try {
      const response = await apiClient.get('/tasks/', {
        params: { estado: status }
      })
      return response.data
    } catch (error) {
      console.error(`Error al obtener tareas con estado ${status}:`, error)
      throw error
    }
  }
}

export default taskService