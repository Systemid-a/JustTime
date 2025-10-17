<!-- ============================================================ -->
<!-- ARCHIVO 14/31: src/pages/HomePage.vue (VERSIÓN FINAL SIN DUPLICADOS) -->
<!-- Módulo: Pages -->
<!-- Descripción: Dashboard principal con estadísticas reales -->
<!-- ============================================================ -->

<template>
  <!-- ⚠️ ELIMINADO: <AppHeader /> y <AppSidebar /> porque ya están en App.vue -->
  
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

      <!-- Actividades Próximas -->
      <div class="bg-white rounded-lg shadow p-6 mt-8">
        <h3 class="text-lg font-bold text-gray-800 mb-4">Actividades Próximas</h3>
        <div class="space-y-3">
          <div class="flex items-center space-x-4 p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r">
            <div class="bg-yellow-100 rounded-full p-2">
              <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">Llamar al cliente López</p>
              <p class="text-sm text-gray-600">Seguimiento del caso civil</p>
              <p class="text-xs text-gray-500 mt-1">Mañana - 10:00 AM</p>
            </div>
          </div>

          <div class="flex items-center space-x-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r">
            <div class="bg-blue-100 rounded-full p-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">Audiencia Caso García</p>
              <p class="text-sm text-gray-600">Presentación de alegatos</p>
              <p class="text-xs text-gray-500 mt-1">11 oct 2025 - 3:00 PM</p>
            </div>
          </div>

          <div class="flex items-center space-x-4 p-3 bg-purple-50 border-l-4 border-purple-500 rounded-r">
            <div class="bg-purple-100 rounded-full p-2">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">Enviar documentación</p>
              <p class="text-sm text-gray-600">Documentos para registro mercantil</p>
              <p class="text-xs text-gray-500 mt-1">12 oct 2025</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

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

// ============= MÉTODOS =============

/**
 * Cargar datos del dashboard desde las APIs
 * ✅ VERSIÓN CORREGIDA - Consume APIs reales del backend
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
    
    // ✅ Documentos (si tienes endpoint, sino usar valor por defecto)
    stats.value.documentosSubidos = 0
    
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

// ============= LIFECYCLE =============
onMounted(() => {
  fetchDashboardData()
})
</script>