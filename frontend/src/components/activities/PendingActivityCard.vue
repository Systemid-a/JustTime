<!-- ============================================================ -->
<!-- ARCHIVO: src/components/activities/PendingActivityCard.vue -->
<!-- Módulo: Actividades Pendientes -->
<!-- Descripción: Tarjeta individual de actividad pendiente -->
<!-- ============================================================ -->

<template>
  <div
    class="bg-white border rounded-lg p-4 hover:shadow-md transition-all duration-200 relative group"
    :class="[
      activity.completada ? 'border-gray-200 opacity-75' : 'border-gray-300',
      isOverdue ? 'border-l-4 border-l-red-500' : '',
      activity.prioridad === 'alta' && !activity.completada ? 'border-l-4 border-l-orange-500' : ''
    ]"
  >
    <!-- Header con checkbox y botón eliminar -->
    <div class="flex items-start gap-3 mb-3">
      <!-- Checkbox para completar -->
      <button
        @click.stop="handleToggleComplete"
        class="flex-shrink-0 w-6 h-6 rounded border-2 flex items-center justify-center transition-all mt-0.5"
        :class="[
          activity.completada 
            ? 'bg-green-500 border-green-500' 
            : 'border-gray-300 hover:border-green-500'
        ]"
        :disabled="isUpdating"
      >
        <svg
          v-if="activity.completada"
          class="w-4 h-4 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </button>

      <!-- Descripción -->
      <div
        class="flex-1 cursor-pointer"
        @click="$emit('click', activity)"
      >
        <p
          class="text-gray-800 leading-snug"
          :class="{ 'line-through text-gray-500': activity.completada }"
        >
          {{ activity.descripcion }}
        </p>
      </div>

      <!-- Botón eliminar (aparece al hacer hover) -->
      <button
        @click.stop="showDeleteConfirm = true"
        class="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity p-1.5 rounded-lg bg-red-50 hover:bg-red-100 text-red-600"
        title="Eliminar actividad"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>

    <!-- Información adicional -->
    <div class="flex flex-wrap items-center gap-2 ml-9">
      <!-- Badge de prioridad -->
      <span
        v-if="!activity.completada"
        :class="priorityClasses"
        class="text-xs font-medium px-2 py-1 rounded-full"
      >
        {{ priorityLabel }}
      </span>

      <!-- Fecha de vencimiento -->
      <div
        v-if="activity.fecha_vencimiento"
        class="flex items-center gap-1 text-xs"
        :class="[
          isOverdue && !activity.completada ? 'text-red-600 font-medium' : 'text-gray-500'
        ]"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ formatDate(activity.fecha_vencimiento) }}</span>
      </div>

      <!-- Proyecto asociado -->
      <div
        v-if="activity.proyecto_nombre"
        class="flex items-center gap-1 text-xs text-gray-500"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <span class="truncate max-w-[150px]">{{ activity.proyecto_nombre }}</span>
      </div>

      <!-- Usuario asignado -->
      <div
        v-if="activity.usuario_nombre"
        class="flex items-center gap-1 text-xs text-gray-500"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>{{ activity.usuario_nombre }}</span>
      </div>
    </div>

    <!-- Indicador de vencida -->
    <div
      v-if="isOverdue && !activity.completada"
      class="mt-2 ml-9 flex items-center gap-1 text-xs text-red-600 font-medium"
    >
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>Vencida</span>
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
                ¿Eliminar actividad?
              </h3>
              <p class="text-sm text-gray-600">
                Esta acción no se puede deshacer.
              </p>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex gap-3 justify-end">
            <button
              @click="showDeleteConfirm = false"
              :disabled="isDeleting"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              @click="handleDelete"
              :disabled="isDeleting"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
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
import { usePendingActivityStore } from '@/stores/pendingActivityStore'

// ============= STORES =============
const activityStore = usePendingActivityStore()

// ============= PROPS =============
const props = defineProps({
  activity: {
    type: Object,
    required: true
  }
})

// ============= EMITS =============
const emit = defineEmits(['click', 'updated', 'deleted'])

// ============= STATE =============
const showDeleteConfirm = ref(false)
const isDeleting = ref(false)
const isUpdating = ref(false)

// ============= COMPUTED =============

/**
 * Clases CSS para el badge de prioridad
 */
const priorityClasses = computed(() => {
  const prioridad = props.activity.prioridad?.toLowerCase()
  
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
 * Etiqueta de prioridad
 */
const priorityLabel = computed(() => {
  const prioridad = props.activity.prioridad?.toLowerCase()
  
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
 * Verificar si la actividad está vencida
 */
const isOverdue = computed(() => {
  if (!props.activity.fecha_vencimiento || props.activity.completada) {
    return false
  }
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const dueDate = new Date(props.activity.fecha_vencimiento)
  dueDate.setHours(0, 0, 0, 0)
  
  return dueDate < today
})

// ============= MÉTODOS =============

/**
 * Manejar toggle de completada
 */
async function handleToggleComplete() {
  if (isUpdating.value) return
  
  isUpdating.value = true
  
  try {
    await activityStore.toggleCompletada(
      props.activity.id_actividad_pendiente,
      !props.activity.completada
    )
    
    emit('updated', props.activity.id_actividad_pendiente)
  } catch (error) {
    console.error('Error al actualizar actividad:', error)
    alert('No se pudo actualizar la actividad. Por favor, intenta de nuevo.')
  } finally {
    isUpdating.value = false
  }
}

/**
 * Manejar eliminación
 */
async function handleDelete() {
  if (isDeleting.value) return
  
  isDeleting.value = true
  
  try {
    await activityStore.deleteActivity(props.activity.id_actividad_pendiente)
    
    showDeleteConfirm.value = false
    emit('deleted', props.activity.id_actividad_pendiente)
    
    console.log('✅ Actividad eliminada exitosamente')
  } catch (error) {
    console.error('❌ Error al eliminar actividad:', error)
    alert('No se pudo eliminar la actividad. Por favor, intenta de nuevo.')
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
</script>

<style scoped>
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