// ============================================================
// ARCHIVO: src/services/employeeService.js
// Módulo: Servicios
// Descripción: Servicio para gestionar operaciones CRUD de empleados
// ============================================================

import apiClient from './api'

/**
 * Servicio de Empleados
 * Maneja todas las peticiones HTTP relacionadas con empleados
 */
const employeeService = {
  /**
   * Obtener todos los empleados
   * @param {Object} params - Parámetros de filtro opcionales
   * @returns {Promise} Lista de empleados
   */
  async getEmployees(params = {}) {
    try {
      const response = await apiClient.get('/empleados/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener empleados:', error)
      throw error
    }
  },

  /**
   * Obtener un empleado específico por ID
   * @param {number} employeeId - ID del empleado
   * @returns {Promise} Datos del empleado
   */
  async getEmployee(employeeId) {
    try {
      const response = await apiClient.get(`/empleados/${employeeId}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener empleado ${employeeId}:`, error)
      throw error
    }
  },

  /**
   * Crear un nuevo empleado SIN usuario asociado
   * @param {Object} employeeData - Datos del empleado a crear
   * @returns {Promise} Empleado creado
   */
  async createEmployee(employeeData) {
    try {
      const response = await apiClient.post('/empleados/', employeeData)
      return response.data
    } catch (error) {
      console.error('Error al crear empleado:', error)
      throw error
    }
  },

  /**
   * Crear un nuevo empleado CON usuario y rol
   * @param {Object} employeeData - Datos del empleado + usuario
   * @param {string} employeeData.nombre - Nombre del empleado
   * @param {string} employeeData.telefono - Teléfono del empleado
   * @param {string} employeeData.puesto - Puesto del empleado
   * @param {string} employeeData.email - Email para el usuario
   * @param {string} employeeData.password - Contraseña para el usuario
   * @param {string} employeeData.rol - Rol: 'admin' o 'usuario'
   * @returns {Promise} Empleado con usuario creado
   */
  async createEmployeeWithUser(employeeData) {
    try {
      const response = await apiClient.post('/empleados/con-usuario', employeeData)
      return response.data
    } catch (error) {
      console.error('Error al crear empleado con usuario:', error)
      throw error
    }
  },

  /**
   * Actualizar un empleado existente
   * @param {number} employeeId - ID del empleado
   * @param {Object} employeeData - Datos actualizados del empleado
   * @returns {Promise} Empleado actualizado
   */
  async updateEmployee(employeeId, employeeData) {
    try {
      const response = await apiClient.put(`/empleados/${employeeId}`, employeeData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar empleado ${employeeId}:`, error)
      throw error
    }
  },

  /**
   * Eliminar un empleado (soft delete)
   * @param {number} employeeId - ID del empleado a eliminar
   * @returns {Promise} Confirmación de eliminación
   */
  async deleteEmployee(employeeId) {
    try {
      const response = await apiClient.delete(`/empleados/${employeeId}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar empleado ${employeeId}:`, error)
      throw error
    }
  },

  /**
   * Vincular un usuario existente a un empleado existente
   * @param {number} employeeId - ID del empleado
   * @param {number} userId - ID del usuario a vincular
   * @returns {Promise} Empleado con usuario vinculado
   */
  async linkUserToEmployee(employeeId, userId) {
    try {
      const response = await apiClient.post(`/empleados/${employeeId}/vincular-usuario`, {
        usuario_id: userId
      })
      return response.data
    } catch (error) {
      console.error(`Error al vincular usuario a empleado ${employeeId}:`, error)
      throw error
    }
  },

  /**
   * Obtener empleados activos solamente
   * @returns {Promise} Lista de empleados activos
   */
  async getActiveEmployees() {
    try {
      const response = await apiClient.get('/empleados/', {
        params: { incluir_inactivos: false }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener empleados activos:', error)
      throw error
    }
  },

  /**
   * Obtener todos los empleados (activos e inactivos)
   * @returns {Promise} Lista completa de empleados
   */
  async getAllEmployees() {
    try {
      const response = await apiClient.get('/empleados/', {
        params: { incluir_inactivos: true }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener todos los empleados:', error)
      throw error
    }
  }
}

export default employeeService