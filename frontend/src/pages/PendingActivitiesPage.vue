<!-- ============================================================ -->
<!-- ARCHIVO: src/pages/PendingActivitiesPage.vue -->
<!-- Módulo: Páginas -->
<!-- Descripción: Vista principal de gestión de actividades pendientes -->
<!-- ============================================================ -->

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Actividades Pendientes</h2>
          <p class="text-sm text-gray-500 mt-1">
            Gestiona tus recordatorios y actividades por completar
          </p>
        </div>
        <button
          @click="openNewActivityModal"
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Actividad
        </button>
      </div>

      <!-- Estadísticas -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <!-- Total -->
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-medium text-blue-600 uppercase">Total</p>
              <p class="text-2xl font-bold text-blue-700 mt-1">
                {{ estadisticas.total }}
              </p>
            </div>
            <div class="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Pendientes -->
        <div class="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-4 border border-yellow-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-medium text-yellow-600 uppercase">Pendientes</p>
              <p class="text-2xl font-bold text-yellow-700 mt-1">
                {{ estadisticas.pendientes }}
              </p>
            </div>
            <div class="w-12 h-12 bg-yellow-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Completadas -->
        <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-medium text-green-600 uppercase">Completadas</p>
              <p class="text-2xl font-bold text-green-700 mt-1">
                {{ estadisticas.completadas }}
              </p>
            </div>
            <div class="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Vencidas -->
        <div class="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-4 border border-red-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-medium text-red-600 uppercase">Vencidas</p>
              <p class="text-2xl font-bold text-red-700 mt-1">
                {{ estadisticas.vencidas }}
              </p>
            </div>
            <div class="w-12 h-12 bg-red-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Porcentaje -->
        <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-medium text-purple-600 uppercase">Progreso</p>
              <p class="text-2xl font-bold text-purple-700 mt-1">
                {{ estadisticas.porcentajeCompletado }}%
              </p>
            </div>
            <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="flex-1 overflow-hidden bg-gray-50">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Cargando actividades...</p>
        </div>
      </div>

      <!-- Lista de Actividades -->
      <PendingActivityList
        v-else
        :activities="activities"
        :loading="loading"
        :proyectos="proyectos"
        @edit-activity="openEditActivityModal"
        @activity-updated="handleActivityUpdated"
        @activity-deleted="handleActivityDeleted"
      />
    </div>

    <!-- Modal para crear/editar actividad -->
    <Modal
      :isOpen="showModal"
      :title="modalTitle"
      size="lg"
      @close="closeModal"
    >
      <PendingActivityForm
        :activity="selectedActivity"
        @save="handleSaveActivity"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePendingActivityStore } from '@/stores/pendingActivityStore'
import PendingActivityList from '@/components/activities/PendingActivityList.vue'
import PendingActivityForm from '@/components/activities/PendingActivityForm.vue'
import Modal from '@/components/shared/Modal.vue'
import apiClient from '@/services/api'

// ============= STORES =============
const activityStore = usePendingActivityStore()

// ============= STATE =============
const loading = ref(false)
const showModal = ref(false)
const selectedActivity = ref(null)
const proyectos = ref([])

// ============= COMPUTED =============

/**
 * Actividades desde el store
 */
const activities = computed(() => {
  return activityStore.activities
})

/**
 * Estadísticas desde el store
 */
const estadisticas = computed(() => {
  return activityStore.estadisticas
})

/**
 * Título del modal según el modo
 */
const modalTitle = computed(() => {
  return selectedActivity.value ? 'Editar Actividad' : 'Nueva Actividad'
})

// ============= MÉTODOS =============

/**
 * Cargar actividades desde el store
 */
async function loadActivities() {
  loading.value = true
  try {
    await activityStore.fetchActivities()
  } catch (error) {
    console.error('Error al cargar actividades:', error)
    showToast('Error al cargar actividades', 'error')
  } finally {
    loading.value = false
  }
}

/**
 * Cargar proyectos para filtros
 */
async function loadProyectos() {
  try {
    const response = await apiClient.get('/projects/')
    if (response.data.success && response.data.data) {
      proyectos.value = response.data.data
    }
  } catch (error) {
    console.error('Error al cargar proyectos:', error)
  }
}

/**
 * Abrir modal para nueva actividad
 */
function openNewActivityModal() {
  selectedActivity.value = null
  showModal.value = true
}

/**
 * Abrir modal para editar actividad
 */
function openEditActivityModal(activity) {
  selectedActivity.value = activity
  showModal.value = true
}

/**
 * Cerrar modal
 */
function closeModal() {
  showModal.value = false
  selectedActivity.value = null
}

/**
 * Guardar actividad (crear o actualizar)
 */
async function handleSaveActivity(activityData) {
  closeModal()
  await loadActivities()
  showToast(
    selectedActivity.value ? 'Actividad actualizada correctamente' : 'Actividad creada correctamente',
    'success'
  )
}

/**
 * Manejar actualización de actividad
 */
async function handleActivityUpdated(activityId) {
  await loadActivities()
  showToast('Actividad actualizada correctamente', 'success')
}

/**
 * Manejar eliminación de actividad
 */
async function handleActivityDeleted(activityId) {
  await loadActivities()
  showToast('Actividad eliminada correctamente', 'success')
}

/**
 * Mostrar notificación toast
 */
function showToast(message, type = 'info') {
  const toast = document.createElement('div')
  toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white z-50 transition-opacity duration-300 ${
    type === 'success' ? 'bg-green-500' : 
    type === 'error' ? 'bg-red-500' : 
    'bg-blue-500'
  }`
  toast.textContent = message
  
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.style.opacity = '0'
    setTimeout(() => {
      document.body.removeChild(toast)
    }, 300)
  }, 3000)
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadActivities()
  loadProyectos()
})
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

/* Animación de fade para las cards de estadísticas */
.bg-gradient-to-br {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.bg-gradient-to-br:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>