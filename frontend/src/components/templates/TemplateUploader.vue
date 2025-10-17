<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="p-2 bg-indigo-100 rounded-lg">
            <Upload class="h-6 w-6 text-indigo-600" />
          </div>
          <div>
            <h2 class="text-xl font-bold text-gray-900">Subir Nueva Plantilla</h2>
            <p class="text-sm text-gray-500">Archivos .docx - Máximo 5MB</p>
          </div>
        </div>
        <button
          @click="cerrarModal"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X class="h-6 w-6" />
        </button>
      </div>

      <!-- Contenido -->
      <div class="p-6">
        <form @submit.prevent="subirPlantilla">
          
          <!-- Zona de Drag & Drop -->
          <div
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200',
              dragOver ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 bg-gray-50',
              archivoSeleccionado ? 'border-green-500 bg-green-50' : ''
            ]"
          >
            <!-- Sin archivo seleccionado -->
            <div v-if="!archivoSeleccionado" class="space-y-4">
              <div class="flex justify-center">
                <FileText class="h-16 w-16 text-gray-400" />
              </div>
              <div>
                <p class="text-lg font-medium text-gray-700">
                  Arrastra tu archivo .docx aquí
                </p>
                <p class="text-sm text-gray-500 mt-1">o haz clic para seleccionar</p>
              </div>
              <input
                ref="fileInput"
                type="file"
                accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                @change="handleFileSelect"
                class="hidden"
              />
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="inline-flex items-center px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                <FolderOpen class="h-5 w-5 mr-2" />
                Seleccionar Archivo
              </button>
              <div class="text-xs text-gray-500">
                Solo archivos .docx - Tamaño máximo: 5MB
              </div>
            </div>

            <!-- Archivo seleccionado -->
            <div v-else class="space-y-4">
              <div class="flex items-center justify-center">
                <div class="p-3 bg-green-100 rounded-full">
                  <FileCheck class="h-12 w-12 text-green-600" />
                </div>
              </div>
              <div>
                <p class="text-lg font-medium text-gray-900">{{ archivoSeleccionado.name }}</p>
                <p class="text-sm text-gray-500 mt-1">
                  {{ formatFileSize(archivoSeleccionado.size) }}
                </p>
              </div>
              <button
                type="button"
                @click="removerArchivo"
                class="inline-flex items-center px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100"
              >
                <X class="h-4 w-4 mr-1" />
                Remover archivo
              </button>
            </div>

            <!-- Error de validación -->
            <div v-if="errorArchivo" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-center text-red-800">
                <AlertCircle class="h-5 w-5 mr-2" />
                <span class="text-sm font-medium">{{ errorArchivo }}</span>
              </div>
            </div>
          </div>

          <!-- Formulario de Metadatos -->
          <div class="mt-6 space-y-4">
            
            <!-- Nombre de la Plantilla -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nombre de la Plantilla <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formData.nombre"
                type="text"
                required
                placeholder="Ej: Contrato de Compraventa de Inmuebles"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :class="{ 'border-red-500': errorNombre }"
              />
              <p v-if="errorNombre" class="mt-1 text-sm text-red-600">{{ errorNombre }}</p>
            </div>

            <!-- Categoría -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Categoría Jurídica
              </label>
              <select
                v-model="formData.categoria"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Seleccionar categoría (opcional)</option>
                <option value="contrato">Contrato</option>
                <option value="demanda">Demanda</option>
                <option value="escritura">Escritura</option>
                <option value="poder">Poder</option>
                <option value="memorial">Memorial</option>
                <option value="dictamen">Dictamen</option>
                <option value="otro">Otro</option>
              </select>
            </div>

            <!-- Descripción -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                v-model="formData.descripcion"
                rows="3"
                placeholder="Descripción opcional de la plantilla..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
              ></textarea>
              <p class="mt-1 text-xs text-gray-500">
                {{ formData.descripcion ? formData.descripcion.length : 0 }} / 1000 caracteres
              </p>
            </div>
          </div>

          <!-- Botones de Acción -->
          <div class="mt-6 flex items-center justify-end space-x-3 pt-6 border-t border-gray-200">
            <button
              type="button"
              @click="cerrarModal"
              :disabled="uploading"
              class="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="!archivoSeleccionado || uploading || !formData.nombre"
              class="inline-flex items-center px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Loader2 v-if="uploading" class="h-5 w-5 mr-2 animate-spin" />
              <Upload v-else class="h-5 w-5 mr-2" />
              {{ uploading ? 'Subiendo...' : 'Subir Plantilla' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { 
  Upload, X, FileText, FolderOpen, FileCheck, AlertCircle, Loader2 
} from 'lucide-vue-next'
import templateService from '@/services/templateService'

// ============= EMITS =============
const emit = defineEmits(['close', 'template-uploaded'])

// ============= ESTADO =============
const archivoSeleccionado = ref(null)
const dragOver = ref(false)
const uploading = ref(false)
const errorArchivo = ref('')
const errorNombre = ref('')

const formData = reactive({
  nombre: '',
  categoria: '',
  descripcion: ''
})

const fileInput = ref(null)

// ============= CONSTANTES =============
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB en bytes
const ALLOWED_EXTENSIONS = ['.docx']
const ALLOWED_MIME_TYPES = [
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

// ============= MÉTODOS =============

/**
 * Validar archivo
 */
const validarArchivo = (file) => {
  // Validar extensión
  const fileName = file.name.toLowerCase()
  const hasValidExtension = ALLOWED_EXTENSIONS.some(ext => fileName.endsWith(ext))
  
  if (!hasValidExtension) {
    errorArchivo.value = 'Solo se permiten archivos .docx'
    return false
  }

  // Validar tipo MIME
  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    errorArchivo.value = 'Tipo de archivo no válido. Solo archivos Word (.docx)'
    return false
  }

  // Validar tamaño
  if (file.size > MAX_FILE_SIZE) {
    errorArchivo.value = `El archivo es muy grande. Máximo ${formatFileSize(MAX_FILE_SIZE)}`
    return false
  }

  errorArchivo.value = ''
  return true
}

/**
 * Manejar selección de archivo (input)
 */
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && validarArchivo(file)) {
    archivoSeleccionado.value = file
    
    // Auto-llenar nombre si está vacío
    if (!formData.nombre) {
      formData.nombre = file.name.replace('.docx', '').replace(/[_-]/g, ' ')
    }
  }
}

/**
 * Manejar drop de archivo (drag & drop)
 */
const handleDrop = (event) => {
  dragOver.value = false
  
  const files = event.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    if (validarArchivo(file)) {
      archivoSeleccionado.value = file
      
      // Auto-llenar nombre si está vacío
      if (!formData.nombre) {
        formData.nombre = file.name.replace('.docx', '').replace(/[_-]/g, ' ')
      }
    }
  }
}

/**
 * Remover archivo seleccionado
 */
const removerArchivo = () => {
  archivoSeleccionado.value = null
  errorArchivo.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

/**
 * Formatear tamaño de archivo
 */
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Validar formulario
 */
const validarFormulario = () => {
  let isValid = true

  // Validar nombre
  if (!formData.nombre || formData.nombre.trim().length < 3) {
    errorNombre.value = 'El nombre debe tener al menos 3 caracteres'
    isValid = false
  } else {
    errorNombre.value = ''
  }

  // Validar archivo
  if (!archivoSeleccionado.value) {
    errorArchivo.value = 'Debes seleccionar un archivo .docx'
    isValid = false
  }

  return isValid
}

/**
 * Subir plantilla al backend
 */
const subirPlantilla = async () => {
  // Validar formulario
  if (!validarFormulario()) {
    return
  }

  uploading.value = true

  try {
    const response = await templateService.uploadTemplate(
      {
        nombre: formData.nombre.trim(),
        categoria: formData.categoria || null,
        descripcion: formData.descripcion.trim() || null
      },
      archivoSeleccionado.value
    )

    if (response.success) {
      emit('template-uploaded', response.data)
    }
  } catch (error) {
    console.error('Error al subir plantilla:', error)
    
    // Mostrar error al usuario
    const errorMessage = error.response?.data?.detail || 'Error al subir la plantilla'
    errorArchivo.value = errorMessage
  } finally {
    uploading.value = false
  }
}

/**
 * Cerrar modal
 */
const cerrarModal = () => {
  if (!uploading.value) {
    emit('close')
  }
}
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>