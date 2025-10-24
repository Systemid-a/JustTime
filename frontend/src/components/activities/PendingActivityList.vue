<!-- ============================================================ -->
<!-- ARCHIVO: src/components/activities/PendingActivityList.vue -->
<!-- Módulo: Actividades Pendientes -->
<!-- Descripción: Lista completa de actividades con filtros -->
<!-- ============================================================ -->

<template>
  <div class="h-full flex flex-col">
    <!-- Filtros y búsqueda -->
    <div class="bg-white border-b border-gray-200 p-4 space-y-3">
      <!-- Fila 1: Tabs de estado -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-all',
            activeTab === tab.value
              ? 'bg-blue-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        >
          <span class="flex items-center gap-2">
            <component :is="tab.icon" class="w-4 h-4" />
            {{ tab.label }}
            <span
              v-if="tab.count !== undefined"
              :class="[
                'px-2 py-0.5 rounded-full text-xs font-bold',
                activeTab === tab.value
                  ? 'bg-white text-blue-600'
                  : 'bg-gray-200 text-gray-700'
              ]"
            >
              {{ tab.count }}
            </span>
          </span>
        </button>
      </div>

      <!-- Fila 2: Filtros adicionales -->
      <div class="flex flex-wrap gap-3">
        <!-- Filtro por Proyecto -->
        <select
          v-model="filterProyecto"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Todos los proyectos</option>
          <option
            v-for="proyecto in proyectos"
            :key="proyecto.id_proyecto"
            :value="proyecto.id_proyecto"
          >
            {{ proyecto.nombre }}
          </option>
        </select>

        <!-- Filtro por Prioridad -->
        <select
          v-model="filterPrioridad"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Todas las prioridades</option>
          <option value="alta">🔴 Alta</option>
          <option value="media">🟡 Media</option>
          <option value="baja">🔵 Baja</option>
        </select>

        <!-- Búsqueda -->
        <div class="flex-1 min-w-[200px] relative">
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar actividad..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <!-- Botón limpiar filtros -->
        <button
          v-if="hasActiveFilters"
          @click="clearFilters"
          class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
        >
          Limpiar filtros
        </button>
      </div>

      <!-- Información de resultados -->
      <div class="flex items-center justify-between text-sm text-gray-600">
        <span>
          Mostrando <strong>{{ filteredActivities.length }}</strong> 
          {{ filteredActivities.length === 1 ? 'actividad' : 'actividades' }}
        </span>
        
        <!-- Ordenar -->
        <select
          v-model="sortBy"
          class="px-3 py-1.5 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-blue-500"
        >
          <option value="fecha_desc">Más recientes</option>
          <option value="fecha_asc">Más antiguas</option>
          <option value="prioridad">Por prioridad</option>
          <option value="vencimiento">Por vencimiento</option>
        </select>
      </div>
    </div>

    <!-- Lista de actividades -->
    <div class="flex-1 overflow-y-auto p-4">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Cargando actividades...</p>
        </div>
      </div>

      <!-- Lista de tarjetas -->
      <div v-else-if="filteredActivities.length > 0" class="space-y-3">
        <PendingActivityCard
          v-for="activity in sortedActivities"
          :key="activity.id_actividad_pendiente"
          :activity="activity"
          @click="$emit('edit-activity', $event)"
          @updated="handleActivityUpdated"
          @deleted="handleActivityDeleted"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="flex items-center justify-center h-full">
        <div class="text-center max-w-md">
          <svg class="w-20 h-20 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            {{ emptyStateTitle }}
          </h3>
          <p class="text-gray-600 mb-4">
            {{ emptyStateMessage }}
          </p>
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Limpiar filtros
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import PendingActivityCard from './PendingActivityCard.vue'

// ============= PROPS =============
const props = defineProps({
  activities: {
    type: Array,
    required: true,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  proyectos: {
    type: Array,
    default: () => []
  }
})

// ============= EMITS =============
const emit = defineEmits(['edit-activity', 'activity-updated', 'activity-deleted'])

// ============= STATE =============
const activeTab = ref('todas')
const filterProyecto = ref('')
const filterPrioridad = ref('')
const searchQuery = ref('')
const sortBy = ref('fecha_desc')

// ============= TABS CONFIGURATION =============
const tabs = computed(() => [
  {
    value: 'todas',
    label: 'Todas',
    icon: 'svg',
    count: props.activities.length
  },
  {
    value: 'pendientes',
    label: 'Pendientes',
    icon: 'svg',
    count: props.activities.filter(a => !a.completada).length
  },
  {
    value: 'completadas',
    label: 'Completadas',
    icon: 'svg',
    count: props.activities.filter(a => a.completada).length
  },
  {
    value: 'vencidas',
    label: 'Vencidas',
    icon: 'svg',
    count: props.activities.filter(a => {
      if (a.completada || !a.fecha_vencimiento) return false
      return new Date(a.fecha_vencimiento) < new Date()
    }).length
  },
  {
    value: 'hoy',
    label: 'Hoy',
    icon: 'svg',
    count: props.activities.filter(a => {
      if (a.completada || !a.fecha_vencimiento) return false
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      const dueDate = new Date(a.fecha_vencimiento)
      return dueDate >= today && dueDate < tomorrow
    }).length
  }
])

// ============= COMPUTED =============

/**
 * Verificar si hay filtros activos
 */
const hasActiveFilters = computed(() => {
  return filterProyecto.value || filterPrioridad.value || searchQuery.value
})

/**
 * Actividades filtradas por tab activo
 */
const activitiesByTab = computed(() => {
  let filtered = props.activities

  switch (activeTab.value) {
    case 'pendientes':
      filtered = filtered.filter(a => !a.completada)
      break
    case 'completadas':
      filtered = filtered.filter(a => a.completada)
      break
    case 'vencidas':
      filtered = filtered.filter(a => {
        if (a.completada || !a.fecha_vencimiento) return false
        return new Date(a.fecha_vencimiento) < new Date()
      })
      break
    case 'hoy':
      filtered = filtered.filter(a => {
        if (a.completada || !a.fecha_vencimiento) return false
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        const tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        const dueDate = new Date(a.fecha_vencimiento)
        return dueDate >= today && dueDate < tomorrow
      })
      break
  }

  return filtered
})

/**
 * Actividades con filtros aplicados
 */
const filteredActivities = computed(() => {
  let filtered = activitiesByTab.value

  // Filtrar por proyecto
  if (filterProyecto.value) {
    filtered = filtered.filter(a => a.proyecto_id_fk === filterProyecto.value)
  }

  // Filtrar por prioridad
  if (filterPrioridad.value) {
    filtered = filtered.filter(a => a.prioridad === filterPrioridad.value)
  }

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(a =>
      a.descripcion?.toLowerCase().includes(query)
    )
  }

  return filtered
})

/**
 * Actividades ordenadas
 */
const sortedActivities = computed(() => {
  const activities = [...filteredActivities.value]

  switch (sortBy.value) {
    case 'fecha_asc':
      return activities.sort((a, b) => 
        a.id_actividad_pendiente - b.id_actividad_pendiente
      )
    case 'fecha_desc':
      return activities.sort((a, b) => 
        b.id_actividad_pendiente - a.id_actividad_pendiente
      )
    case 'prioridad':
      const prioridadOrder = { alta: 3, media: 2, baja: 1 }
      return activities.sort((a, b) => 
        prioridadOrder[b.prioridad] - prioridadOrder[a.prioridad]
      )
    case 'vencimiento':
      return activities.sort((a, b) => {
        if (!a.fecha_vencimiento) return 1
        if (!b.fecha_vencimiento) return -1
        return new Date(a.fecha_vencimiento) - new Date(b.fecha_vencimiento)
      })
    default:
      return activities
  }
})

/**
 * Título del empty state
 */
const emptyStateTitle = computed(() => {
  if (hasActiveFilters.value) {
    return 'No se encontraron actividades'
  }
  
  switch (activeTab.value) {
    case 'pendientes':
      return '¡Todo al día!'
    case 'completadas':
      return 'Aún no has completado actividades'
    case 'vencidas':
      return 'No hay actividades vencidas'
    case 'hoy':
      return 'No hay actividades para hoy'
    default:
      return 'No hay actividades'
  }
})

/**
 * Mensaje del empty state
 */
const emptyStateMessage = computed(() => {
  if (hasActiveFilters.value) {
    return 'Intenta ajustar los filtros o borrar la búsqueda'
  }
  
  switch (activeTab.value) {
    case 'pendientes':
      return 'No tienes actividades pendientes en este momento'
    case 'completadas':
      return 'Las actividades que completes aparecerán aquí'
    case 'vencidas':
      return '¡Excelente! Estás al día con tus actividades'
    case 'hoy':
      return 'No tienes actividades programadas para hoy'
    default:
      return 'Crea tu primera actividad para comenzar'
  }
})

// ============= MÉTODOS =============

/**
 * Limpiar todos los filtros
 */
function clearFilters() {
  filterProyecto.value = ''
  filterPrioridad.value = ''
  searchQuery.value = ''
}

/**
 * Manejar actualización de actividad
 */
function handleActivityUpdated(activityId) {
  emit('activity-updated', activityId)
}

/**
 * Manejar eliminación de actividad
 */
function handleActivityDeleted(activityId) {
  emit('activity-deleted', activityId)
}

// ============= WATCHERS =============

/**
 * Limpiar filtros al cambiar de tab
 */
watch(activeTab, () => {
  clearFilters()
})
</script>

<style scoped>
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