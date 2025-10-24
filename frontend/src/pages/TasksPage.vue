<!-- ============================================================ -->
<!-- ARCHIVO 16/31: src/pages/TasksPage.vue -->
<!-- Módulo: Páginas -->
<!-- Descripción: Vista principal de gestión de tareas con Kanban -->
<!-- ============================================================ -->

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Gestión de Tareas</h2>
          <p class="text-sm text-gray-500 mt-1">
            Organiza y gestiona tus tareas con el tablero Kanban
          </p>
        </div>
        <button
          @click="openNewTaskModal"
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Tarea
        </button>
      </div>

      <!-- Toggle Vista y Filtros -->
      <div class="flex flex-col md:flex-row md:items-center gap-4">
        <!-- Toggle Kanban/Lista -->
        <div class="flex bg-gray-100 rounded-lg p-1">
          <button
            @click="view = 'kanban'"
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              view === 'kanban' 
                ? 'bg-white text-blue-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            <span class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Kanban
            </span>
          </button>
          <button
            @click="view = 'lista'"
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              view === 'lista' 
                ? 'bg-white text-blue-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            <span class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
              Lista
            </span>
          </button>
        </div>

        <!-- Filtros -->
        <div class="flex flex-1 gap-3">
          <!-- Filtro por Proyecto -->
          <select
            v-model="filterProject"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los proyectos</option>
            <option
              v-for="proyecto in projects"
              :key="proyecto.id_proyecto"
              :value="proyecto.id_proyecto"
            >
              {{ proyecto.nombre }}
            </option>
          </select>

          <!-- Filtro por Estado -->
          <select
            v-model="filterStatus"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="nuevo">Nuevo</option>
            <option value="progreso">En Progreso</option>
            <option value="finalizado">Finalizado</option>
          </select>

          <!-- Búsqueda -->
          <div class="flex-1 max-w-md relative">
            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar tarea..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="flex-1 overflow-hidden p-6 bg-gray-50">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Cargando tareas...</p>
        </div>
      </div>

      <!-- Vista Kanban -->
      <TaskKanban
        v-else-if="view === 'kanban'"
        :tasks="filteredTasks"
        @task-updated="handleTaskUpdated"
        @edit-task="openEditTaskModal"
      />

      <!-- Vista Lista -->
      <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Título
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Proyecto
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Prioridad
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Vencimiento
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="task in filteredTasks"
              :key="task.id_tarea"
              class="hover:bg-gray-50 cursor-pointer"
              @click="openEditTaskModal(task)"
            >
              <td class="px-6 py-4">
                <div class="text-sm font-medium text-gray-900">{{ task.titulo }}</div>
                <div class="text-sm text-gray-500 truncate max-w-xs">{{ task.descripcion }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ task.proyecto_nombre || 'Sin proyecto' }}
              </td>
              <td class="px-6 py-4">
                <span :class="getStatusBadgeClass(task.estado)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ getStatusLabel(task.estado) }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span :class="getPriorityBadgeClass(task.prioridad)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ getPriorityLabel(task.prioridad) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ formatDate(task.fecha_vencimiento) }}
              </td>
              <td class="px-6 py-4 text-right text-sm font-medium">
                <button
                  @click.stop="openEditTaskModal(task)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Editar
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="filteredTasks.length === 0" class="text-center py-12">
          <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-gray-500">No se encontraron tareas</p>
        </div>
      </div>
    </div>

    <!-- Modal para crear/editar tarea -->
    <Modal
      :isOpen="showModal"
      :title="modalTitle"
      size="lg"
      @close="closeModal"
    >
      <TaskForm
        :task="selectedTask"
        @save="handleSaveTask"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import TaskKanban from '@/components/tasks/TaskKanban.vue'
import TaskForm from '@/components/tasks/TaskForm.vue'
import Modal from '@/components/shared/Modal.vue'
import apiClient from '@/services/api'

// ============= STORES =============
const taskStore = useTaskStore()

// ============= STATE =============
const view = ref('kanban') // 'kanban' o 'lista'
const loading = ref(false)
const showModal = ref(false)
const selectedTask = ref(null)
const projects = ref([])

// Filtros
const filterProject = ref('')
const filterStatus = ref('')
const searchQuery = ref('')

// ============= COMPUTED =============

/**
 * Tareas filtradas según criterios
 */
const filteredTasks = computed(() => {
  let tasks = taskStore.tasks

  // Filtrar por proyecto
  if (filterProject.value) {
    tasks = tasks.filter(t => t.proyecto_id_fk === filterProject.value)
  }

  // Filtrar por estado
  if (filterStatus.value) {
    tasks = tasks.filter(t => t.estado === filterStatus.value)
  }

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    tasks = tasks.filter(t =>
      t.titulo.toLowerCase().includes(query) ||
      t.descripcion?.toLowerCase().includes(query)
    )
  }

  return tasks
})

/**
 * Título del modal según el modo
 */
const modalTitle = computed(() => {
  return selectedTask.value ? 'Editar Tarea' : 'Nueva Tarea'
})

// ============= MÉTODOS =============

/**
 * Cargar tareas desde el store
 */
async function loadTasks() {
  loading.value = true
  try {
    await taskStore.fetchTasks()
  } catch (error) {
    console.error('Error al cargar tareas:', error)
  } finally {
    loading.value = false
  }
}

/**
 * Cargar proyectos para filtros
 */
async function loadProjects() {
  try {
    const response = await apiClient.get('/projects/')
    if (response.data.success && response.data.data) {
      projects.value = response.data.data
    }
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
  }
}

/**
 * Abrir modal para nueva tarea
 */
function openNewTaskModal() {
  selectedTask.value = null
  showModal.value = true
}

/**
 * Abrir modal para editar tarea
 */
function openEditTaskModal(task) {
  selectedTask.value = task
  showModal.value = true
}

/**
 * Cerrar modal
 */
function closeModal() {
  showModal.value = false
  selectedTask.value = null
}

/**
 * Guardar tarea (crear o actualizar)
 */
async function handleSaveTask(taskData) {
  closeModal()
  await loadTasks() // Recargar lista de tareas
}

/**
 * Manejar actualización de tarea desde Kanban
 */
async function handleTaskUpdated(event) {
  if (!event.error) {
    await loadTasks()
  }
}

/**
 * Obtener clase CSS para badge de estado
 */
function getStatusBadgeClass(status) {
  const classes = {
    'nuevo': 'bg-blue-100 text-blue-700',
    'progreso': 'bg-yellow-100 text-yellow-700',
    'finalizado': 'bg-green-100 text-green-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}

/**
 * Obtener etiqueta de estado
 */
function getStatusLabel(status) {
  const labels = {
    'nuevo': 'Nuevo',
    'progreso': 'En Progreso',
    'finalizado': 'Finalizado'
  }
  return labels[status] || status
}

/**
 * Obtener clase CSS para badge de prioridad
 */
function getPriorityBadgeClass(priority) {
  const classes = {
    'alta': 'bg-red-100 text-red-700',
    'media': 'bg-yellow-100 text-yellow-700',
    'baja': 'bg-blue-100 text-blue-700'
  }
  return classes[priority] || 'bg-gray-100 text-gray-700'
}

/**
 * Obtener etiqueta de prioridad
 */
function getPriorityLabel(priority) {
  const labels = {
    'alta': 'Alta',
    'media': 'Media',
    'baja': 'Baja'
  }
  return labels[priority] || priority
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
  if (!dateString) return 'Sin fecha'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-GT', { day: '2-digit', month: 'short', year: 'numeric' })
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadTasks()
  loadProjects()
})
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>