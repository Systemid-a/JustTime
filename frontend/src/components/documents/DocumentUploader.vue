<!-- ============================================================ -->
<!-- COMPONENTE: DocumentUploader.vue - VERSIÓN FINAL -->
<!-- Dropdown dinámico con proyectos desde /api/projects/ -->
<!-- ============================================================ -->

<template>
  <div class="p-6">
    <form @submit.prevent="subirDocumento">
      
      <!-- Drag & Drop Zone -->
      <div
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        :class="[
          'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
          isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300',
          selectedFile ? 'bg-green-50 border-green-500' : ''
        ]"
      >
        <input
          ref="fileInput"
          type="file"
          @change="handleFileSelect"
          class="hidden"
          accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.gif,.webp,.xls,.xlsx,.csv,.txt,.rtf,.zip,.rar"
        />

        <!-- Sin archivo -->
        <div v-if="!selectedFile">
          <Upload class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p class="text-lg font-medium text-gray-900 mb-2">Arrastra tu archivo aquí</p>
          <p class="text-sm text-gray-600 mb-4">o haz click para seleccionar</p>
          <button
            type="button"
            @click="$refs.fileInput.click()"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg"
          >
            <FileText class="h-4 w-4 mr-2" />
            Seleccionar Archivo
          </button>
          
          <div class="mt-6 pt-6 border-t border-gray-200">
            <p class="text-xs font-medium text-gray-700 mb-2">Tipos soportados:</p>
            <div class="flex flex-wrap gap-2 justify-center">
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">PDF</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">Word</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">Excel</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">Imágenes</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">ZIP</span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">+9 más</span>
            </div>
          </div>
        </div>

        <!-- Con archivo -->
        <div v-else class="text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <CheckCircle class="h-8 w-8 text-green-600" />
          </div>
          <p class="text-lg font-medium text-gray-900 mb-1">{{ selectedFile.name }}</p>
          <p class="text-sm text-gray-600 mb-4">{{ formatFileSize(selectedFile.size) }} - {{ getFileType(selectedFile.name) }}</p>
          <button type="button" @click="removeFile" class="text-sm text-red-600 hover:text-red-700 font-medium">
            <X class="h-4 w-4 inline mr-1" />
            Remover archivo
          </button>
        </div>
      </div>

      <!-- Error -->
      <div v-if="validationError" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-start">
          <AlertTriangle class="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error de validación</h3>
            <p class="text-sm text-red-700 mt-1">{{ validationError }}</p>
          </div>
        </div>
      </div>

      <!-- Info -->
      <div v-if="selectedFile && !validationError" class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div class="flex items-start">
          <Info class="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div class="ml-3">
            <h3 class="text-sm font-medium text-blue-800">Información del archivo</h3>
            <ul class="text-sm text-blue-700 mt-1 space-y-1">
              <li>• Tamaño: {{ formatFileSize(selectedFile.size) }}</li>
              <li>• Tipo: {{ getFileCategory(selectedFile.name) }}</li>
              <li>• Máximo: {{ getMaxSize(selectedFile.name) }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Dropdown Proyecto -->
      <div class="mt-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Proyecto (Opcional)</label>
        
        <div v-if="loadingProyectos" class="flex items-center text-sm text-gray-500 py-2">
          <Loader2 class="h-4 w-4 animate-spin mr-2" />
          Cargando proyectos...
        </div>
        
        <select
          v-else
          v-model="formData.proyecto_id"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Sin proyecto</option>
          <option 
            v-for="proyecto in proyectos" 
            :key="proyecto.id_proyecto" 
            :value="proyecto.id_proyecto"
          >
            {{ proyecto.nombre }}
          </option>
        </select>
        
        <p class="text-xs text-gray-500 mt-1">
          {{ proyectos.length > 0 ? `${proyectos.length} proyectos disponibles` : 'Vincula a un proyecto' }}
        </p>
      </div>

      <!-- Botones -->
      <div class="mt-6 flex gap-3">
        <button
          type="button"
          @click="$emit('cancel')"
          :disabled="uploading"
          class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="!selectedFile || uploading || !!validationError"
          class="flex-1 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg disabled:opacity-50"
        >
          <Loader2 v-if="uploading" class="h-4 w-4 animate-spin inline mr-2" />
          {{ uploading ? 'Subiendo...' : 'Subir Documento' }}
        </button>
      </div>

      <!-- Progreso -->
      <div v-if="uploading" class="mt-4">
        <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
          <span>Subiendo...</span>
          <span>{{ uploadProgress }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div :style="{ width: uploadProgress + '%' }" class="bg-indigo-600 h-2 rounded-full transition-all"></div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Upload, FileText, CheckCircle, X, AlertTriangle, Info, Loader2 } from 'lucide-vue-next'
import documentService from '@/services/documentService'
import projectService from '@/services/projectService'
import { useAuthStore } from '@/stores/authStore'

const emit = defineEmits(['uploaded', 'cancel'])
const authStore = useAuthStore()

const fileInput = ref(null)
const selectedFile = ref(null)
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const validationError = ref('')
const proyectos = ref([])
const loadingProyectos = ref(false)

const formData = ref({
  proyecto_id: '',
  subido_por: authStore.user?.id_usuario || null
})

// Cargar proyectos
const cargarProyectos = async () => {
  loadingProyectos.value = true
  try {
    const response = await projectService.getProjects()
    
    if (response.success && response.data) {
      if (response.data.proyectos) {
        proyectos.value = response.data.proyectos
      } else if (Array.isArray(response.data)) {
        proyectos.value = response.data
      }
    } else if (Array.isArray(response)) {
      proyectos.value = response
    }
    
    console.log(`✅ ${proyectos.value.length} proyectos cargados`)
  } catch (error) {
    console.error('❌ Error al cargar proyectos:', error)
  } finally {
    loadingProyectos.value = false
  }
}

// Validación
watch(selectedFile, (newFile) => {
  if (newFile) validateFile(newFile)
})

const validateFile = (file) => {
  validationError.value = ''
  
  const allowed = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'xls', 'xlsx', 'csv', 'txt', 'rtf', 'zip', 'rar']
  const ext = file.name.split('.').pop().toLowerCase()
  
  if (!allowed.includes(ext)) {
    validationError.value = `Tipo no permitido`
    return false
  }
  
  const maxSizes = {
    'pdf': 10, 'doc': 10, 'docx': 10,
    'jpg': 5, 'jpeg': 5, 'png': 5, 'gif': 5, 'webp': 5,
    'xls': 15, 'xlsx': 15, 'csv': 15,
    'txt': 2, 'rtf': 2,
    'zip': 50, 'rar': 50
  }
  
  const maxMB = maxSizes[ext] || 10
  const maxBytes = maxMB * 1024 * 1024
  
  if (file.size > maxBytes) {
    validationError.value = `Archivo muy grande. Máximo: ${maxMB}MB`
    return false
  }
  
  return true
}

const handleFileSelect = (e) => {
  if (e.target.files[0]) selectedFile.value = e.target.files[0]
}

const handleDrop = (e) => {
  isDragging.value = false
  if (e.dataTransfer.files[0]) selectedFile.value = e.dataTransfer.files[0]
}

const removeFile = () => {
  selectedFile.value = null
  validationError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

const subirDocumento = async () => {
  if (!selectedFile.value || validationError.value) return
  
  uploading.value = true
  uploadProgress.value = 0
  
  try {
    const interval = setInterval(() => {
      if (uploadProgress.value < 90) uploadProgress.value += 10
    }, 200)
    
    const metadata = {
      proyecto_id: formData.value.proyecto_id || null,
      subido_por: formData.value.subido_por
    }
    
    const response = await documentService.uploadDocument(metadata, selectedFile.value)
    
    clearInterval(interval)
    uploadProgress.value = 100
    
    if (response.success) {
      emit('uploaded', response.data)
      removeFile()
      formData.value.proyecto_id = ''
    } else {
      validationError.value = response.message || 'Error al subir'
    }
  } catch (error) {
    validationError.value = error.response?.data?.detail || 'Error al subir'
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const getFileType = (filename) => filename.split('.').pop().toUpperCase()

const getFileCategory = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  if (['pdf', 'doc', 'docx'].includes(ext)) return 'Documento'
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return 'Imagen'
  if (['xls', 'xlsx', 'csv'].includes(ext)) return 'Hoja de Cálculo'
  if (['txt', 'rtf'].includes(ext)) return 'Texto'
  if (['zip', 'rar'].includes(ext)) return 'Comprimido'
  return 'Otro'
}

const getMaxSize = (filename) => {
  const ext = filename.split('.').pop().toLowerCase()
  const sizes = {
    'pdf': '10 MB', 'doc': '10 MB', 'docx': '10 MB',
    'jpg': '5 MB', 'jpeg': '5 MB', 'png': '5 MB', 'gif': '5 MB', 'webp': '5 MB',
    'xls': '15 MB', 'xlsx': '15 MB', 'csv': '15 MB',
    'txt': '2 MB', 'rtf': '2 MB',
    'zip': '50 MB', 'rar': '50 MB'
  }
  return sizes[ext] || '10 MB'
}

onMounted(() => cargarProyectos())
</script>