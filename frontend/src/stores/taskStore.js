// ============================================================
// ARCHIVO 26/31: src/stores/taskStore.js
// Módulo: Stores (Pinia)
// Descripción: Estado global de tareas con Pinia
// ✨ CORREGIDO: Estados ahora usan "en_progreso" en vez de "progreso"
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import taskService from '@/services/taskService'

export const useTaskStore = defineStore('task', () => {
  // ============= ESTADO =============
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedTask = ref(null)

  // ============= GETTERS (Computed) =============
  
  /**
   * Obtener tareas por estado
   * ⚠️ CORREGIDO: Ahora usa "en_progreso" que es como lo espera el backend
   */
  const tasksByStatus = computed(() => {
    return {
      nuevo: tasks.value.filter(t => t.estado === 'nuevo'),
      en_progreso: tasks.value.filter(t => t.estado === 'en_progreso'),
      finalizado: tasks.value.filter(t => t.estado === 'finalizado')
    }
  })

  /**
   * Obtener tareas pendientes (nuevo + en_progreso)
   */
  const pendingTasks = computed(() => {
    return tasks.value.filter(t => 
      t.estado === 'nuevo' || t.estado === 'en_progreso'
    )
  })

  /**
   * Obtener tareas finalizadas
   */
  const completedTasks = computed(() => {
    return tasks.value.filter(t => t.estado === 'finalizado')
  })

  /**
   * Contar tareas por estado
   */
  const taskCounts = computed(() => {
    return {
      nuevo: tasksByStatus.value.nuevo.length,
      en_progreso: tasksByStatus.value.en_progreso.length,
      finalizado: tasksByStatus.value.finalizado.length,
      total: tasks.value.length,
      pending: pendingTasks.value.length
    }
  })

  /**
   * Obtener tareas por prioridad
   */
  const tasksByPriority = computed(() => {
    return {
      alta: tasks.value.filter(t => t.prioridad === 'alta'),
      media: tasks.value.filter(t => t.prioridad === 'media'),
      baja: tasks.value.filter(t => t.prioridad === 'baja')
    }
  })

  /**
   * Obtener tareas vencidas
   */
  const overdueTasks = computed(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    return tasks.value.filter(task => {
      if (!task.fecha_vencimiento || task.estado === 'finalizado') {
        return false
      }
      
      const dueDate = new Date(task.fecha_vencimiento)
      dueDate.setHours(0, 0, 0, 0)
      
      return dueDate < today
    })
  })

  // ============= ACTIONS =============

  /**
   * Obtener todas las tareas desde el backend
   */
  async function fetchTasks(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.getTasks(params)
      
      if (response.success && response.data) {
        tasks.value = response.data
      } else {
        throw new Error(response.message || 'Error al cargar tareas')
      }
      
      return tasks.value
    } catch (err) {
      error.value = err.message || 'Error al cargar tareas'
      console.error('Error en fetchTasks:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener tablero Kanban organizado
   * ⚠️ CORREGIDO: Ahora maneja correctamente "en_progreso"
   */
  async function fetchKanbanBoard() {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.getKanbanBoard()
      
      if (response.success && response.data) {
        // El backend retorna: { nuevo: [...], en_progreso: [...], finalizado: [...] }
        // Aplanamos a un array único
        tasks.value = [
          ...(response.data.nuevo || []),
          ...(response.data.en_progreso || []),
          ...(response.data.finalizado || [])
        ]
        
        console.log('✅ Tablero Kanban cargado:', {
          nuevo: response.data.nuevo?.length || 0,
          en_progreso: response.data.en_progreso?.length || 0,
          finalizado: response.data.finalizado?.length || 0
        })
      } else {
        throw new Error(response.message || 'Error al cargar tablero Kanban')
      }
      
      return tasksByStatus.value
    } catch (err) {
      error.value = err.message || 'Error al cargar tablero Kanban'
      console.error('Error en fetchKanbanBoard:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener una tarea específica por ID
   */
  async function fetchTask(taskId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.getTask(taskId)
      
      if (response.success && response.data) {
        selectedTask.value = response.data
        return response.data
      } else {
        throw new Error(response.message || 'Error al cargar tarea')
      }
    } catch (err) {
      error.value = err.message || 'Error al cargar tarea'
      console.error('Error en fetchTask:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear una nueva tarea
   */
  async function createTask(taskData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.createTask(taskData)
      
      if (response.success && response.data) {
        // Agregar la nueva tarea al array
        tasks.value.push(response.data)
        console.log('✅ Tarea creada:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al crear tarea')
      }
    } catch (err) {
      error.value = err.message || 'Error al crear tarea'
      console.error('Error en createTask:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar una tarea existente
   */
  async function updateTask(taskId, taskData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.updateTask(taskId, taskData)
      
      if (response.success && response.data) {
        // Actualizar la tarea en el array
        const index = tasks.value.findIndex(t => t.id_tarea === taskId)
        if (index !== -1) {
          tasks.value[index] = response.data
        }
        
        console.log('✅ Tarea actualizada:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al actualizar tarea')
      }
    } catch (err) {
      error.value = err.message || 'Error al actualizar tarea'
      console.error('Error en updateTask:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar solo el estado de una tarea (para drag & drop)
   * ⚠️ CRÍTICO: Esta función ahora valida que el estado sea correcto
   */
  async function updateTaskStatus(taskId, newStatus) {
    loading.value = true
    error.value = null
    
    // Validar que el estado sea uno de los permitidos
    const validStatuses = ['nuevo', 'en_progreso', 'finalizado']
    if (!validStatuses.includes(newStatus)) {
      console.error(`❌ Estado inválido: "${newStatus}". Debe ser: nuevo, en_progreso o finalizado`)
      error.value = 'Estado inválido'
      loading.value = false
      throw new Error('Estado inválido')
    }
    
    try {
      console.log(`🔄 Actualizando tarea ${taskId} a estado: ${newStatus}`)
      
      const response = await taskService.updateTaskStatus(taskId, newStatus)
      
      if (response.success && response.data) {
        // Actualizar el estado en el array local
        const task = tasks.value.find(t => t.id_tarea === taskId)
        if (task) {
          task.estado = newStatus
          console.log('✅ Estado actualizado localmente')
        }
        
        console.log('✅ Estado actualizado en el backend:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al actualizar estado')
      }
    } catch (err) {
      error.value = err.message || 'Error al actualizar estado de tarea'
      console.error('❌ Error en updateTaskStatus:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar una tarea
   * ✨ MEJORADO: Mejor manejo de errores y logging
   */
  async function deleteTask(taskId) {
    loading.value = true
    error.value = null
    
    try {
      console.log(`🗑️ Eliminando tarea ID: ${taskId}`)
      
      const response = await taskService.deleteTask(taskId)
      
      if (response.success) {
        // Remover la tarea del array
        const index = tasks.value.findIndex(t => t.id_tarea === taskId)
        if (index !== -1) {
          const deletedTask = tasks.value.splice(index, 1)[0]
          console.log('✅ Tarea eliminada del store:', deletedTask.titulo)
        }
        
        console.log('✅ Tarea eliminada del backend')
        return true
      } else {
        throw new Error(response.message || 'Error al eliminar tarea')
      }
    } catch (err) {
      error.value = err.message || 'Error al eliminar tarea'
      console.error('❌ Error en deleteTask:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener tareas de un proyecto específico
   */
  async function fetchTasksByProject(projectId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await taskService.getTasksByProject(projectId)
      
      if (response.success && response.data) {
        return response.data
      } else {
        throw new Error(response.message || 'Error al cargar tareas del proyecto')
      }
    } catch (err) {
      error.value = err.message || 'Error al cargar tareas del proyecto'
      console.error('Error en fetchTasksByProject:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Limpiar estado seleccionado
   */
  function clearSelectedTask() {
    selectedTask.value = null
  }

  /**
   * Limpiar errores
   */
  function clearError() {
    error.value = null
  }

  /**
   * Resetear el store completo
   */
  function $reset() {
    tasks.value = []
    loading.value = false
    error.value = null
    selectedTask.value = null
  }

  // ============= RETORNAR API PÚBLICA =============
  return {
    // Estado
    tasks,
    loading,
    error,
    selectedTask,
    
    // Getters
    tasksByStatus,
    pendingTasks,
    completedTasks,
    taskCounts,
    tasksByPriority,
    overdueTasks,
    
    // Actions
    fetchTasks,
    fetchKanbanBoard,
    fetchTask,
    createTask,
    updateTask,
    updateTaskStatus,
    deleteTask,
    fetchTasksByProject,
    clearSelectedTask,
    clearError,
    $reset
  }
})