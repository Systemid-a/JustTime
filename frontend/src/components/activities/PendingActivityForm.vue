<!-- ============================================================ -->
<!-- ARCHIVO: src/components/activities/PendingActivityForm.vue -->
<!-- Módulo: Actividades Pendientes -->
<!-- Descripción: Formulario para crear y editar actividades -->
<!-- ============================================================ -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <!-- Descripción -->
    <div class="form-group">
      <label for="descripcion" class="block text-sm font-medium text-gray-700 mb-1">
        Descripción <span class="text-red-500">*</span>
      </label>
      <textarea
        id="descripcion"
        v-model="formData.descripcion"
        rows="3"
        required
        maxlength="1000"
        placeholder="Describe la actividad o recordatorio..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all"
        :class="{ 'border-red-500': errors.descripcion }"
      ></textarea>
      <div class="flex justify-between items-center mt-1">
        <span v-if="errors.descripcion" class="text-red-500 text-sm">
          {{ errors.descripcion }}
        </span>
        <span class="text-xs text-gray-500 ml-auto">
          {{ formData.descripcion?.length || 0 }} / 1000 caracteres
        </span>
      </div>
    </div>

    <!-- Usuario Asignado -->
    <div class="form-group">
      <label for="usuario" class="block text-sm font-medium text-gray-700 mb-1">
        Usuario Asignado <span class="text-red-500">*</span>
      </label>
      <select
        id="usuario"
        v-model="formData.usuario_id_fk"
        required
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      >
        <option :value="null" disabled>Selecciona un usuario</option>
        <option
          v-for="usuario in usuarios"
          :key="usuario.id_usuario"
          :value="usuario.id_usuario"
        >
          {{ usuario.nombre }}
        </option>
      </select>
    </div>

    <!-- Proyecto (Opcional) -->
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
          v-for="proyecto in proyectos"
          :key="proyecto.id_proyecto"
          :value="proyecto.id_proyecto"
        >
          {{ proyecto.nombre }}
        </option>
      </select>
    </div>

    <!-- Fecha de Vencimiento y Prioridad (Grid 2 columnas) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Fecha de Vencimiento -->
      <div class="form-group">
        <label for="fecha" class="block text-sm font-medium text-gray-700 mb-1">
          Fecha de Vencimiento
        </label>
        <input
          id="fecha"
          v-model="formData.fecha_vencimiento"
          type="datetime-local"
          :min="minDateTime"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
        <p class="text-xs text-gray-500 mt-1">
          Opcional - Deja vacío si no tiene fecha límite
        </p>
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
          <option value="baja">🔵 Baja</option>
          <option value="media">🟡 Media</option>
          <option value="alta">🔴 Alta</option>
        </select>
      </div>
    </div>

    <!-- Estado Completada (Solo en modo edición) -->
    <div v-if="isEditMode" class="form-group">
      <label class="flex items-center gap-3 cursor-pointer">
        <input
          type="checkbox"
          v-model="formData.completada"
          class="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-2 focus:ring-green-500"
        />
        <span class="text-sm font-medium text-gray-700">
          Marcar como completada
        </span>
      </label>
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
        <span>{{ loading ? 'Guardando...' : (isEditMode ? 'Actualizar' : 'Crear Actividad') }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import apiClient from '@/services/api'

// ============= PROPS =============
const props = defineProps({
  activity: {
    type: Object,
    default: null
  }
})

// ============= EMITS =============
const emit = defineEmits(['save', 'cancel'])

// ============= STATE =============
const loading = ref(false)
const proyectos = ref([])
const usuarios = ref([])
const errors = reactive({
  descripcion: ''
})

const formData = reactive({
  descripcion: '',
  usuario_id_fk: null,
  proyecto_id_fk: null,
  fecha_vencimiento: '',
  prioridad: 'media',
  completada: false
})

// ============= COMPUTED =============

/**
 * Determinar si es modo edición o creación
 */
const isEditMode = computed(() => {
  return !!props.activity
})

/**
 * Validar si el formulario es válido
 */
const isFormValid = computed(() => {
  return formData.descripcion.trim().length >= 3 &&
         formData.usuario_id_fk !== null &&
         formData.prioridad
})

/**
 * Fecha y hora mínima (ahora)
 */
const minDateTime = computed(() => {
  const now = new Date()
  // Formato: YYYY-MM-DDTHH:MM
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}`
})

// ============= MÉTODOS =============

/**
 * Cargar proyectos activos para el select
 */
async function loadProyectos() {
  try {
    const response = await apiClient.get('/projects/')
    if (response.data.success && response.data.data) {
      // Filtrar solo proyectos activos
      proyectos.value = response.data.data.filter(p => p.estado === 'activo')
    }
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
  }
}

/**
 * Cargar usuarios para el select
 */
async function loadUsuarios() {
  try {
    const response = await apiClient.get('/auth/users')
    if (response.data.success && response.data.data) {
      usuarios.value = response.data.data
    }
  } catch (error) {
    console.error('Error al cargar usuarios:', error)
    // Si falla, crear usuario mock con el usuario actual
    usuarios.value = [
      { id_usuario: 1, nombre: 'Usuario Actual' }
    ]
  }
}

/**
 * Inicializar formulario con datos de actividad (si es edición)
 */
function initializeForm() {
  if (props.activity) {
    formData.descripcion = props.activity.descripcion || ''
    formData.usuario_id_fk = props.activity.usuario_id_fk || null
    formData.proyecto_id_fk = props.activity.proyecto_id_fk || null
    formData.prioridad = props.activity.prioridad || 'media'
    formData.completada = props.activity.completada || false
    
    // Formatear fecha para datetime-local
    if (props.activity.fecha_vencimiento) {
      const date = new Date(props.activity.fecha_vencimiento)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      
      formData.fecha_vencimiento = `${year}-${month}-${day}T${hours}:${minutes}`
    }
  } else {
    // Modo creación: establecer usuario actual si está disponible
    if (usuarios.value.length > 0) {
      formData.usuario_id_fk = usuarios.value[0].id_usuario
    }
  }
}

/**
 * Validar formulario
 */
function validateForm() {
  errors.descripcion = ''
  
  if (formData.descripcion.trim().length < 3) {
    errors.descripcion = 'La descripción debe tener al menos 3 caracteres'
    return false
  }
  
  if (formData.descripcion.trim().length > 1000) {
    errors.descripcion = 'La descripción no puede superar los 1000 caracteres'
    return false
  }
  
  if (!formData.usuario_id_fk) {
    alert('Debes seleccionar un usuario')
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
      descripcion: formData.descripcion.trim(),
      usuario_id_fk: formData.usuario_id_fk,
      proyecto_id_fk: formData.proyecto_id_fk || null,
      prioridad: formData.prioridad,
      completada: formData.completada
    }
    
    // Convertir fecha de datetime-local a ISO string
    if (formData.fecha_vencimiento) {
      const dateTime = new Date(formData.fecha_vencimiento)
      dataToSend.fecha_vencimiento = dateTime.toISOString()
    } else {
      dataToSend.fecha_vencimiento = null
    }
    
    let response
    
    if (isEditMode.value) {
      // Actualizar actividad existente
      response = await apiClient.put(
        `/pending-activities/${props.activity.id_actividad_pendiente}`,
        dataToSend
      )
    } else {
      // Crear nueva actividad
      response = await apiClient.post('/pending-activities/', dataToSend)
    }
    
    if (response.data.success) {
      emit('save', response.data.data)
    } else {
      throw new Error(response.data.message || 'Error al guardar actividad')
    }
  } catch (error) {
    console.error('Error al guardar actividad:', error)
    alert('Error al guardar la actividad. Por favor, intenta nuevamente.')
  } finally {
    loading.value = false
  }
}

// ============= LIFECYCLE =============
onMounted(async () => {
  await loadUsuarios()
  await loadProyectos()
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