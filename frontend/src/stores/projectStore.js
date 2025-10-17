import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import projectService from '@/services/projectService'
import { mapProjectFromBackend, mapProjectToBackend } from '@/utils/constants'

export const useProjectStore = defineStore('project', () => {
  const projects = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentProject = ref(null)

  const activeProjects = computed(() => {
    return projects.value.filter(p => p.estado === 'activo')
  })

  const pausedProjects = computed(() => {
    return projects.value.filter(p => p.estado === 'pausado')
  })

  const finishedProjects = computed(() => {
    return projects.value.filter(p => p.estado === 'finalizado')
  })

  const projectsByCategory = computed(() => {
    const grouped = {}
    projects.value.forEach(project => {
      const categoria = project.categoria || 'sin_categoria'
      if (!grouped[categoria]) {
        grouped[categoria] = []
      }
      grouped[categoria].push(project)
    })
    return grouped
  })

  const projectCounts = computed(() => {
    return {
      total: projects.value.length,
      activos: activeProjects.value.length,
      pausados: pausedProjects.value.length,
      finalizados: finishedProjects.value.length
    }
  })

  const getProjectById = computed(() => {
    return (id) => projects.value.find(p => p.id_proyecto === id)
  })

  async function fetchProjects() {
    loading.value = true
    error.value = null
    try {
      const response = await projectService.getProjects()
      
      if (response.success && response.data) {
        projects.value = response.data.map(proj => mapProjectFromBackend(proj))
        console.log(`✅ Proyectos cargados: ${projects.value.length}`)
      } else {
        projects.value = []
      }
    } catch (err) {
      error.value = 'Error al cargar proyectos'
      console.error('❌ Error en fetchProjects:', err)
      projects.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchActiveProjects() {
    loading.value = true
    error.value = null
    try {
      const response = await projectService.getActiveProjects()
      
      if (response.success && response.data) {
        projects.value = response.data.map(proj => mapProjectFromBackend(proj))
        console.log(`✅ Proyectos activos cargados: ${projects.value.length}`)
      } else {
        projects.value = []
      }
    } catch (err) {
      error.value = 'Error al cargar proyectos activos'
      console.error('❌ Error en fetchActiveProjects:', err)
      projects.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id) {
    loading.value = true
    error.value = null
    try {
      const response = await projectService.getProject(id)
      
      if (response.success && response.data) {
        const mappedProject = mapProjectFromBackend(response.data)
        currentProject.value = mappedProject
        
        const index = projects.value.findIndex(p => p.id_proyecto === id)
        if (index !== -1) {
          projects.value[index] = mappedProject
        }
        
        console.log('✅ Proyecto cargado:', mappedProject)
      }
    } catch (err) {
      error.value = `Error al cargar proyecto ${id}`
      console.error('❌ Error en fetchProject:', err)
    } finally {
      loading.value = false
    }
  }

  async function createProject(projectData) {
    loading.value = true
    error.value = null
    try {
      const backendData = mapProjectToBackend(projectData)
      
      console.log('📤 Creando proyecto:', backendData)
      
      const response = await projectService.createProject(backendData)
      
      if (response.success && response.data) {
        const newProject = mapProjectFromBackend(response.data)
        projects.value.push(newProject)
        
        console.log('✅ Proyecto creado')
        return newProject
      }
    } catch (err) {
      error.value = 'Error al crear proyecto'
      console.error('❌ Error en createProject:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProject(id, projectData) {
    loading.value = true
    error.value = null
    try {
      const backendData = mapProjectToBackend(projectData)
      
      console.log(`🔄 Actualizando proyecto ${id}:`, backendData)
      
      const response = await projectService.updateProject(id, backendData)
      
      if (response.success && response.data) {
        const updatedProject = mapProjectFromBackend(response.data)
        
        const index = projects.value.findIndex(p => p.id_proyecto === id)
        if (index !== -1) {
          projects.value[index] = updatedProject
        }
        
        if (currentProject.value?.id_proyecto === id) {
          currentProject.value = updatedProject
        }
        
        console.log('✅ Proyecto actualizado')
        return updatedProject
      }
    } catch (err) {
      error.value = 'Error al actualizar proyecto'
      console.error('❌ Error en updateProject:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteProject(id) {
    loading.value = true
    error.value = null
    try {
      console.log(`🗑️ Eliminando proyecto ${id}`)
      
      await projectService.deleteProject(id)
      
      projects.value = projects.value.filter(p => p.id_proyecto !== id)
      
      if (currentProject.value?.id_proyecto === id) {
        currentProject.value = null
      }
      
      console.log('✅ Proyecto eliminado')
    } catch (err) {
      error.value = 'Error al eliminar proyecto'
      console.error('❌ Error en deleteProject:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function finalizeProject(id) {
    loading.value = true
    error.value = null
    try {
      console.log(`✔️ Finalizando proyecto ${id}`)
      
      const response = await projectService.finalizeProject(id)
      
      if (response.success && response.data) {
        const finalizedProject = mapProjectFromBackend(response.data)
        
        const index = projects.value.findIndex(p => p.id_proyecto === id)
        if (index !== -1) {
          projects.value[index] = finalizedProject
        }
        
        console.log('✅ Proyecto finalizado')
        return finalizedProject
      }
    } catch (err) {
      error.value = 'Error al finalizar proyecto'
      console.error('❌ Error en finalizeProject:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  function resetStore() {
    projects.value = []
    loading.value = false
    error.value = null
    currentProject.value = null
  }

  return {
    projects,
    loading,
    error,
    currentProject,
    activeProjects,
    pausedProjects,
    finishedProjects,
    projectsByCategory,
    projectCounts,
    getProjectById,
    fetchProjects,
    fetchActiveProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    finalizeProject,
    clearError,
    resetStore
  }
})