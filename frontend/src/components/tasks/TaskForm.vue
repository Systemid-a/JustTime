<!-- ============================================================ -->
<!-- ARCHIVO 6/31: src/components/tasks/TaskForm.vue -->
<!-- Módulo: Tareas -->
<!-- Descripción: Formulario para crear y editar tareas -->
<!-- ============================================================ -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <!-- Título -->
    <div class="form-group">
      <label for="titulo" class="block text-sm font-medium text-gray-700 mb-1">
        Título <span class="text-red-500">*</span>
      </label>
      <input
        id="titulo"
        v-model="formData.titulo"
        type="text"
        required
        maxlength="200"
        placeholder="Ej: Revisar expediente García"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        :class="{ 'border-red-500': errors.titulo }"
      />
      <span v-if="errors.titulo" class="text-red-500 text-sm mt-1 block">
        {{ errors.titulo }}
      </span>
    </div>

    <!-- Descripción -->
    <div class="form-group">
      <label for="descripcion" class="block text-sm font-medium text-gray-700 mb-1">
        Descripción
      </label>
      <textarea
        id="descripcion"
        v-model="formData.descripcion"
        rows="4"
        maxlength="1000"
        placeholder="Describe los detalles de la tarea..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all"
      ></textarea>
      <p class="text-xs text-gray-500 mt-1">
        {{ formData.descripcion?.length || 0 }} / 1000 caracteres
      </p>
    </div>

    <!-- Proyecto -->
    <div class="form-group">
      <label for="proyecto" class="block text-sm font-medium text-gray-700 mb-1">
        Proyecto
      </label>
      <select
        id="proyecto"
        v-model="formData.proyecto_id_fk"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      >
        <option :value="null">Sin proyecto asignado</option>
        <option
          v-for="proyecto in projects"
          :key="proyecto.id_proyecto"
          :value="proyecto.id_proyecto"
        >
          {{ proyecto.nombre }}
        </option>
      </select>
    </div>

    <!-- Estado y Prioridad (Grid 2 columnas) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Estado -->
      <div class="form-group">
        <label for="estado" class="block text-sm font-medium text-gray-700 mb-1">
          Estado <span class="text-red-500">*</span>
        </label>
        <select
          id="estado"
          v-model="formData.estado"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        >
          <option value="nuevo">Nuevo</option>
          <option value="en_progreso">En Progreso</option>
          <option value="finalizado">Finalizado</option>
        </select>
      </div>

      <!-- Prioridad -->
      <div class="form-group">
        <label for="prioridad" class="block text-sm font-medium text-gray-700 mb-1">
          Prioridad <span class="text-red-500">*</span>
        </label>
        <select
          id="prioridad"
          v-model="formData.prioridad"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        >
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
        </select>
      </div>
    </div>

    <!-- Fecha de Vencimiento -->
    <div class="form-group">
      <label for="fecha" class="block text-sm font-medium text-gray-700 mb-1">
        Fecha de Vencimiento
      </label>
      <input
        id="fecha"
        v-model="formData.fecha_vencimiento"
        type="date"
        :min="minDate"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      />
    </div>

    <!-- Botones de acción -->
    <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
      <button
        type="button"
        @click="$emit('cancel')"
        :disabled="loading"
        class="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Cancelar
      </button>
      <button
        type="submit"
        :disabled="loading || !isFormValid"
        class="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <svg v-if="loading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ loading ? 'Guardando...' : (isEditMode ? 'Actualizar' : 'Crear Tarea') }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/services/api'

// ============= PROPS =============
const props = defineProps({
  task: {
    type: Object,
    default: null
  }
})

// ============= EMITS =============
const emit = defineEmits(['save', 'cancel'])

// ============= STATE =============
const loading = ref(false)
const projects = ref([])
const errors = reactive({
  titulo: ''
})

const formData = reactive({
  titulo: '',
  descripcion: '',
  proyecto_id_fk: null,
  estado: 'nuevo',
  prioridad: 'media',
  fecha_vencimiento: ''
})

// ============= COMPUTED =============

/**
 * Determinar si es modo edición o creación
 */
const isEditMode = computed(() => {
  return !!props.task
})

/**
 * Validar si el formulario es válido
 */
const isFormValid = computed(() => {
  return formData.titulo.trim().length >= 3 &&
         formData.estado &&
         formData.prioridad
})

/**
 * Fecha mínima (hoy)
 */
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// ============= MÉTODOS =============

/**
 * Cargar proyectos activos para el select
 */
async function loadProjects() {
  try {
    const response = await apiClient.get('/projects/')
    if (response.data.success && response.data.data) {
      // Filtrar solo proyectos activos
      projects.value = response.data.data.filter(p => p.estado === 'activo')
    }
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
  }
}

/**
 * Inicializar formulario con datos de tarea (si es edición)
 */
function initializeForm() {
  if (props.task) {
    formData.titulo = props.task.titulo || ''
    formData.descripcion = props.task.descripcion || ''
    formData.proyecto_id_fk = props.task.proyecto_id_fk || null
    formData.estado = props.task.estado || 'nuevo'
    formData.prioridad = props.task.prioridad || 'media'
    formData.fecha_vencimiento = props.task.fecha_vencimiento 
      ? props.task.fecha_vencimiento.split('T')[0] 
      : ''
  }
}

/**
 * Validar formulario
 */
function validateForm() {
  errors.titulo = ''
  
  if (formData.titulo.trim().length < 3) {
    errors.titulo = 'El título debe tener al menos 3 caracteres'
    return false
  }
  
  if (formData.titulo.trim().length > 200) {
    errors.titulo = 'El título no puede superar los 200 caracteres'
    return false
  }
  
  return true
}

/**
 * Enviar formulario
 */
async function handleSubmit() {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  
  try {
    // Preparar datos para enviar
    const dataToSend = {
      titulo: formData.titulo.trim(),
      descripcion: formData.descripcion?.trim() || null,
      estado: formData.estado,
      prioridad: formData.prioridad,
      proyecto_id_fk: formData.proyecto_id_fk || null,
      fecha_vencimiento: formData.fecha_vencimiento || null
    }
    
    let response
    
    if (isEditMode.value) {
      // Actualizar tarea existente
      response = await apiClient.put(`/tasks/${props.task.id_tarea}`, dataToSend)
    } else {
      // Crear nueva tarea
      response = await apiClient.post('/tasks/', dataToSend)
    }
    
    if (response.data.success) {
      emit('save', response.data.data)
    } else {
      throw new Error(response.data.message || 'Error al guardar tarea')
    }
  } catch (error) {
    console.error('Error al guardar tarea:', error)
    alert('Error al guardar la tarea. Por favor, intenta nuevamente.')
  } finally {
    loading.value = false
  }
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadProjects()
  initializeForm()
})
</script>

<style scoped>
/* Animación de spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>