// ============================================================
// ARCHIVO: src/stores/employeeStore.js
// Módulo: Stores (Pinia)
// Descripción: Estado global de empleados con Pinia
// ============================================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import employeeService from '@/services/employeeService'

export const useEmployeeStore = defineStore('employee', () => {
  // ============= ESTADO =============
  const employees = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedEmployee = ref(null)

  // ============= GETTERS (Computed) =============
  
  /**
   * Obtener empleados activos
   */
  const activeEmployees = computed(() => {
    return employees.value.filter(e => e.activo === true)
  })

  /**
   * Obtener empleados inactivos
   */
  const inactiveEmployees = computed(() => {
    return employees.value.filter(e => e.activo === false)
  })

  /**
   * Obtener empleados con usuario asociado
   */
  const employeesWithUser = computed(() => {
    return employees.value.filter(e => e.usuario_id_fk !== null && e.usuario_id_fk !== undefined)
  })

  /**
   * Obtener empleados sin usuario asociado
   */
  const employeesWithoutUser = computed(() => {
    return employees.value.filter(e => !e.usuario_id_fk)
  })

  /**
   * Contar empleados
   */
  const employeeCounts = computed(() => {
    return {
      total: employees.value.length,
      activos: activeEmployees.value.length,
      inactivos: inactiveEmployees.value.length,
      conUsuario: employeesWithUser.value.length,
      sinUsuario: employeesWithoutUser.value.length
    }
  })

  /**
   * Obtener empleados por rol (si tienen usuario)
   */
  const employeesByRole = computed(() => {
    return {
      admin: employees.value.filter(e => e.rol === 'admin'),
      usuario: employees.value.filter(e => e.rol === 'usuario'),
      sinRol: employees.value.filter(e => !e.rol)
    }
  })

  // ============= ACTIONS =============

  /**
   * Obtener todos los empleados desde el backend
   * @param {boolean} incluirInactivos - Incluir empleados inactivos
   */
  async function fetchEmployees(incluirInactivos = false) {
    loading.value = true
    error.value = null
    
    try {
      const response = incluirInactivos 
        ? await employeeService.getAllEmployees()
        : await employeeService.getActiveEmployees()
      
      if (response.success && response.data) {
        employees.value = response.data
        console.log(`✅ Empleados cargados: ${employees.value.length}`)
      } else {
        throw new Error(response.message || 'Error al cargar empleados')
      }
      
      return employees.value
    } catch (err) {
      error.value = err.message || 'Error al cargar empleados'
      console.error('❌ Error en fetchEmployees:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtener un empleado específico por ID
   */
  async function fetchEmployee(employeeId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await employeeService.getEmployee(employeeId)
      
      if (response.success && response.data) {
        selectedEmployee.value = response.data
        return response.data
      } else {
        throw new Error(response.message || 'Error al cargar empleado')
      }
    } catch (err) {
      error.value = err.message || 'Error al cargar empleado'
      console.error('❌ Error en fetchEmployee:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo empleado SIN usuario
   */
  async function createEmployee(employeeData) {
    loading.value = true
    error.value = null
    
    try {
      console.log('📝 Creando empleado sin usuario:', employeeData)
      
      const response = await employeeService.createEmployee(employeeData)
      
      if (response.success && response.data) {
        // Agregar el nuevo empleado al array
        employees.value.push(response.data)
        console.log('✅ Empleado creado:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al crear empleado')
      }
    } catch (err) {
      error.value = err.message || 'Error al crear empleado'
      console.error('❌ Error en createEmployee:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo empleado CON usuario y rol
   */
  async function createEmployeeWithUser(employeeData) {
    loading.value = true
    error.value = null
    
    try {
      console.log('📝 Creando empleado con usuario:', {
        nombre: employeeData.nombre,
        email: employeeData.email,
        rol: employeeData.rol
      })
      
      const response = await employeeService.createEmployeeWithUser(employeeData)
      
      if (response.success && response.data) {
        // Agregar el nuevo empleado al array
        employees.value.push(response.data)
        console.log('✅ Empleado con usuario creado:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al crear empleado con usuario')
      }
    } catch (err) {
      error.value = err.message || 'Error al crear empleado con usuario'
      console.error('❌ Error en createEmployeeWithUser:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar un empleado existente
   */
  async function updateEmployee(employeeId, employeeData) {
    loading.value = true
    error.value = null
    
    try {
      console.log(`📝 Actualizando empleado ${employeeId}:`, employeeData)
      
      const response = await employeeService.updateEmployee(employeeId, employeeData)
      
      if (response.success && response.data) {
        // Actualizar el empleado en el array
        const index = employees.value.findIndex(e => e.id_empleado === employeeId)
        if (index !== -1) {
          employees.value[index] = response.data
        }
        
        console.log('✅ Empleado actualizado:', response.data)
        return response.data
      } else {
        throw new Error(response.message || 'Error al actualizar empleado')
      }
    } catch (err) {
      error.value = err.message || 'Error al actualizar empleado'
      console.error('❌ Error en updateEmployee:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar un empleado (soft delete)
   */
  async function deleteEmployee(employeeId) {
    loading.value = true
    error.value = null
    
    try {
      console.log(`🗑️ Eliminando empleado ID: ${employeeId}`)
      
      const response = await employeeService.deleteEmployee(employeeId)
      
      if (response.success) {
        // Remover el empleado del array o marcarlo como inactivo
        const index = employees.value.findIndex(e => e.id_empleado === employeeId)
        if (index !== -1) {
          // Marcar como inactivo en lugar de eliminar
          employees.value[index].activo = false
          console.log('✅ Empleado marcado como inactivo')
        }
        
        return true
      } else {
        throw new Error(response.message || 'Error al eliminar empleado')
      }
    } catch (err) {
      error.value = err.message || 'Error al eliminar empleado'
      console.error('❌ Error en deleteEmployee:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Vincular usuario a empleado
   */
  async function linkUserToEmployee(employeeId, userId) {
    loading.value = true
    error.value = null
    
    try {
      console.log(`🔗 Vinculando usuario ${userId} a empleado ${employeeId}`)
      
      const response = await employeeService.linkUserToEmployee(employeeId, userId)
      
      if (response.success && response.data) {
        // Actualizar el empleado en el array
        const index = employees.value.findIndex(e => e.id_empleado === employeeId)
        if (index !== -1) {
          employees.value[index] = response.data
        }
        
        console.log('✅ Usuario vinculado exitosamente')
        return response.data
      } else {
        throw new Error(response.message || 'Error al vincular usuario')
      }
    } catch (err) {
      error.value = err.message || 'Error al vincular usuario'
      console.error('❌ Error en linkUserToEmployee:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Limpiar empleado seleccionado
   */
  function clearSelectedEmployee() {
    selectedEmployee.value = null
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
    employees.value = []
    loading.value = false
    error.value = null
    selectedEmployee.value = null
  }

  // ============= RETORNAR API PÚBLICA =============
  return {
    // Estado
    employees,
    loading,
    error,
    selectedEmployee,
    
    // Getters
    activeEmployees,
    inactiveEmployees,
    employeesWithUser,
    employeesWithoutUser,
    employeeCounts,
    employeesByRole,
    
    // Actions
    fetchEmployees,
    fetchEmployee,
    createEmployee,
    createEmployeeWithUser,
    updateEmployee,
    deleteEmployee,
    linkUserToEmployee,
    clearSelectedEmployee,
    clearError,
    $reset
  }
})