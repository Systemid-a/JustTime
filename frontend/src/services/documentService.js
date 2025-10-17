// ============================================================
// ARCHIVO: src/services/documentService.js - VERSIÓN FINAL
// Módulo: Services
// Descripción: Servicio para gestión de documentos
// ============================================================

import apiClient from './api' // ✅ CORREGIDO - importa de api.js

/**
 * Servicio de Documentos
 * Gestión completa de documentos del sistema
 */
const documentService = {
  
  /**
   * Obtener todos los documentos
   */
  async getDocuments(params = {}) {
    try {
      const response = await apiClient.get('/documentos', { params })
      return response.data
    } catch (error) {
      console.error('Error al obtener documentos:', error)
      throw error
    }
  },

  /**
   * Obtener documento por ID
   */
  async getDocumentById(id) {
    try {
      const response = await apiClient.get(`/documentos/${id}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener documento:', error)
      throw error
    }
  },

  /**
   * Subir nuevo documento
   */
  async uploadDocument(documentData, file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('nombre', documentData.nombre)
      
      if (documentData.categoria) {
        formData.append('categoria', documentData.categoria)
      }
      if (documentData.descripcion) {
        formData.append('descripcion', documentData.descripcion)
      }
      if (documentData.proyecto_id) {
        formData.append('proyecto_id', documentData.proyecto_id)
      }

      const response = await apiClient.post('/documentos/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error al subir documento:', error)
      throw error
    }
  },

  /**
   * Actualizar documento
   */
  async updateDocument(id, updateData) {
    try {
      const response = await apiClient.put(`/documentos/${id}`, updateData)
      return response.data
    } catch (error) {
      console.error('Error al actualizar documento:', error)
      throw error
    }
  },

  /**
   * Eliminar documento
   */
  async deleteDocument(id, hardDelete = false) {
    try {
      const response = await apiClient.delete(`/documentos/${id}`, {
        params: { hard_delete: hardDelete }
      })
      return response.data
    } catch (error) {
      console.error('Error al eliminar documento:', error)
      throw error
    }
  },

  /**
   * Descargar documento
   */
  async downloadDocument(id, nombreArchivo) {
    try {
      const response = await apiClient.get(`/documentos/${id}/download`, {
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
      console.error('Error al descargar documento:', error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de documentos
   */
  async getStatistics() {
    try {
      const response = await apiClient.get('/documentos/stats/summary')
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  },

  /**
   * Buscar documentos
   */
  async searchDocuments(query) {
    try {
      const response = await apiClient.get('/documentos/search', {
        params: { q: query }
      })
      return response.data
    } catch (error) {
      console.error('Error al buscar documentos:', error)
      throw error
    }
  }
}

export default documentService