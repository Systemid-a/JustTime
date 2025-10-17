<!-- ============================================================ -->
<!-- ARCHIVO 3/31: src/components/tasks/TaskKanban.vue -->
<!-- Módulo: Tareas -->
<!-- Descripción: Tablero Kanban completo con drag & drop -->
<!-- ✅ CORREGIDO: Líneas 38 y 91 - 'progreso' → 'en_progreso' -->
<!-- ============================================================ -->

<template>
  <div class="h-full">
    <!-- Loading overlay -->
    <div
      v-if="isUpdating"
      class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 shadow-xl">
        <div class="flex items-center gap-3">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="text-gray-700 font-medium">Actualizando tarea...</span>
        </div>
      </div>
    </div>

    <!-- Grid de 3 columnas -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 h-full">
      <!-- Columna NUEVO -->
      <TaskColumn
        title="Nuevo"
        :tasks="nuevoTasks"
        status="nuevo"
        color="blue"
        @task-dropped="handleTaskDropped"
        @edit-task="$emit('edit-task', $event)"
      />

      <!-- Columna EN PROGRESO -->
      <TaskColumn
        title="En Progreso"
        :tasks="enProgresoTasks"
        status="en_progreso"
        color="yellow"
        @task-dropped="handleTaskDropped"
        @edit-task="$emit('edit-task', $event)"
      />

      <!-- Columna FINALIZADO -->
      <TaskColumn
        title="Finalizado"
        :tasks="finalizadoTasks"
        status="finalizado"
        color="green"
        @task-dropped="handleTaskDropped"
        @edit-task="$emit('edit-task', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TaskColumn from './TaskColumn.vue'
import { useTaskStore } from '@/stores/taskStore'

// ============= PROPS =============
const props = defineProps({
  tasks: {
    type: Array,
    required: true,
    default: () => []
  }
})

// ============= EMITS =============
const emit = defineEmits(['task-updated', 'edit-task'])

// ============= STATE =============
const isUpdating = ref(false)
const taskStore = useTaskStore()

// ============= COMPUTED =============

/**
 * Tareas en estado NUEVO
 */
const nuevoTasks = computed(() => {
  return props.tasks.filter(task => task.estado === 'nuevo')
})

/**
 * Tareas en estado EN PROGRESO
 * ✅ CORREGIDO: Cambió de 'progreso' a 'en_progreso'
 */
const enProgresoTasks = computed(() => {
  return props.tasks.filter(task => task.estado === 'en_progreso')
})

/**
 * Tareas en estado FINALIZADO
 */
const finalizadoTasks = computed(() => {
  return props.tasks.filter(task => task.estado === 'finalizado')
})

// ============= MÉTODOS =============

/**
 * Manejar cuando una tarea es soltada en una nueva columna
 */
async function handleTaskDropped(event) {
  const { taskId, newStatus, task } = event
  
  // Si el estado no cambió, no hacer nada
  if (task.estado === newStatus) {
    return
  }
  
  isUpdating.value = true
  
  try {
    // Actualizar estado usando el store
    await taskStore.updateTaskStatus(taskId, newStatus)
    
    // Emitir evento para que el padre actualice la lista
    emit('task-updated', {
      taskId,
      newStatus,
      message: 'Tarea actualizada correctamente'
    })
    
    // Mostrar notificación de éxito
    showToast('Tarea movida correctamente', 'success')
  } catch (error) {
    console.error('Error al actualizar tarea:', error)
    
    // Mostrar error al usuario
    showToast('Error al mover la tarea. Intenta nuevamente.', 'error')
    
    // Emitir evento de error para que el padre pueda revertir si es necesario
    emit('task-updated', {
      taskId,
      error: true,
      message: error.message
    })
  } finally {
    isUpdating.value = false
  }
}

/**
 * Mostrar notificación toast (implementación simple)
 */
function showToast(message, type = 'info') {
  // Crear elemento toast
  const toast = document.createElement('div')
  toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white z-50 transition-opacity duration-300 ${
    type === 'success' ? 'bg-green-500' : 
    type === 'error' ? 'bg-red-500' : 
    'bg-blue-500'
  }`
  toast.textContent = message
  
  document.body.appendChild(toast)
  
  // Remover después de 3 segundos
  setTimeout(() => {
    toast.style.opacity = '0'
    setTimeout(() => {
      document.body.removeChild(toast)
    }, 300)
  }, 3000)
}
</script>

<style scoped>
/* Animación de loading */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>