<!-- ============================================================ -->
<!-- ARCHIVO 17/31: src/pages/ProjectsPage.vue -->
<!-- Módulo: Páginas -->
<!-- Descripción: Vista principal de gestión de proyectos con toggle Cards/Lista -->
<!-- ============================================================ -->

<template>
  <div class="p-8">
    <!-- Header: Título y Botón Nuevo Proyecto -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Gestión de Proyectos</h1>
        <p class="text-gray-600 mt-1">Organiza y gestiona tus casos jurídicos</p>
      </div>
      <button
        @click="openNewProjectModal"
        class="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nuevo Proyecto
      </button>
    </div>

    <!-- Barra de Controles: Toggle Vista + Filtros + Búsqueda -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Toggle Vista Cards/Lista -->
        <div class="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
          <button
            @click="currentView = 'cards'"
            :class="[
              'flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all',
              currentView === 'cards'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Tarjetas
          </button>
          <button
            @click="currentView = 'list'"
            :class="[
              'flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all',
              currentView === 'list'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
            Lista
          </button>
        </div>

        <!-- Filtros -->
        <div class="flex-1 flex flex-col sm:flex-row gap-3">
          <!-- Filtro por Estado -->
          <select
            v-model="filterStatus"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="activo">Activos</option>
            <option value="pausado">Pausados</option>
            <option value="finalizado">Finalizados</option>
          </select>

          <!-- Filtro por Categoría -->
          <select
            v-model="filterCategory"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todas las categorías</option>
            <option value="civil">Civil</option>
            <option value="penal">Penal</option>
            <option value="laboral">Laboral</option>
            <option value="comercial">Comercial</option>
            <option value="familia">Familia</option>
          </select>

          <!-- Búsqueda -->
          <div class="relative flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar proyecto..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Contador de resultados -->
      <div v-if="filteredProjects.length > 0" class="mt-3 text-sm text-gray-600">
        Mostrando {{ filteredProjects.length }} {{ filteredProjects.length === 1 ? 'proyecto' : 'proyectos' }}
      </div>
    </div>

    <!-- Estado de Carga -->
    <div v-if="projectStore.loading" class="flex items-center justify-center py-20">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600 font-medium">Cargando proyectos...</p>
      </div>
    </div>

    <!-- Vista de Tarjetas (Cards Grid) -->
    <div
      v-else-if="currentView === 'cards' && filteredProjects.length > 0"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <ProjectCard
        v-for="project in filteredProjects"
        :key="project.id_proyecto"
        :project="project"
        @click="openEditProjectModal(project)"
      />
    </div>

    <!-- Vista de Lista (Tabla) -->
    <ProjectList
      v-else-if="currentView === 'list' && filteredProjects.length > 0"
      :projects="filteredProjects"
      @edit="openEditProjectModal"
    />

    <!-- Mensaje cuando no hay proyectos -->
    <div
      v-else-if="!projectStore.loading && filteredProjects.length === 0"
      class="flex flex-col items-center justify-center py-20 text-center"
    >
      <svg class="w-24 h-24 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="text-xl font-semibold text-gray-700 mb-2">
        {{ searchQuery || filterStatus || filterCategory ? 'No se encontraron proyectos' : 'No hay proyectos' }}
      </h3>
      <p class="text-gray-500 mb-6">
        {{ searchQuery || filterStatus || filterCategory 
          ? 'Intenta ajustar los filtros de búsqueda' 
          : 'Crea tu primer proyecto para comenzar' 
        }}
      </p>
      <button
        v-if="!searchQuery && !filterStatus && !filterCategory"
        @click="openNewProjectModal"
        class="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Crear Primer Proyecto
      </button>
    </div>

    <!-- Modal con Formulario -->
    <Modal :show="showModal" :size="'lg'" @close="closeModal">
      <ProjectForm
        :project="selectedProject"
        @save="handleSaveProject"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProjectStore } from '@/stores/projectStore'
import ProjectCard from '@/components/projects/ProjectCard.vue'
import ProjectList from '@/components/projects/ProjectList.vue'
import ProjectForm from '@/components/projects/ProjectForm.vue'
import Modal from '@/components/shared/Modal.vue'

// ============= STORES =============
const projectStore = useProjectStore()

// ============= STATE =============
const currentView = ref('cards') // 'cards' o 'list'
const showModal = ref(false)
const selectedProject = ref(null)
const searchQuery = ref('')
const filterStatus = ref('')
const filterCategory = ref('')

// ============= COMPUTED =============

/**
 * Proyectos filtrados según criterios de búsqueda
 */
const filteredProjects = computed(() => {
  let projects = projectStore.projects

  // Filtrar por estado
  if (filterStatus.value) {
    projects = projects.filter(p => p.estado === filterStatus.value)
  }

  // Filtrar por categoría
  if (filterCategory.value) {
    projects = projects.filter(p => p.categoria === filterCategory.value)
  }

  // Filtrar por búsqueda de texto
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    projects = projects.filter(p => {
      return (
        p.nombre?.toLowerCase().includes(query) ||
        p.descripcion?.toLowerCase().includes(query) ||
        p.cliente?.toLowerCase().includes(query)
      )
    })
  }

  return projects
})

// ============= METHODS =============

/**
 * Abrir modal para nuevo proyecto
 */
function openNewProjectModal() {
  selectedProject.value = null
  showModal.value = true
}

/**
 * Abrir modal para editar proyecto
 */
function openEditProjectModal(project) {
  selectedProject.value = project
  showModal.value = true
}

/**
 * Cerrar modal
 */
function closeModal() {
  showModal.value = false
  selectedProject.value = null
}

/**
 * Guardar proyecto (crear o actualizar)
 */
async function handleSaveProject(projectData) {
  try {
    if (selectedProject.value) {
      // Actualizar proyecto existente
      await projectStore.updateProject(selectedProject.value.id_proyecto, projectData)
      console.log('Proyecto actualizado exitosamente')
    } else {
      // Crear nuevo proyecto
      await projectStore.createProject(projectData)
      console.log('Proyecto creado exitosamente')
    }
    
    // Cerrar modal
    closeModal()
    
    // Recargar proyectos
    await projectStore.fetchProjects()
  } catch (error) {
    console.error('Error al guardar proyecto:', error)
    alert('Hubo un error al guardar el proyecto. Por favor, intenta nuevamente.')
  }
}

// ============= LIFECYCLE =============

/**
 * Cargar proyectos al montar el componente
 */
onMounted(async () => {
  await projectStore.fetchProjects()
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>