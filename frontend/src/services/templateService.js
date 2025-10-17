// ============================================================
// ARCHIVO: src/services/templateService.js
// Módulo: Servicios
// Descripción: Servicio HTTP para gestión de plantillas de documentos Word
// ============================================================

import apiClient from './api' // ✅ CORREGIDO - importa de api.js

/**
 * Servicio para gestión de plantillas
 */
const templateService = {
  /**
   * Subir nueva plantilla .docx
   */
  async uploadTemplate(templateData, file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('nombre', templateData.nombre)
      
      if (templateData.categoria) {
        formData.append('categoria', templateData.categoria)
      }
      
      if (templateData.descripcion) {
        formData.append('descripcion', templateData.descripcion)
      }

      const response = await apiClient.post('/plantillas/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      return response.data
    } catch (error) {
      console.error('Error al subir plantilla:', error)
      throw error
    }
  },

  /**
   * Obtener lista de todas las plantillas
   */
  async getTemplates(params = {}) {
    try {
      const response = await apiClient.get('/plantillas/', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener plantillas:', error)
      throw error
    }
  },

  /**
   * Obtener plantilla específica por ID
   */
  async getTemplate(id) {
    try {
      const response = await apiClient.get(`/plantillas/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error al obtener plantilla ${id}:`, error)
      throw error
    }
  },

  /**
   * Descargar archivo .docx de plantilla
   */
  async downloadTemplate(id, nombreArchivo) {
    try {
      const response = await apiClient.get(`/plantillas/${id}/download`, {
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', nombreArchivo)
      document.body.appendChild(link)
      link.click()
      
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return response.data
    } catch (error) {
      console.error(`Error al descargar plantilla ${id}:`, error)
      throw error
    }
  },

  /**
   * Actualizar metadatos de plantilla
   */
  async updateTemplate(id, templateData) {
    try {
      const response = await apiClient.put(`/plantillas/${id}`, templateData)
      return response.data
    } catch (error) {
      console.error(`Error al actualizar plantilla ${id}:`, error)
      throw error
    }
  },

  /**
   * Eliminar plantilla
   */
  async deleteTemplate(id, hardDelete = false) {
    try {
      const response = await apiClient.delete(`/plantillas/${id}`, {
        params: { hard_delete: hardDelete }
      })
      return response.data
    } catch (error) {
      console.error(`Error al eliminar plantilla ${id}:`, error)
      throw error
    }
  },

  /**
   * Filtrar plantillas por categoría
   */
  async getTemplatesByCategory(categoria) {
    try {
      const response = await apiClient.get('/plantillas/', {
        params: { categoria }
      })
      return response.data
    } catch (error) {
      console.error(`Error al filtrar plantillas:`, error)
      throw error
    }
  },

  /**
   * Obtener solo plantillas activas
   */
  async getActiveTemplates() {
    try {
      const response = await apiClient.get('/plantillas/', {
        params: { solo_activas: true }
      })
      return response.data
    } catch (error) {
      console.error('Error al obtener plantillas activas:', error)
      throw error
    }
  },

  /**
   * Obtener estadísticas
   */
  async getStatistics() {
    try {
      const response = await apiClient.get('/plantillas/stats/summary')
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  },

  /**
   * Cambiar estado de plantilla
   */
  async toggleTemplateStatus(id, activo) {
    try {
      const response = await apiClient.put(`/plantillas/${id}`, { 
        activo: activo ? 1 : 0 
      })
      return response.data
    } catch (error) {
      console.error(`Error al cambiar estado:`, error)
      throw error
    }
  }
}

export default templateService
