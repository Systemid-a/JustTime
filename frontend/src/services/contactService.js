// ============================================================
// ARCHIVO 24/31: src/services/contactService.js
// Módulo: Servicios
// Descripción: Servicio HTTP para gestión de contactos (personas y empresas)
// ============================================================

import apiClient from './api'

/**
 * Servicio para gestión de contactos
 * Incluye CRUD completo y métodos especializados para personas y empresas
 */
const contactService = {
  /**
   * Obtener lista de todos los contactos
   * @param {Object} params - Parámetros de filtrado opcionales
   * @returns {Promise<Array>} Lista de contactos
   */
  async getContacts(params = {}) {
    try {
      const response = await apiClient.get('/contactos/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener contactos:', error)
      throw error
    }
  },

  /**
   * Obtener contacto específico por ID
   * @param {Number} id - ID del contacto
   * @returns {Promise<Object>} Datos del contacto
   */
  async getContact(id) {
    try {
      const response = await apiClient.get(`/contactos/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener contacto ${id}:`, error)
      throw error
    }
  },

  /**
   * Crear nuevo contacto
   * @param {Object} contactData - Datos del contacto
   * @returns {Promise<Object>} Contacto creado
   */
  async createContact(contactData) {
    try {
      const response = await apiClient.post('/contactos/', contactData)
      return response.data
    } catch (error) {
      console.error('Error al crear contacto:', error)
      throw error
    }
  },

  /**
   * Actualizar contacto existente
   * @param {Number} id - ID del contacto
   * @param {Object} contactData - Datos actualizados
   * @returns {Promise<Object>} Contacto actualizado
   */
  async updateContact(id, contactData) {
    try {
      const response = await apiClient.put(`/contactos/${id}`, contactData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar contacto ${id}:`, error)
      throw error
    }
  },

  /**
   * Eliminar contacto (soft delete - marca como inactivo)
   * @param {Number} id - ID del contacto
   * @returns {Promise<Object>} Respuesta de confirmación
   */
  async deleteContact(id) {
    try {
      const response = await apiClient.delete(`/contactos/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al eliminar contacto ${id}:`, error)
      throw error
    }
  },

  /**
   * Filtrar contactos por tipo (persona o empresa)
   * @param {String} tipo - Tipo de contacto ('persona' o 'empresa')
   * @returns {Promise<Array>} Contactos filtrados
   */
  async getContactsByType(tipo) {
    try {
      const response = await apiClient.get('/contactos/', {
        params: { tipo }
      })
      return response.data
    } catch (error) {
      console.error(`Error al filtrar contactos por tipo ${tipo}:`, error)
      throw error
    }
  },

  /**
   * Obtener solo contactos activos
   * @returns {Promise<Array>} Lista de contactos activos
   */
  async getActiveContacts() {
    try {
      const response = await apiClient.get('/contactos/', {
        params: { activo: true }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener contactos activos:', error)
      throw error
    }
  },

  /**
   * Obtener solo personas activas
   * @returns {Promise<Array>} Lista de personas activas
   */
  async getActivePersons() {
    try {
      const response = await apiClient.get('/contactos/', {
        params: { tipo: 'persona', activo: true }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener personas activas:', error)
      throw error
    }
  },

  /**
   * Obtener solo empresas activas
   * @returns {Promise<Array>} Lista de empresas activas
   */
  async getActiveCompanies() {
    try {
      const response = await apiClient.get('/contactos/', {
        params: { tipo: 'empresa', activo: true }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener empresas activas:', error)
      throw error
    }
  },

  /**
   * Buscar contactos por término (nombre, email o teléfono)
   * @param {String} searchTerm - Término de búsqueda
   * @returns {Promise<Array>} Contactos que coinciden
   */
  async searchContacts(searchTerm) {
    try {
      const response = await apiClient.get('/contactos/', {
        params: { search: searchTerm }
      })
      return response.data
    } catch (error) {
      console.error('Error al buscar contactos:', error)
      throw error
    }
  },

  /**
   * Cambiar estado de contacto (activo/inactivo)
   * @param {Number} id - ID del contacto
   * @param {Boolean} activo - Nuevo estado
   * @returns {Promise<Object>} Contacto actualizado
   */
  async toggleContactStatus(id, activo) {
    try {
      const response = await apiClient.patch(`/contactos/${id}`, { activo })
      return response.data
    } catch (error) {
      console.error(`Error al cambiar estado del contacto ${id}:`, error)
      throw error
    }
  }
}

export default contactService