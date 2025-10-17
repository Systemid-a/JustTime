<!-- ============================================================ -->
<!-- ARCHIVO 7/31: src/components/projects/ProjectList.vue -->
<!-- Módulo: Proyectos -->
<!-- Descripción: Vista de tabla con todos los proyectos -->
<!-- ============================================================ -->

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <!-- Tabla de proyectos -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <!-- Header de la tabla -->
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th 
              class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
              @click="sort('nombre')"
            >
              <div class="flex items-center gap-2">
                Nombre del Proyecto
                <svg v-if="sortBy === 'nombre'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
                </svg>
              </div>
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Categoría
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Cliente
            </th>
            <th 
              class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
              @click="sort('estado')"
            >
              <div class="flex items-center gap-2">
                Estado
                <svg v-if="sortBy === 'estado'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
                </svg>
              </div>
            </th>
            <th class="px-6 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Tareas
            </th>
            <th 
              class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
              @click="sort('fecha_inicio')"
            >
              <div class="flex items-center gap-2">
                Fecha Inicio
                <svg v-if="sortBy === 'fecha_inicio'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
                </svg>
              </div>
            </th>
          </tr>
        </thead>

        <!-- Body de la tabla -->
        <tbody class="divide-y divide-gray-200">
          <!-- Fila por cada proyecto -->
          <tr
            v-for="project in sortedProjects"
            :key="project.id_proyecto"
            class="hover:bg-gray-50 cursor-pointer transition-colors"
            @click="$emit('edit', project)"
          >
            <!-- Nombre -->
            <td class="px-6 py-4">
              <div class="flex flex-col">
                <span class="font-semibold text-gray-900">{{ project.nombre }}</span>
                <span v-if="project.descripcion" class="text-sm text-gray-500 line-clamp-1">
                  {{ project.descripcion }}
                </span>
              </div>
            </td>

            <!-- Categoría -->
            <td class="px-6 py-4">
              <span
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold text-white"
                :class="getCategoryColor(project.categoria_nombre)"
              >
                {{ getCategoryLabel(project.categoria_nombre) }}
              </span>
            </td>

            <!-- Cliente -->
            <td class="px-6 py-4">
              <span class="text-sm text-gray-700">
                {{ project.contacto_nombre || 'Sin cliente' }}
              </span>
            </td>

            <!-- Estado -->
            <td class="px-6 py-4">
              <span
                class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium"
                :class="getStatusColor(project.estado)"
              >
                <span class="w-2 h-2 rounded-full" :class="getStatusDot(project.estado)"></span>
                {{ getStatusLabel(project.estado) }}
              </span>
            </td>

            <!-- Tareas -->
            <td class="px-6 py-4 text-center">
              <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold">
                {{ project.tareas_count || 0 }}
              </span>
            </td>

            <!-- Fecha Inicio -->
            <td class="px-6 py-4">
              <span class="text-sm text-gray-700">
                {{ formatDate(project.fecha_inicio) }}
              </span>
            </td>
          </tr>

          <!-- Mensaje si no hay proyectos -->
          <tr v-if="projects.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-500">
              <div class="flex flex-col items-center gap-2">
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p class="text-lg font-medium">No hay proyectos</p>
                <p class="text-sm">Crea tu primer proyecto para comenzar</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ============= PROPS =============
const props = defineProps({
  projects: {
    type: Array,
    required: true,
    default: () => []
  }
})

// ============= EMITS =============
defineEmits(['edit'])

// ============= STATE =============
const sortBy = ref('fecha_inicio')
const sortOrder = ref('desc')

// ============= COMPUTED =============

/**
 * Proyectos ordenados según criterio seleccionado
 */
const sortedProjects = computed(() => {
  const projectsCopy = [...props.projects]
  
  projectsCopy.sort((a, b) => {
    let valueA = a[sortBy.value]
    let valueB = b[sortBy.value]
    
    // Manejo especial para fechas
    if (sortBy.value === 'fecha_inicio') {
      valueA = new Date(valueA).getTime()
      valueB = new Date(valueB).getTime()
    }
    
    // Manejo de valores null/undefined
    if (valueA == null) return 1
    if (valueB == null) return -1
    
    // Comparación
    if (valueA < valueB) {
      return sortOrder.value === 'asc' ? -1 : 1
    }
    if (valueA > valueB) {
      return sortOrder.value === 'asc' ? 1 : -1
    }
    return 0
  })
  
  return projectsCopy
})

// ============= METHODS =============

/**
 * Cambiar ordenamiento
 */
function sort(field) {
  if (sortBy.value === field) {
    // Toggle orden si es el mismo campo
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Nuevo campo, orden descendente por defecto
    sortBy.value = field
    sortOrder.value = 'desc'
  }
}

/**
 * Obtener color de categoría
 */
function getCategoryColor(categoria) {
  const cat = categoria?.toLowerCase()
  
  switch (cat) {
    case 'civil':
      return 'bg-blue-500'
    case 'penal':
      return 'bg-red-500'
    case 'laboral':
      return 'bg-green-500'
    case 'comercial':
      return 'bg-yellow-500'
    case 'familia':
      return 'bg-purple-500'
    default:
      return 'bg-gray-500'
  }
}

/**
 * Obtener etiqueta de categoría
 */
function getCategoryLabel(categoria) {
  const cat = categoria?.toLowerCase()
  
  switch (cat) {
    case 'civil':
      return 'Civil'
    case 'penal':
      return 'Penal'
    case 'laboral':
      return 'Laboral'
    case 'comercial':
      return 'Comercial'
    case 'familia':
      return 'Familia'
    default:
      return 'Sin categoría'
  }
}

/**
 * Obtener color de estado
 */
function getStatusColor(estado) {
  const est = estado?.toLowerCase()
  
  switch (est) {
    case 'activo':
      return 'bg-green-100 text-green-700'
    case 'pausado':
      return 'bg-yellow-100 text-yellow-700'
    case 'finalizado':
      return 'bg-gray-100 text-gray-700'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}

/**
 * Obtener color del punto de estado
 */
function getStatusDot(estado) {
  const est = estado?.toLowerCase()
  
  switch (est) {
    case 'activo':
      return 'bg-green-500'
    case 'pausado':
      return 'bg-yellow-500'
    case 'finalizado':
      return 'bg-gray-500'
    default:
      return 'bg-gray-500'
  }
}

/**
 * Obtener etiqueta de estado
 */
function getStatusLabel(estado) {
  const est = estado?.toLowerCase()
  
  switch (est) {
    case 'activo':
      return 'Activo'
    case 'pausado':
      return 'Pausado'
    case 'finalizado':
      return 'Finalizado'
    default:
      return 'Desconocido'
  }
}

/**
 * Formatear fecha a formato legible
 */
function formatDate(dateString) {
  if (!dateString) return 'Sin fecha'
  
  try {
    const date = new Date(dateString)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    
    return `${day}/${month}/${year}`
  } catch (error) {
    return 'Fecha inválida'
  }
}
</script>

<style scoped>
/* Limitar texto a 1 línea */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>