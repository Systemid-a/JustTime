<!-- ============================================================ -->
<!-- PÁGINA: TemplatesPage.vue CORREGIDO -->
<!-- Compatible con tu estructura de backend actual -->
<!-- ============================================================ -->

<template>
  <div class="min-h-screen bg-gray-50">
    
    <!-- ✅ NOTIFICACIÓN VISUAL (Reemplaza alert()) -->
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
            <FileText class="h-8 w-8 text-indigo-600" />
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Plantillas de Documentos</h1>
              <p class="text-sm text-gray-500 mt-1">Gestión de plantillas Word (.docx) reutilizables</p>
            </div>
          </div>
          <button
            @click="openUploadModal"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-sm"
          >
            <Plus class="h-5 w-5 mr-2" />
            Nueva Plantilla
          </button>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Filtros -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Categoría</label>
            <select
              v-model="filtroCategoria"
              @change="aplicarFiltros"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">Todas las categorías</option>
              <option value="contrato">Contrato</option>
              <option value="demanda">Demanda</option>
              <option value="escritura">Escritura</option>
              <option value="poder">Poder</option>
              <option value="memorial">Memorial</option>
              <option value="dictamen">Dictamen</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
            <div class="relative">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                v-model="searchTerm"
                type="text"
                placeholder="Buscar por nombre..."
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Estado</label>
            <select
              v-model="soloActivas"
              @change="aplicarFiltros"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option :value="true">Solo activas</option>
              <option :value="false">Todas</option>
            </select>
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
            <FileText class="h-10 w-10 text-indigo-500" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Activas</p>
              <p class="text-2xl font-bold text-green-600">{{ estadisticas.activas || 0 }}</p>
            </div>
            <CheckCircle class="h-10 w-10 text-green-500" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Inactivas</p>
              <p class="text-2xl font-bold text-gray-600">{{ estadisticas.inactivas || 0 }}</p>
            </div>
            <XCircle class="h-10 w-10 text-gray-400" />
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Categorías</p>
              <p class="text-2xl font-bold text-indigo-600">{{ Object.keys(estadisticas.por_categoria || {}).length }}</p>
            </div>
            <FolderOpen class="h-10 w-10 text-indigo-500" />
          </div>
        </div>
      </div>

      <!-- Tabla de Plantillas -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        
        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <Loader2 class="h-8 w-8 text-indigo-600 animate-spin" />
          <span class="ml-3 text-gray-600">Cargando plantillas...</span>
        </div>

        <!-- Sin resultados -->
        <div v-else-if="plantillasFiltradas.length === 0" class="text-center py-12">
          <FileText class="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p class="text-lg font-medium text-gray-900 mb-2">No hay plantillas</p>
          <p class="text-gray-600 mb-4">Comienza subiendo tu primera plantilla</p>
          <button
            @click="openUploadModal"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg"
          >
            <Plus class="h-5 w-5 mr-2" />
            Subir Primera Plantilla
          </button>
        </div>

        <!-- Tabla -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Archivo</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Categoría</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="plantilla in plantillasFiltradas" :key="plantilla.id_plantilla" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <div class="flex items-center">
                    <FileText class="h-5 w-5 text-indigo-500 mr-3" />
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ plantilla.nombre }}</div>
                      <div v-if="plantilla.descripcion" class="text-xs text-gray-500">{{ plantilla.descripcion }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">{{ plantilla.nombre_archivo }}</td>
                <td class="px-6 py-4">
                  <span 
                    :class="getCategoriaColor(plantilla.categoria)"
                    class="px-3 py-1 inline-flex text-xs font-semibold rounded-full"
                  >
                    {{ getCategoriaLabel(plantilla.categoria) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-600">{{ formatearFecha(plantilla.fecha_subida) }}</td>
                <td class="px-6 py-4">
                  <span 
                    :class="plantilla.activo ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
                    class="px-2 py-1 inline-flex text-xs font-semibold rounded-full"
                  >
                    {{ plantilla.activo ? 'Activa' : 'Inactiva' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <!-- Botón Descargar -->
                    <button
                      @click="descargarPlantilla(plantilla)"
                      class="text-blue-600 hover:text-blue-900 p-2 hover:bg-blue-50 rounded transition-colors"
                      title="Descargar plantilla"
                    >
                      <Download class="h-5 w-5" />
                    </button>
                    
                    <!-- ✅ BOTÓN ELIMINAR (NUEVO) -->
                    <button
                      @click="confirmarEliminar(plantilla)"
                      class="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded transition-colors"
                      title="Eliminar plantilla"
                    >
                      <Trash2 class="h-5 w-5" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ✅ MODAL DE CONFIRMACIÓN PARA ELIMINAR -->
    <Modal
      :isOpen="showDeleteModal"
      title="¿Eliminar plantilla?"
      size="sm"
      @close="cancelarEliminar"
    >
      <div class="space-y-4">
        <div class="flex items-start gap-3 p-4 bg-red-50 rounded-lg">
          <AlertCircle class="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p class="text-sm text-red-900 font-medium">
              Esta acción no se puede deshacer
            </p>
            <p class="text-sm text-red-700 mt-1">
              La plantilla <span class="font-semibold">"{{ plantillaAEliminar?.nombre }}"</span> será eliminada permanentemente.
            </p>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <button
            @click="cancelarEliminar"
            :disabled="eliminando"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            @click="eliminarPlantilla"
            :disabled="eliminando"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <Loader2 v-if="eliminando" class="h-4 w-4 animate-spin" />
            <Trash2 v-else class="h-4 w-4" />
            {{ eliminando ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Modal Upload -->
    <TemplateUploader
      v-if="showUploadModal"
      @close="closeUploadModal"
      @uploaded="onTemplateUploaded"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  FileText, Plus, Search, Download, CheckCircle, XCircle, 
  FolderOpen, Loader2, Trash2, AlertCircle, X
} from 'lucide-vue-next'
import templateService from '@/services/templateService'
import TemplateUploader from '@/components/templates/TemplateUploader.vue'
import Modal from '@/components/shared/Modal.vue'

// ============= ESTADO =============
const plantillas = ref([])
const estadisticas = ref({
  total: 0,
  activas: 0,
  inactivas: 0,
  por_categoria: {}
})
const loading = ref(false)
const eliminando = ref(false)
const searchTerm = ref('')
const filtroCategoria = ref('')
const soloActivas = ref(true)
const showUploadModal = ref(false)
const showDeleteModal = ref(false)
const plantillaAEliminar = ref(null)

// ✅ ESTADO DE NOTIFICACIONES
const notification = ref({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

// ============= COMPUTED =============
const plantillasFiltradas = computed(() => {
  let resultado = plantillas.value

  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    resultado = resultado.filter(p => 
      p.nombre.toLowerCase().includes(term) ||
      p.nombre_archivo.toLowerCase().includes(term) ||
      (p.descripcion && p.descripcion.toLowerCase().includes(term))
    )
  }

  return resultado
})

// ============= MÉTODOS DE NOTIFICACIÓN =============
const showNotification = (type, title, message) => {
  notification.value = {
    show: true,
    type,
    title,
    message
  }
  
  // Auto-ocultar después de 4 segundos
  setTimeout(() => {
    hideNotification()
  }, 4000)
}

const hideNotification = () => {
  notification.value.show = false
}

// ============= MÉTODOS CRUD =============
const cargarPlantillas = async () => {
  loading.value = true
  try {
    const params = {
      solo_activas: soloActivas.value
    }

    if (filtroCategoria.value) {
      params.categoria = filtroCategoria.value
    }

    const response = await templateService.getTemplates(params)
    
    // ✅ COMPATIBLE CON TU ESTRUCTURA DE BACKEND
    if (response.success) {
      plantillas.value = response.data.templates || []
      estadisticas.value = response.data.estadisticas || {}
    }
  } catch (error) {
    console.error('Error al cargar plantillas:', error)
    showNotification('error', 'Error', 'No se pudieron cargar las plantillas')
  } finally {
    loading.value = false
  }
}

const aplicarFiltros = () => {
  cargarPlantillas()
}

const descargarPlantilla = async (plantilla) => {
  try {
    await templateService.downloadTemplate(
      plantilla.id_plantilla, 
      plantilla.nombre_archivo
    )
    // ✅ Notificación visual (reemplaza alert)
    showNotification('success', '¡Descargada!', `Plantilla "${plantilla.nombre}" descargada exitosamente`)
  } catch (error) {
    console.error('Error al descargar:', error)
    showNotification('error', 'Error', 'No se pudo descargar la plantilla')
  }
}

// ✅ MÉTODOS PARA ELIMINAR (NUEVOS)
const confirmarEliminar = (plantilla) => {
  plantillaAEliminar.value = plantilla
  showDeleteModal.value = true
}

const cancelarEliminar = () => {
  showDeleteModal.value = false
  plantillaAEliminar.value = null
}

const eliminarPlantilla = async () => {
  if (!plantillaAEliminar.value) return

  eliminando.value = true
  try {
    await templateService.deleteTemplate(plantillaAEliminar.value.id_plantilla)
    
    // ✅ Notificación de éxito
    showNotification(
      'success',
      '¡Eliminada!',
      `Plantilla "${plantillaAEliminar.value.nombre}" eliminada exitosamente`
    )
    
    // Cerrar modal y recargar
    showDeleteModal.value = false
    plantillaAEliminar.value = null
    await cargarPlantillas()
  } catch (error) {
    console.error('Error al eliminar:', error)
    showNotification('error', 'Error', 'No se pudo eliminar la plantilla')
  } finally {
    eliminando.value = false
  }
}

const openUploadModal = () => {
  showUploadModal.value = true
}

const closeUploadModal = () => {
  showUploadModal.value = false
}

const onTemplateUploaded = (newTemplate) => {
  closeUploadModal()
  cargarPlantillas()
  // ✅ Notificación visual (reemplaza alert)
  showNotification('success', '¡Éxito!', `Plantilla "${newTemplate.nombre}" subida correctamente`)
}

// ============= HELPERS =============
const getCategoriaColor = (categoria) => {
  const colores = {
    'contrato': 'bg-blue-100 text-blue-800',
    'demanda': 'bg-red-100 text-red-800',
    'escritura': 'bg-green-100 text-green-800',
    'poder': 'bg-purple-100 text-purple-800',
    'memorial': 'bg-yellow-100 text-yellow-800',
    'dictamen': 'bg-indigo-100 text-indigo-800',
    'otro': 'bg-gray-100 text-gray-800'
  }
  return colores[categoria] || 'bg-gray-100 text-gray-800'
}

const getCategoriaLabel = (categoria) => {
  const labels = {
    'contrato': 'Contrato',
    'demanda': 'Demanda',
    'escritura': 'Escritura',
    'poder': 'Poder',
    'memorial': 'Memorial',
    'dictamen': 'Dictamen',
    'otro': 'Otro'
  }
  return labels[categoria] || categoria || 'Sin categoría'
}

const formatearFecha = (fecha) => {
  if (!fecha) return '-'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// ============= LIFECYCLE =============
onMounted(() => {
  cargarPlantillas()
})
</script>

<style scoped>
/* Animación para notificaciones */
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
