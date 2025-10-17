<!-- ============================================================ -->
<!-- ARCHIVO 5/31: src/components/tasks/TaskCard.vue -->
<!-- Módulo: Tareas -->
<!-- Descripción: Tarjeta individual de tarea para tablero Kanban -->
<!-- ✨ ACTUALIZADO: Botón de eliminar agregado -->
<!-- ============================================================ -->

<template>
  <div
    class="bg-white border border-gray-200 rounded-lg p-4 cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow duration-200 relative group"
    @click="handleCardClick"
  >
    <!-- Botón de eliminar (aparece al hacer hover) -->
    <button
      @click.stop="showDeleteConfirm = true"
      class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-1.5 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 hover:text-red-700"
      title="Eliminar tarea"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
      </svg>
    </button>

    <!-- Título de la tarea -->
    <h4 class="font-semibold text-gray-800 mb-2 line-clamp-2 pr-8">
      {{ task.titulo }}
    </h4>

    <!-- Descripción (máximo 2 líneas) -->
    <p v-if="task.descripcion" class="text-sm text-gray-600 mb-3 line-clamp-2">
      {{ task.descripcion }}
    </p>

    <!-- Separador -->
    <div class="border-t border-gray-100 mb-3"></div>

    <!-- Información adicional -->
    <div class="space-y-2">
      <!-- Prioridad y Proyecto en una fila -->
      <div class="flex items-center justify-between gap-2">
        <!-- Badge de prioridad -->
        <span :class="priorityClasses" class="text-xs font-medium px-2 py-1 rounded-full">
          {{ priorityLabel }}
        </span>

        <!-- Nombre del proyecto (si existe) -->
        <span v-if="task.proyecto_nombre" class="text-xs text-gray-500 flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
          </svg>
          {{ truncateText(task.proyecto_nombre, 15) }}
        </span>
      </div>

      <!-- Fecha de vencimiento -->
      <div v-if="task.fecha_vencimiento" class="flex items-center gap-1 text-xs text-gray-500">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span :class="{ 'text-red-600 font-medium': isOverdue }">
          {{ formatDate(task.fecha_vencimiento) }}
        </span>
      </div>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        @click.self="showDeleteConfirm = false"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6 animate-fade-in">
          <!-- Encabezado -->
          <div class="flex items-start gap-4 mb-4">
            <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 mb-1">
                ¿Eliminar tarea?
              </h3>
              <p class="text-sm text-gray-600">
                Estás a punto de eliminar "<strong>{{ task.titulo }}</strong>". Esta acción no se puede deshacer.
              </p>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex gap-3 justify-end">
            <button
              @click="showDeleteConfirm = false"
              :disabled="isDeleting"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              @click="handleDelete"
              :disabled="isDeleting"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg v-if="isDeleting" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isDeleting ? 'Eliminando...' : 'Eliminar' }}</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useTaskStore } from '@/stores/taskStore'

// ============= STORES =============
const taskStore = useTaskStore()

// ============= PROPS =============
const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

// ============= EMITS =============
const emit = defineEmits(['click', 'deleted'])

// ============= STATE =============
const showDeleteConfirm = ref(false)
const isDeleting = ref(false)

// ============= COMPUTED =============

/**
 * Clases CSS para el badge de prioridad
 */
const priorityClasses = computed(() => {
  const prioridad = props.task.prioridad?.toLowerCase()
  
  switch (prioridad) {
    case 'alta':
      return 'bg-red-100 text-red-700'
    case 'media':
      return 'bg-yellow-100 text-yellow-700'
    case 'baja':
      return 'bg-blue-100 text-blue-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
})

/**
 * Etiqueta de prioridad en español
 */
const priorityLabel = computed(() => {
  const prioridad = props.task.prioridad?.toLowerCase()
  
  switch (prioridad) {
    case 'alta':
      return '🔴 Alta'
    case 'media':
      return '🟡 Media'
    case 'baja':
      return '🔵 Baja'
    default:
      return 'Sin prioridad'
  }
})

/**
 * Verificar si la tarea está vencida
 */
const isOverdue = computed(() => {
  if (!props.task.fecha_vencimiento) return false
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const dueDate = new Date(props.task.fecha_vencimiento)
  dueDate.setHours(0, 0, 0, 0)
  
  return dueDate < today && props.task.estado !== 'finalizado'
})

// ============= MÉTODOS =============

/**
 * Manejar click en la tarjeta (evitar que se active al hacer click en el botón de eliminar)
 */
function handleCardClick() {
  if (!showDeleteConfirm.value) {
    emit('click', props.task)
  }
}

/**
 * Manejar eliminación de tarea
 */
async function handleDelete() {
  if (isDeleting.value) return
  
  isDeleting.value = true
  
  try {
    await taskStore.deleteTask(props.task.id_tarea)
    
    // Cerrar modal
    showDeleteConfirm.value = false
    
    // Emitir evento de tarea eliminada
    emit('deleted', props.task.id_tarea)
    
    // Opcional: Mostrar notificación de éxito
    console.log('✅ Tarea eliminada exitosamente')
  } catch (error) {
    console.error('❌ Error al eliminar tarea:', error)
    alert('No se pudo eliminar la tarea. Por favor, intenta de nuevo.')
  } finally {
    isDeleting.value = false
  }
}

/**
 * Formatear fecha a formato legible
 */
function formatDate(dateString) {
  if (!dateString) return 'Sin fecha'
  
  const date = new Date(dateString)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  const dateOnly = new Date(date)
  dateOnly.setHours(0, 0, 0, 0)
  
  // Si es hoy
  if (dateOnly.getTime() === today.getTime()) {
    return 'Hoy'
  }
  
  // Si es mañana
  if (dateOnly.getTime() === tomorrow.getTime()) {
    return 'Mañana'
  }
  
  // Formato normal: DD MMM
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  return `${date.getDate()} ${months[date.getMonth()]}`
}

/**
 * Truncar texto largo
 */
function truncateText(text, maxLength) {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<style scoped>
/* Limitar texto a 2 líneas */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animación de aparición del modal */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>