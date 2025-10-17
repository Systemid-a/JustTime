<template>
  <div
    class="bg-white border-2 rounded-xl p-5 cursor-pointer hover:shadow-lg hover:-translate-y-1 transition-all duration-200 relative group"
    :class="borderColorClass"
    @click="handleCardClick"
  >
    <button
      @click.stop="showDeleteConfirm = true"
      class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 z-10"
      title="Eliminar proyecto"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
      </svg>
    </button>

    <div class="flex items-start justify-between mb-3">
      <span class="text-xs font-semibold px-3 py-1 rounded-full text-white" :class="categoryColorClass">
        {{ categoryLabel }}
      </span>
      <span class="flex items-center gap-1 text-sm font-medium" :class="statusColorClass">
        <span class="w-2 h-2 rounded-full" :class="statusDotClass"></span>
        {{ statusLabel }}
      </span>
    </div>

    <h3 class="text-lg font-bold text-gray-800 mb-2 line-clamp-2 min-h-[3.5rem]">
      {{ project.nombre }}
    </h3>

    <p v-if="project.descripcion" class="text-sm text-gray-600 mb-4 line-clamp-3 min-h-[3.75rem]">
      {{ project.descripcion }}
    </p>
    <div v-else class="mb-4 min-h-[3.75rem] flex items-center">
      <p class="text-sm text-gray-400 italic">Sin descripción</p>
    </div>

    <div class="border-t border-gray-200 mb-4"></div>

    <div class="space-y-2">
      <div class="flex items-center gap-2 text-sm text-gray-700">
        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
        <span class="font-medium">{{ taskCount }} {{ taskCount === 1 ? 'tarea' : 'tareas' }}</span>
      </div>

      <div v-if="project.cliente" class="flex items-center gap-2 text-sm text-gray-700">
        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span class="truncate">{{ project.cliente }}</span>
      </div>

      <div v-if="project.fecha_inicio" class="flex items-center gap-2 text-sm text-gray-700">
        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ formatDate(project.fecha_inicio) }}</span>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        @click.self="showDeleteConfirm = false"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div class="flex items-start gap-4 mb-4">
            <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 mb-1">¿Eliminar proyecto?</h3>
              <p class="text-sm text-gray-600">
                Estás a punto de eliminar "<strong>{{ project.nombre }}</strong>". Esta acción no se puede deshacer.
              </p>
            </div>
          </div>

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
import { useProjectStore } from '@/stores/projectStore'

const projectStore = useProjectStore()

const props = defineProps({
  project: { type: Object, required: true }
})

const emit = defineEmits(['click', 'deleted'])

const showDeleteConfirm = ref(false)
const isDeleting = ref(false)

const taskCount = computed(() => props.project.tareas_count || 0)

const borderColorClass = computed(() => {
  const categoria = props.project.categoria_nombre?.toLowerCase() || props.project.categoria?.toLowerCase()
  const colors = {
    civil: 'border-blue-200 hover:border-blue-400',
    penal: 'border-red-200 hover:border-red-400',
    laboral: 'border-green-200 hover:border-green-400',
    comercial: 'border-yellow-200 hover:border-yellow-400',
    familia: 'border-purple-200 hover:border-purple-400'
  }
  return colors[categoria] || 'border-gray-200 hover:border-gray-400'
})

const categoryColorClass = computed(() => {
  const categoria = props.project.categoria_nombre?.toLowerCase() || props.project.categoria?.toLowerCase()
  const colors = {
    civil: 'bg-blue-500',
    penal: 'bg-red-500',
    laboral: 'bg-green-500',
    comercial: 'bg-yellow-500',
    familia: 'bg-purple-500'
  }
  return colors[categoria] || 'bg-gray-500'
})

const categoryLabel = computed(() => {
  const categoria = props.project.categoria_nombre?.toLowerCase() || props.project.categoria?.toLowerCase()
  const labels = {
    civil: 'Civil',
    penal: 'Penal',
    laboral: 'Laboral',
    comercial: 'Comercial',
    familia: 'Familia'
  }
  return labels[categoria] || 'Sin categoría'
})

const statusColorClass = computed(() => {
  const estado = props.project.estado?.toLowerCase()
  const colors = {
    activo: 'text-green-600',
    pausado: 'text-yellow-600',
    finalizado: 'text-gray-600'
  }
  return colors[estado] || 'text-gray-600'
})

const statusDotClass = computed(() => {
  const estado = props.project.estado?.toLowerCase()
  const colors = {
    activo: 'bg-green-500',
    pausado: 'bg-yellow-500',
    finalizado: 'bg-gray-500'
  }
  return colors[estado] || 'bg-gray-500'
})

const statusLabel = computed(() => {
  const estado = props.project.estado?.toLowerCase()
  const labels = {
    activo: 'Activo',
    pausado: 'Pausado',
    finalizado: 'Finalizado'
  }
  return labels[estado] || 'Desconocido'
})

function handleCardClick() {
  if (!showDeleteConfirm.value) {
    emit('click', props.project)
  }
}

async function handleDelete() {
  if (isDeleting.value) return
  
  isDeleting.value = true
  
  try {
    await projectStore.deleteProject(props.project.id_proyecto)
    showDeleteConfirm.value = false
    emit('deleted', props.project.id_proyecto)
  } catch (error) {
    alert('No se pudo eliminar el proyecto.')
  } finally {
    isDeleting.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return 'Sin fecha'
  
  try {
    const date = new Date(dateString)
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`
  } catch (error) {
    return 'Fecha inválida'
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>