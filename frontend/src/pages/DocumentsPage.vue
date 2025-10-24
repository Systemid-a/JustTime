<!-- ============================================================ -->
<!-- PÁGINA: DocumentsPage.vue COMPLETA -->
<!-- Módulo: Documentos -->
<!-- Descripción: Página principal de gestión de documentos -->
<!-- ============================================================ -->

<template>
  <div class="min-h-screen bg-gray-50">
    
    <!-- Notificación Visual -->
    <Transition name="notification">
      <div
        v-if="notification.show"
        :class="[
          'fixed top-4 right-4 z-50 max-w-md w-full px-6 py-4 rounded-lg shadow-lg border-l-4',
          'flex items-start gap-3',
          notification.type === 'success' ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'
        ]"
      >
        <CheckCircle v-if="notification.type === 'success'" class="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
        <XCircle v-else class="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
        
        <div class="flex-1">
          <h3 :class="notification.type === 'success' ? 'text-green-900' : 'text-red-900'" class="font-semibold">
            {{ notification.title }}
          </h3>
          <p :class="notification.type === 'success' ? 'text-green-700' : 'text-red-700'" class="text-sm mt-1">
            {{ notification.message }}
          </p>
        </div>
        
        <button
          @click="hideNotification"
          :class="notification.type === 'success' ? 'text-green-500 hover:text-green-700' : 'text-red-500 hover:text-red-700'"
          class="flex-shrink-0"
        >
          <X class="w-5 h-5" />
        </button>
      </div>
    </Transition>

    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <FolderOpen class="h-8 w-8 text-indigo-600" />
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Gestión de Documentos</h1>
              <p class="text-sm text-gray-500 mt-1">Archivos vinculados a proyectos (14 tipos soportados)</p>
            </div>
          </div>
          <button
            @click="openUploadModal"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-sm"
          >
            <Upload class="h-5 w-5 mr-2" />
            Subir Documento
          </button>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Filtros -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
            <div class="relative">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                v-model="searchTerm"
                @input="buscarDocumentos"
                type="text"
                placeholder="Buscar por nombre..."
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Archivo</label>
            <select
              v-model="filtroTipo"
              @change="aplicarFiltros"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">Todos los tipos</option>
              <option value="pdf">PDF</option>
              <option value="docx">Word</option>
              <option value="jpg">JPG</option>
              <option value="png">PNG</option>
              <option value="xlsx">Excel</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Proyecto</label>
            <select
              v-model="filtroProyecto"
              @change="aplicarFiltros"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">Todos los proyectos</option>
              <option value="sin_proyecto">Sin proyecto</option>
            </select>
          </div>

          <div class="flex items-end">
            <button
              @click="limpiarFiltros"
              class="w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <RotateCcw class="h-4 w-4 inline mr-2" />
              Limpiar
            </button>
          </div>
        </div>
      </div>

      <!-- Estadísticas -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total</p>
              <p class="text-2xl font-bold text-gray-900">{{ estadisticas.total || 0 }}</p>
            </div>
            <FolderOpen class="h-10 w-10 text-indigo-500" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Con Proyecto</p>
              <p class="text-2xl font-bold text-green-600">{{ estadisticas.con_proyecto || 0 }}</p>
            </div>
            <CheckCircle class="h-10 w-10 text-green-500" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Sin Proyecto</p>
              <p class="text-2xl font-bold text-gray-600">{{ estadisticas.sin_proyecto || 0 }}</p>
            </div>
            <FileText class="h-10 w-10 text-gray-400" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Tipos</p>
              <p class="text-2xl font-bold text-indigo-600">{{ Object.keys(estadisticas.por_tipo || {}).length }}</p>
            </div>
            <File class="h-10 w-10 text-indigo-500" />
          </div>
        </div>
      </div>

      <!-- Tabla de Documentos -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        
        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <Loader2 class="h-8 w-8 text-indigo-600 animate-spin" />
          <span class="ml-3 text-gray-600">Cargando documentos...</span>
        </div>

        <!-- Sin resultados -->
        <div v-else-if="documentos.length === 0" class="text-center py-12">
          <FolderOpen class="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p class="text-lg font-medium text-gray-900 mb-2">No hay documentos</p>
          <p class="text-gray-600 mb-4">Comienza subiendo tu primer documento</p>
          <button
            @click="openUploadModal"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg"
          >
            <Upload class="h-5 w-5 mr-2" />
            Subir Primer Documento
          </button>
        </div>

        <!-- Tabla -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Archivo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Proyecto</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="documento in documentos" :key="documento.id_documento" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="flex items-center">
                    <FileText class="h-8 w-8 text-indigo-500 mr-3" />
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ documento.nombre_archivo }}</div>
                      <div class="text-xs text-gray-500">{{ getFileCategory(documento.tipo_archivo) }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                    {{ (documento.tipo_archivo || '').replace('.', '').toUpperCase() }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">
                  {{ documento.proyecto_id_fk ? `Proyecto #${documento.proyecto_id_fk}` : 'Sin proyecto' }}
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">{{ formatearFecha(documento.fecha_subida) }}</td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end space-x-2">
                    <button
                      @click="descargarDocumento(documento)"
                      class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                      title="Descargar"
                    >
                      <Download class="h-4 w-4" />
                    </button>
                    <button
                      @click="confirmarEliminar(documento)"
                      class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Eliminar"
                    >
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal de Upload -->
    <Modal :isOpen="showUploadModal" @close="closeUploadModal" title="Subir Documento">
      <DocumentUploader 
        @uploaded="onDocumentUploaded"
        @cancel="closeUploadModal"
      />
    </Modal>

    <!-- Modal de Confirmación -->
    <Modal :isOpen="showDeleteModal" @close="cancelarEliminar" title="Confirmar Eliminación">
      <div class="p-6">
        <div class="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
          <AlertTriangle class="w-6 h-6 text-red-600" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 text-center mb-2">
          ¿Eliminar documento?
        </h3>
        <p class="text-sm text-gray-600 text-center mb-6">
          ¿Estás seguro de eliminar "{{ documentoAEliminar?.nombre_archivo }}"?
          <br>
          <span class="font-semibold text-red-600">Esta acción no se puede deshacer.</span>
        </p>
        
        <div class="flex gap-3">
          <button
            @click="cancelarEliminar"
            :disabled="eliminando"
            class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            @click="eliminarDocumento"
            :disabled="eliminando"
            class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg disabled:opacity-50"
          >
            <Loader2 v-if="eliminando" class="h-4 w-4 animate-spin inline mr-2" />
            {{ eliminando ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  FolderOpen, Upload, Search, Download, Trash2, FileText, File,
  CheckCircle, XCircle, X, AlertTriangle, Loader2, RotateCcw
} from 'lucide-vue-next'

import documentService from '@/services/documentService'
import DocumentUploader from '@/components/documents/DocumentUploader.vue'
import Modal from '@/components/shared/Modal.vue'

// ============= ESTADO =============
const documentos = ref([])
const estadisticas = ref({
  total: 0,
  con_proyecto: 0,
  sin_proyecto: 0,
  por_tipo: {}
})
const loading = ref(false)
const eliminando = ref(false)
const searchTerm = ref('')
const filtroTipo = ref('')
const filtroProyecto = ref('')
const showUploadModal = ref(false)
const showDeleteModal = ref(false)
const documentoAEliminar = ref(null)

const notification = ref({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

// ============= MÉTODOS =============
const showNotification = (type, title, message) => {
  notification.value = { show: true, type, title, message }
  setTimeout(() => hideNotification(), 4000)
}

const hideNotification = () => {
  notification.value.show = false
}

const cargarDocumentos = async () => {
  loading.value = true
  try {
    const params = {}
    if (filtroTipo.value) params.tipo_archivo = filtroTipo.value
    if (filtroProyecto.value && filtroProyecto.value !== 'sin_proyecto') {
      params.proyecto_id = parseInt(filtroProyecto.value)
    }
    
    const response = await documentService.getDocuments(params)
    
    if (response.success) {
      documentos.value = response.data.documentos || []
      estadisticas.value = response.data.estadisticas || {}
    }
  } catch (error) {
    console.error('Error:', error)
    showNotification('error', 'Error', 'No se pudieron cargar los documentos')
  } finally {
    loading.value = false
  }
}

const buscarDocumentos = async () => {
  if (!searchTerm.value.trim()) {
    await cargarDocumentos()
    return
  }
  
  loading.value = true
  try {
    const response = await documentService.searchDocuments(searchTerm.value)
    if (response.success) {
      documentos.value = response.data.documentos || []
    }
  } catch (error) {
    showNotification('error', 'Error', 'No se pudo realizar la búsqueda')
  } finally {
    loading.value = false
  }
}

const aplicarFiltros = () => cargarDocumentos()

const limpiarFiltros = () => {
  searchTerm.value = ''
  filtroTipo.value = ''
  filtroProyecto.value = ''
  cargarDocumentos()
}

const descargarDocumento = async (documento) => {
  try {
    await documentService.downloadDocument(documento.id_documento, documento.nombre_archivo)
    showNotification('success', '¡Descargado!', `Documento "${documento.nombre_archivo}" descargado`)
  } catch (error) {
    showNotification('error', 'Error', 'No se pudo descargar el documento')
  }
}

const confirmarEliminar = (documento) => {
  documentoAEliminar.value = documento
  showDeleteModal.value = true
}

const cancelarEliminar = () => {
  showDeleteModal.value = false
  documentoAEliminar.value = null
}

const eliminarDocumento = async () => {
  if (!documentoAEliminar.value) return

  eliminando.value = true
  try {
    await documentService.deleteDocument(documentoAEliminar.value.id_documento, true)
    showNotification('success', '¡Eliminado!', `Documento eliminado exitosamente`)
    showDeleteModal.value = false
    documentoAEliminar.value = null
    await cargarDocumentos()
  } catch (error) {
    showNotification('error', 'Error', 'No se pudo eliminar el documento')
  } finally {
    eliminando.value = false
  }
}

const openUploadModal = () => showUploadModal.value = true
const closeUploadModal = () => showUploadModal.value = false

const onDocumentUploaded = (newDocument) => {
  closeUploadModal()
  cargarDocumentos()
  showNotification('success', '¡Éxito!', `Documento subido correctamente`)
}

const getFileCategory = (tipoArchivo) => {
  if (!tipoArchivo) return 'Otro'
  const tipo = tipoArchivo.toLowerCase().replace('.', '')
  if (['pdf', 'doc', 'docx'].includes(tipo)) return 'Documento'
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(tipo)) return 'Imagen'
  if (['xls', 'xlsx', 'csv'].includes(tipo)) return 'Hoja de Cálculo'
  return 'Otro'
}

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  cargarDocumentos()
})
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>