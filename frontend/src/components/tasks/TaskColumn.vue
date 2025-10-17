<!-- ============================================================ -->
<!-- ARCHIVO 4/31: src/components/tasks/TaskColumn.vue -->
<!-- Módulo: Tareas -->
<!-- Descripción: Columna individual del tablero Kanban con drag & drop -->
<!-- ============================================================ -->

<template>
  <div class="flex flex-col bg-gray-50 rounded-lg h-full">
    <!-- Header de la columna -->
    <div 
      class="flex items-center justify-between px-4 py-3 border-b-4 rounded-t-lg"
      :class="borderColorClass"
    >
      <h3 class="font-semibold text-gray-800 text-lg">
        {{ title }}
      </h3>
      <span 
        class="bg-white text-gray-700 font-bold text-sm px-3 py-1 rounded-full border border-gray-300"
      >
        {{ tasks.length }}
      </span>
    </div>

    <!-- Área de drop con VueDraggable -->
    <VueDraggable
      v-model="localTasks"
      :group="{ name: 'tasks' }"
      :animation="200"
      ghost-class="ghost-card"
      drag-class="drag-card"
      class="flex-1 p-3 space-y-3 overflow-y-auto min-h-[200px]"
      @change="handleDrop"
    >
      <TaskCard
        v-for="task in localTasks"
        :key="task.id_tarea"
        :task="task"
        :data-task-id="task.id_tarea"
        @click="$emit('edit-task', task)"
      />
    </VueDraggable>

    <!-- Mensaje cuando no hay tareas -->
    <div
      v-if="tasks.length === 0"
      class="flex-1 flex items-center justify-center p-6 text-center"
    >
      <div class="text-gray-400">
        <svg class="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <p class="text-sm">No hay tareas</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import TaskCard from './TaskCard.vue'

// ============= PROPS =============
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  tasks: {
    type: Array,
    required: true,
    default: () => []
  },
  status: {
    type: String,
    required: true,
    validator: (value) => ['nuevo', 'progreso', 'finalizado'].includes(value)
  },
  color: {
    type: String,
    required: true
  }
})

// ============= EMITS =============
const emit = defineEmits(['update:tasks', 'task-dropped', 'edit-task'])

// ============= COMPUTED =============

/**
 * Modelo local para el v-model de VueDraggable
 */
const localTasks = computed({
  get() {
    return props.tasks
  },
  set(value) {
    emit('update:tasks', value)
  }
})

/**
 * Clase de color del borde superior según el estado
 */
const borderColorClass = computed(() => {
  const colorMap = {
    'nuevo': 'border-blue-500 bg-blue-50',
    'en_progreso': 'border-yellow-500 bg-yellow-50',
    'finalizado': 'border-green-500 bg-green-50'
  }
  return colorMap[props.status] || 'border-gray-500 bg-gray-50'
})

// ============= MÉTODOS =============

/**
 * Manejar cuando una tarea es soltada en esta columna
 */
function handleDrop(event) {
  // El evento 'change' de VueDraggable nos dice qué cambió
  if (event.added) {
    // Una tarea fue agregada a esta columna desde otra
    const task = event.added.element
    const newStatus = props.status
    
    emit('task-dropped', {
      taskId: task.id_tarea,
      newStatus: newStatus,
      task: task
    })
  }
}
</script>

<style scoped>
/* Estilos para el ghost (preview) durante el drag */
.ghost-card {
  opacity: 0.5;
  background: #e5e7eb;
  border: 2px dashed #9ca3af;
}

/* Estilos para la card mientras se está arrastrando */
.drag-card {
  opacity: 0.8;
  transform: rotate(3deg);
  cursor: grabbing;
}

/* Scroll personalizado */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>