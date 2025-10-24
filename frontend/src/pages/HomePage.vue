<!-- ============================================================ -->
<!-- ARCHIVO: src/pages/HomePage.vue (VERSIÓN FINAL CORREGIDA) -->
<!-- Módulo: Pages -->
<!-- Descripción: Dashboard principal con estadísticas reales -->
<!-- ✅ CORREGIDO: Ahora carga actividades pendientes reales desde el backend -->
<!-- ============================================================ -->

<template>
  <div>
    <!-- Título -->
    <div class="mb-8">
      <h2 class="text-3xl font-bold text-gray-800">Dashboard</h2>
      <p class="text-gray-600 mt-1">Vista general de tu oficina jurídica</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <p class="text-red-800">{{ error }}</p>
      <button @click="fetchDashboardData" class="mt-2 text-red-600 hover:text-red-800 font-medium">
        Reintentar
      </button>
    </div>

    <!-- Contenido -->
    <div v-else>
      <!-- Tarjetas de Estadísticas -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Proyectos Activos -->
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">PROYECTOS ACTIVOS</p>
              <p class="text-3xl font-bold text-gray-800 mt-2">{{ stats.proyectosActivos }}</p>
              <p class="text-gray-500 text-xs mt-1">Casos en gestión</p>
            </div>
            <div class="bg-blue-100 rounded-full p-3">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Tareas Pendientes -->
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">TAREAS PENDIENTES</p>
              <p class="text-3xl font-bold text-gray-800 mt-2">{{ stats.tareasPendientes }}</p>
              <p class="text-gray-500 text-xs mt-1">Por completar</p>
            </div>
            <div class="bg-yellow-100 rounded-full p-3">
              <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Contactos Registrados -->
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">CONTACTOS REGISTRADOS</p>
              <p class="text-3xl font-bold text-gray-800 mt-2">{{ stats.contactosRegistrados }}</p>
              <p class="text-gray-500 text-xs mt-1">Clientes y empresas</p>
            </div>
            <div class="bg-green-100 rounded-full p-3">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Documentos Subidos -->
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">DOCUMENTOS SUBIDOS</p>
              <p class="text-3xl font-bold text-gray-800 mt-2">{{ stats.documentosSubidos }}</p>
              <p class="text-gray-500 text-xs mt-1">Archivos totales</p>
            </div>
            <div class="bg-purple-100 rounded-full p-3">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Secciones de Contenido -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Proyectos Recientes -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-800">Proyectos Recientes</h3>
            <router-link to="/proyectos" class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
              Ver todos →
            </router-link>
          </div>

          <!-- Lista de Proyectos -->
          <div v-if="recentProjects.length > 0" class="space-y-4">
            <div 
              v-for="project in recentProjects" 
              :key="project.id_proyecto"
              class="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-r-lg hover:bg-blue-100 transition cursor-pointer"
            >
              <h4 class="font-semibold text-gray-800">{{ project.nombre }}</h4>
              <p class="text-gray-600 text-sm mt-1">{{ project.descripcion }}</p>
              <div class="flex items-center justify-between mt-2">
                <span class="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                  {{ project.estado }}
                </span>
                <span class="text-xs text-gray-500">{{ formatDate(project.fecha_inicio) }}</span>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
            </svg>
            <p class="text-gray-500 mt-2">No hay proyectos recientes</p>
          </div>
        </div>

        <!-- Tareas por Hacer -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-800">Tareas por Hacer</h3>
            <router-link to="/kanban" class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
              Ver Kanban →
            </router-link>
          </div>

          <!-- Lista de Tareas -->
          <div v-if="pendingTasks.length > 0" class="space-y-3">
            <div 
              v-for="task in pendingTasks" 
              :key="task.id_tarea"
              class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition cursor-pointer"
            >
              <input type="checkbox" class="mt-1 w-4 h-4 text-indigo-600" />
              <div class="flex-1">
                <p class="font-medium text-gray-800">{{ task.titulo }}</p>
                <p class="text-sm text-gray-600 mt-1">{{ task.descripcion }}</p>
                <div class="flex items-center space-x-2 mt-2">
                  <span class="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">
                    {{ task.prioridad }}
                  </span>
                  <span class="text-xs text-gray-500">{{ formatDate(task.fecha_vencimiento) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-gray-500 mt-2">No hay tareas pendientes</p>
          </div>
        </div>
      </div>

      <!-- ✅ CORREGIDO: Actividades Pendientes REALES desde la API -->
      <div class="bg-white rounded-lg shadow p-6 mt-8">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">Actividades Próximas</h3>
          <router-link to="/actividades-pendientes" class="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
            Ver todas →
          </router-link>
        </div>

        <!-- Lista de Actividades Pendientes -->
        <div v-if="upcomingActivities.length > 0" class="space-y-3">
          <div 
            v-for="activity in upcomingActivities" 
            :key="activity.id_actividad_pendiente"
            class="flex items-center space-x-4 p-3 rounded-r border-l-4"
            :class="getActivityClasses(activity)"
          >
            <div class="rounded-full p-2" :class="getActivityIconBgClass(activity)">
              <svg class="w-5 h-5" :class="getActivityIconClass(activity)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="activity.prioridad === 'alta'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                <path v-else-if="activity.prioridad === 'media'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <p class="font-medium text-gray-800">{{ activity.descripcion }}</p>
              <div class="flex items-center space-x-2 mt-1">
                <span 
                  class="inline-block text-xs px-2 py-1 rounded"
                  :class="getPriorityClasses(activity.prioridad)"
                >
                  {{ activity.prioridad }}
                </span>
                <span v-if="activity.proyecto_nombre" class="text-xs text-gray-600">
                  📁 {{ activity.proyecto_nombre }}
                </span>
                <span v-if="activity.fecha_vencimiento" class="text-xs text-gray-500">
                  📅 {{ formatDate(activity.fecha_vencimiento) }}
                </span>
                <span v-else class="text-xs text-gray-400">Sin fecha</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-8">
          <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-gray-500 mt-2">No hay actividades pendientes</p>
          <p class="text-gray-400 text-sm mt-1">¡Excelente! Estás al día con tus tareas</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'
import documentService from '@/services/documentService'
import pendingActivityService from '@/services/pendingActivityService'  // ✅ IMPORTADO

// ============= COMPOSABLES =============
const router = useRouter()

// ============= ESTADO =============
const loading = ref(true)
const error = ref(null)

// Estadísticas
const stats = ref({
  proyectosActivos: 0,
  tareasPendientes: 0,
  contactosRegistrados: 0,
  documentosSubidos: 0
})

// Datos
const recentProjects = ref([])
const pendingTasks = ref([])
const upcomingActivities = ref([])  // ✅ NUEVO: Para actividades pendientes reales

// ============= MÉTODOS =============

/**
 * Cargar datos del dashboard desde las APIs
 * ✅ VERSIÓN CORREGIDA - Incluye actividades pendientes reales
 */
async function fetchDashboardData() {
  loading.value = true
  error.value = null
  
  try {
    // ✅ CARGAR PROYECTOS desde API
    const projectsResponse = await apiClient.get('/projects/')
    const projects = projectsResponse.data.data || []
    
    // Calcular proyectos activos
    stats.value.proyectosActivos = projects.filter(p => p.estado === 'activo').length
    
    // Obtener proyectos recientes (máximo 3)
    recentProjects.value = projects
      .sort((a, b) => new Date(b.fecha_inicio) - new Date(a.fecha_inicio))
      .slice(0, 3)
    
    // ✅ CARGAR TAREAS desde API
    const tasksResponse = await apiClient.get('/tasks/')
    const tasks = tasksResponse.data.data || []
    
    // Calcular tareas pendientes
    stats.value.tareasPendientes = tasks.filter(t => t.estado !== 'finalizado').length
    
    // Obtener tareas pendientes (máximo 5)
    pendingTasks.value = tasks
      .filter(t => t.estado !== 'finalizado')
      .slice(0, 5)
    
    // ✅ CARGAR CONTACTOS desde API
    const contactsResponse = await apiClient.get('/contactos/')
    const contacts = contactsResponse.data.data || []
    stats.value.contactosRegistrados = contacts.length
    
    // ✅ CARGAR DOCUMENTOS desde API
    try {
      const documentsStatsResponse = await documentService.getStatistics()
      if (documentsStatsResponse.success && documentsStatsResponse.data) {
        stats.value.documentosSubidos = documentsStatsResponse.data.total || 0
      } else {
        stats.value.documentosSubidos = 0
      }
    } catch (docError) {
      console.error('❌ Error al cargar estadísticas de documentos:', docError)
      stats.value.documentosSubidos = 0
    }
    
    // ✅ CARGAR ACTIVIDADES PENDIENTES REALES desde API
    try {
      const activitiesResponse = await pendingActivityService.getPendientes()
      if (activitiesResponse.success && activitiesResponse.data) {
        // Obtener las próximas 5 actividades pendientes, ordenadas por fecha de vencimiento
        upcomingActivities.value = activitiesResponse.data
          .sort((a, b) => {
            // Si no tienen fecha, van al final
            if (!a.fecha_vencimiento) return 1
            if (!b.fecha_vencimiento) return -1
            // Ordenar por fecha más cercana primero
            return new Date(a.fecha_vencimiento) - new Date(b.fecha_vencimiento)
          })
          .slice(0, 5)
        
        console.log('✅ Actividades pendientes cargadas:', upcomingActivities.value)
      } else {
        upcomingActivities.value = []
        console.warn('⚠️ No se encontraron actividades pendientes')
      }
    } catch (actError) {
      console.error('❌ Error al cargar actividades pendientes:', actError)
      upcomingActivities.value = []
    }
    
    console.log('✅ Datos del dashboard cargados correctamente')
    
  } catch (err) {
    console.error('❌ Error al cargar datos del dashboard:', err)
    error.value = 'Error al cargar los datos. Por favor, intenta de nuevo.'
  } finally {
    loading.value = false
  }
}

/**
 * Formatear fecha
 */
function formatDate(dateString) {
  if (!dateString) return 'Sin fecha'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short', 
    year: 'numeric' 
  })
}

/**
 * ✅ NUEVO: Obtener clases CSS según la prioridad de la actividad
 */
function getActivityClasses(activity) {
  const priorityMap = {
    'alta': 'bg-red-50 border-red-500',
    'media': 'bg-yellow-50 border-yellow-500',
    'baja': 'bg-blue-50 border-blue-500'
  }
  return priorityMap[activity.prioridad] || 'bg-gray-50 border-gray-500'
}

function getActivityIconBgClass(activity) {
  const priorityMap = {
    'alta': 'bg-red-100',
    'media': 'bg-yellow-100',
    'baja': 'bg-blue-100'
  }
  return priorityMap[activity.prioridad] || 'bg-gray-100'
}

function getActivityIconClass(activity) {
  const priorityMap = {
    'alta': 'text-red-600',
    'media': 'text-yellow-600',
    'baja': 'text-blue-600'
  }
  return priorityMap[activity.prioridad] || 'text-gray-600'
}

function getPriorityClasses(prioridad) {
  const priorityMap = {
    'alta': 'bg-red-100 text-red-800',
    'media': 'bg-yellow-100 text-yellow-800',
    'baja': 'bg-blue-100 text-blue-800'
  }
  return priorityMap[prioridad] || 'bg-gray-100 text-gray-800'
}

// ============= LIFECYCLE =============
onMounted(() => {
  fetchDashboardData()
})
</script>