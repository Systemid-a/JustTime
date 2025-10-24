// ============================================================
// ARCHIVO: src/services/documentService.js - CORREGIDO
// Módulo: Services
// Descripción: Servicio para gestión de documentos (NO plantillas)
// ============================================================

import apiClient from './api'

/**
 * Servicio de Documentos
 * Gestión completa de documentos del sistema (14 tipos de archivos)
 */
const documentService = {
  
  /**
   * Subir nuevo documento
   * @param {Object} metadata - Metadatos del documento
   * @param {File} file - Archivo a subir
   */
  async uploadDocument(metadata, file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      // Solo agregar campos que el backend de documentos espera
      if (metadata.proyecto_id) {
        formData.append('proyecto_id', metadata.proyecto_id)
      }
      
      if (metadata.subido_por) {
        formData.append('subido_por', metadata.subido_por)
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
   * Obtener todos los documentos con filtros opcionales
   */
  async getDocuments(params = {}) {
    try {
      const response = await apiClient.get('/documentos/', { params })
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
   * Buscar documentos por nombre
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
  },

  /**
   * Obtener documentos de un proyecto específico
   */
  async getDocumentsByProject(proyectoId) {
    try {
      const response = await apiClient.get(`/documentos/proyecto/${proyectoId}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener documentos del proyecto:', error)
      throw error
    }
  },

  /**
   * Obtener documentos por tipo de archivo
   */
  async getDocumentsByType(tipoArchivo) {
    try {
      const response = await apiClient.get(`/documentos/tipo/${tipoArchivo}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener documentos por tipo:', error)
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
  async deleteDocument(id, deleteFile = true) {
    try {
      const response = await apiClient.delete(`/documentos/${id}`, {
        params: { delete_file: deleteFile }
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
  }
}

export default documentService