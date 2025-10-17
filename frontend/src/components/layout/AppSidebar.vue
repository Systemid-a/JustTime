<!-- ============================================================ -->
<!-- ARCHIVO 2/31: src/components/layout/AppSidebar.vue - ACTUALIZADO -->
<!-- Módulo: Layout -->
<!-- Descripción: Sidebar con contadores DINÁMICOS desde la BD -->
<!-- ⭐ AGREGADO: Botón de Análisis y Reportes -->
<!-- ============================================================ -->

<template>
  <aside class="w-64 bg-white border-r border-gray-200 overflow-y-auto">
    <!-- Contenido del sidebar -->
    <nav class="px-4 py-6">
      <!-- Sección PRINCIPAL -->
      <div class="mb-6">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Principal
        </h3>
        <router-link
          to="/dashboard"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/dashboard')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <BarChart3 class="w-5 h-5" />
            <span class="font-medium">Dashboard</span>
          </div>
        </router-link>

        <router-link
          to="/tablero"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/tablero')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <Trello class="w-5 h-5" />
            <span class="font-medium">Tablero Kanban</span>
            <span v-if="tasksCount > 0" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              {{ tasksCount }}
            </span>
          </div>
        </router-link>
      </div>

      <!-- Sección GESTIÓN -->
      <div class="mb-6">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Gestión
        </h3>
        
        <router-link
          to="/tareas"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/tareas')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <CheckSquare class="w-5 h-5" />
            <span class="font-medium">Tareas</span>
            <span v-if="tasksCount > 0" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              {{ tasksCount }}
            </span>
          </div>
        </router-link>

        <router-link
          to="/proyectos"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/proyectos')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <FolderOpen class="w-5 h-5" />
            <span class="font-medium">Proyectos</span>
            <span v-if="projectsCount > 0" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              {{ projectsCount }}
            </span>
          </div>
        </router-link>

        <router-link
          to="/contactos"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/contactos')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <Users class="w-5 h-5" />
            <span class="font-medium">Contactos</span>
          </div>
        </router-link>

        <router-link
          to="/documentos"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/documentos')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <FileText class="w-5 h-5" />
            <span class="font-medium">Documentos</span>
          </div>
        </router-link>

        <!-- ⭐ NUEVO: Botón de Análisis y Reportes -->
        <router-link
          to="/analisis"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/analisis')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <PieChart class="w-5 h-5" />
            <span class="font-medium">Análisis</span>
          </div>
        </router-link>
      </div>

      <!-- Sección ORGANIZACIÓN -->
      <div class="mb-6">
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Organización
        </h3>
        
        <router-link
          to="/actividades-pendientes"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/actividades-pendientes')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <Clock class="w-5 h-5" />
            <span class="font-medium">Actividades Pendientes</span>
            <span v-if="pendingActivitiesCount > 0" class="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              {{ pendingActivitiesCount }}
            </span>
          </div>
        </router-link>

        <router-link
          to="/plantillas"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/plantillas')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <FilePlus class="w-5 h-5" />
            <span class="font-medium">Plantillas</span>
          </div>
        </router-link>

        <router-link
          to="/empleados"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/empleados')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200 mt-2',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <UserCircle class="w-5 h-5" />
            <span class="font-medium">Empleados</span>
          </div>
        </router-link>
      </div>

      <!-- Sección SISTEMA -->
      <div>
        <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Sistema
        </h3>
        
        <router-link
          to="/configuracion"
          v-slot="{ isActive }"
          custom
        >
          <div
            @click="navigateTo('/configuracion')"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors duration-200',
              isActive 
                ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600' 
                : 'text-gray-700 hover:bg-gray-50'
            ]"
          >
            <Settings class="w-5 h-5" />
            <span class="font-medium">Configuración</span>
          </div>
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  BarChart3, 
  Trello, 
  CheckSquare, 
  FolderOpen, 
  Users, 
  FileText,
  Clock,
  FilePlus,
  UserCircle,
  Settings,
  PieChart  // ⭐ AGREGADO: Ícono para Análisis
} from 'lucide-vue-next'

// ============= COMPOSABLES =============
const router = useRouter()

// ============= STATE =============
const tasksCount = ref(0) // Dinámico desde BD
const projectsCount = ref(0) // Dinámico desde BD
const pendingActivitiesCount = ref(0) // Dinámico desde BD

// ============= MÉTODOS =============
/**
 * Navegar a una ruta
 */
function navigateTo(path) {
  router.push(path)
}

/**
 * Cargar contadores dinámicos desde la BD real
 */
async function loadCounters() {
  try {
    // Importar apiClient para hacer peticiones
    const apiClient = (await import('@/services/api')).default
    
    // Cargar datos en paralelo
    const [tasksRes, projectsRes] = await Promise.all([
      apiClient.get('/tasks/'),
      apiClient.get('/projects/')
    ])
    
    // Contar tareas pendientes (nuevo + en_progreso)
    if (tasksRes.data?.data) {
      tasksCount.value = tasksRes.data.data.filter(t => 
        t.estado === 'nuevo' || t.estado === 'en_progreso'
      ).length
    }
    
    // Contar proyectos activos
    if (projectsRes.data?.data) {
      projectsCount.value = projectsRes.data.data.filter(p => 
        p.estado === 'activo'
      ).length
    }
    
    // TODO: Implementar actividades pendientes cuando esté el endpoint
    pendingActivitiesCount.value = 0
    
  } catch (error) {
    console.error('Error al cargar contadores:', error)
    // Mantener en 0 si hay error
    tasksCount.value = 0
    projectsCount.value = 0
    pendingActivitiesCount.value = 0
  }
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadCounters()
})
</script>