<!-- ============================================================
     ARCHIVO: src/pages/EmployeesPage.vue
     Módulo: Empleados
     Descripción: Vista principal de gestión de empleados
     ============================================================ -->

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Empleados</h1>
        <p class="mt-1 text-sm text-gray-500">
          Administra el personal y usuarios del sistema
        </p>
      </div>
      <div class="flex gap-3">
        <button
          @click="openCreateModal"
          class="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Nuevo Empleado</span>
        </button>
        <button
          @click="openCreateWithUserModal"
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          <span>Con Usuario</span>
        </button>
      </div>
    </div>

    <!-- Filtros y Búsqueda -->
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <!-- Filtros por Estado -->
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-gray-700">Filtrar por estado:</span>
        <div class="flex gap-2">
          <button
            @click="filterStatus = 'todos'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all',
              filterStatus === 'todos'
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Todos
            <span v-if="filterStatus === 'todos'" class="ml-2 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredEmployees.length }}
            </span>
          </button>
          <button
            @click="filterStatus = 'activos'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              filterStatus === 'activos'
                ? 'bg-green-600 text-white'
                : 'bg-green-50 text-green-700 hover:bg-green-100'
            ]"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Activos
            <span v-if="filterStatus === 'activos'" class="ml-1 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredEmployees.length }}
            </span>
          </button>
          <button
            @click="filterStatus = 'inactivos'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              filterStatus === 'inactivos'
                ? 'bg-red-600 text-white'
                : 'bg-red-50 text-red-700 hover:bg-red-100'
            ]"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            Inactivos
            <span v-if="filterStatus === 'inactivos'" class="ml-1 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredEmployees.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- Filtro por Acceso al Sistema -->
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-gray-700">Acceso al sistema:</span>
        <div class="flex gap-2">
          <button
            @click="filterAccess = 'todos'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all',
              filterAccess === 'todos'
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Todos
          </button>
          <button
            @click="filterAccess = 'conUsuario'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              filterAccess === 'conUsuario'
                ? 'bg-blue-600 text-white'
                : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
            ]"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Con usuario
          </button>
        </div>
      </div>

      <!-- Barra de Búsqueda -->
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre, puesto o teléfono..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          v-if="searchQuery"
          @click="searchQuery = ''"
          class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Contador de Resultados -->
      <div class="flex items-center justify-between text-sm text-gray-600">
        <span>
          Mostrando <span class="font-semibold text-gray-900">{{ filteredEmployees.length }}</span> 
          {{ filteredEmployees.length === 1 ? 'empleado' : 'empleados' }}
        </span>
        <button
          v-if="searchQuery || filterStatus !== 'todos' || filterAccess !== 'todos'"
          @click="clearFilters"
          class="text-blue-600 hover:text-blue-800 font-medium"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="flex items-center gap-3">
        <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-600 font-medium">Cargando empleados...</span>
      </div>
    </div>

    <!-- Lista de Empleados -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nombre
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Puesto
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Teléfono
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Usuario
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Rol
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Estado
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="employee in filteredEmployees"
            :key="employee.id_empleado"
            class="hover:bg-gray-50"
          >
            <td class="px-6 py-4">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10">
                  <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <span class="text-blue-600 font-medium text-sm">
                      {{ getInitials(employee.nombre) }}
                    </span>
                  </div>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{{ employee.nombre }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ employee.puesto || 'Sin puesto' }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              {{ employee.telefono || 'Sin teléfono' }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">
              <!-- Empleado CON usuario vinculado -->
              <div v-if="employee.tiene_usuario && employee.usuario_email">
                <div class="text-sm text-gray-900">{{ employee.usuario_email }}</div>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                  <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Con acceso
                </span>
              </div>
              <!-- Empleado SIN usuario vinculado -->
              <div v-else>
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                  <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clip-rule="evenodd" />
                  </svg>
                  Sin acceso
                </span>
              </div>
            </td>
            <td class="px-6 py-4">
              <span v-if="employee.rol" :class="getRoleBadgeClass(employee.rol)" class="px-2 py-1 text-xs font-medium rounded-full">
                {{ getRoleLabel(employee.rol) }}
              </span>
              <span v-else class="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-600">
                Sin rol
              </span>
            </td>
            <td class="px-6 py-4">
              <span :class="getStatusBadgeClass(employee.activo)" class="px-2 py-1 text-xs font-medium rounded-full">
                {{ employee.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-6 py-4 text-right text-sm font-medium space-x-2">
              <button
                @click="openEditModal(employee)"
                class="text-blue-600 hover:text-blue-900"
              >
                Editar
              </button>
              <button
                @click="confirmDelete(employee)"
                class="text-red-600 hover:text-red-900"
              >
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredEmployees.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-gray-500 mb-2">No se encontraron empleados</p>
        <button
          @click="clearFilters"
          class="text-blue-600 hover:text-blue-800 font-medium text-sm"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Modal para Crear/Editar Empleado Simple -->
    <Modal
      :show="isModalOpen"
      :title="isEditMode ? 'Editar Empleado' : 'Nuevo Empleado'"
      @close="closeModal"
    >
      <EmployeeForm
        :employee="selectedEmployee"
        :loading="submitting"
        :mode="'simple'"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
    </Modal>

    <!-- Modal para Crear Empleado Con Usuario -->
    <Modal
      :show="isUserModalOpen"
      title="Nuevo Empleado con Usuario"
      size="lg"
      @close="closeUserModal"
    >
      <EmployeeUserForm
        :loading="submitting"
        @submit="handleSubmitWithUser"
        @cancel="closeUserModal"
      />
    </Modal>

    <!-- Modal de Confirmación de Eliminación -->
    <Modal
      :show="isDeleteModalOpen"
      title="Confirmar Eliminación"
      @close="cancelDelete"
    >
      <div class="space-y-4">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-700">
              ¿Estás seguro de que deseas desactivar al empleado 
              <span class="font-semibold">{{ employeeToDelete?.nombre }}</span>?
            </p>
            <p class="mt-2 text-sm text-gray-500">
              El empleado será marcado como inactivo. Esta acción puede revertirse posteriormente.
            </p>
          </div>
        </div>
        <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            @click="cancelDelete"
            :disabled="deleting"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="handleDelete"
            :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <svg 
              v-if="deleting" 
              class="animate-spin h-4 w-4 text-white" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ deleting ? 'Desactivando...' : 'Desactivar' }}</span>
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEmployeeStore } from '@/stores/employeeStore'
import Modal from '@/components/shared/Modal.vue'
import EmployeeForm from '@/components/employees/EmployeeForm.vue'
import EmployeeUserForm from '@/components/employees/EmployeeUserForm.vue'

// ============= STORES =============
const employeeStore = useEmployeeStore()

// ============= ESTADO LOCAL =============
const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const searchQuery = ref('')
const filterStatus = ref('activos') // 'todos', 'activos', 'inactivos'
const filterAccess = ref('todos') // 'todos', 'conUsuario', 'sinUsuario'

// Estados del modal de formulario simple
const isModalOpen = ref(false)
const selectedEmployee = ref(null)

// Estados del modal de formulario con usuario
const isUserModalOpen = ref(false)

// Estados del modal de eliminación
const isDeleteModalOpen = ref(false)
const employeeToDelete = ref(null)

// ============= COMPUTED =============

/**
 * Detectar si estamos en modo edición
 */
const isEditMode = computed(() => {
  return selectedEmployee.value !== null
})

/**
 * Empleados filtrados
 */
const filteredEmployees = computed(() => {
  let result = employeeStore.employees

  // Filtrar por estado (activo/inactivo)
  if (filterStatus.value === 'activos') {
    result = result.filter(e => e.activo === true)
  } else if (filterStatus.value === 'inactivos') {
    result = result.filter(e => e.activo === false)
  }

  // Filtrar por acceso al sistema
  if (filterAccess.value === 'conUsuario') {
    result = result.filter(e => e.tiene_usuario === true || e.usuario_id_fk !== null)
  }
  // Si filterAccess === 'todos', no filtramos nada

  // Filtrar por búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(e =>
      e.nombre.toLowerCase().includes(query) ||
      e.puesto?.toLowerCase().includes(query) ||
      e.telefono?.toLowerCase().includes(query)
    )
  }

  return result
})

// ============= MÉTODOS =============

/**
 * Cargar empleados
 */
async function loadEmployees() {
  loading.value = true
  try {
    await employeeStore.fetchEmployees(true) // Incluir inactivos
  } catch (error) {
    console.error('Error al cargar empleados:', error)
    alert('Error al cargar empleados: ' + error.message)
  } finally {
    loading.value = false
  }
}

/**
 * Abrir modal para crear empleado simple
 */
function openCreateModal() {
  selectedEmployee.value = null
  isModalOpen.value = true
}

/**
 * Abrir modal para crear empleado con usuario
 */
function openCreateWithUserModal() {
  isUserModalOpen.value = true
}

/**
 * Abrir modal para editar empleado
 */
function openEditModal(employee) {
  selectedEmployee.value = { ...employee }
  isModalOpen.value = true
}

/**
 * Cerrar modal simple
 */
function closeModal() {
  isModalOpen.value = false
  selectedEmployee.value = null
}

/**
 * Cerrar modal de usuario
 */
function closeUserModal() {
  isUserModalOpen.value = false
}

/**
 * Guardar empleado (crear o actualizar)
 */
async function handleSubmit(employeeData) {
  submitting.value = true
  try {
    if (isEditMode.value) {
      await employeeStore.updateEmployee(selectedEmployee.value.id_empleado, employeeData)
      alert('Empleado actualizado exitosamente')
    } else {
      await employeeStore.createEmployee(employeeData)
      alert('Empleado creado exitosamente')
    }
    closeModal()
    await loadEmployees()
  } catch (error) {
    console.error('Error al guardar empleado:', error)
    alert('Error al guardar empleado: ' + error.message)
  } finally {
    submitting.value = false
  }
}

/**
 * Guardar empleado con usuario
 */
async function handleSubmitWithUser(employeeData) {
  submitting.value = true
  try {
    await employeeStore.createEmployeeWithUser(employeeData)
    alert(`Empleado creado con usuario (${employeeData.rol}) exitosamente`)
    closeUserModal()
    await loadEmployees()
  } catch (error) {
    console.error('Error al crear empleado con usuario:', error)
    alert('Error al crear empleado con usuario: ' + error.message)
  } finally {
    submitting.value = false
  }
}

/**
 * Confirmar eliminación
 */
function confirmDelete(employee) {
  employeeToDelete.value = employee
  isDeleteModalOpen.value = true
}

/**
 * Cancelar eliminación
 */
function cancelDelete() {
  isDeleteModalOpen.value = false
  employeeToDelete.value = null
}

/**
 * Ejecutar eliminación
 */
async function handleDelete() {
  if (!employeeToDelete.value) return

  deleting.value = true
  try {
    await employeeStore.deleteEmployee(employeeToDelete.value.id_empleado)
    alert('Empleado desactivado exitosamente')
    cancelDelete()
    await loadEmployees()
  } catch (error) {
    console.error('Error al eliminar empleado:', error)
    alert('Error al eliminar empleado: ' + error.message)
  } finally {
    deleting.value = false
  }
}

/**
 * Limpiar filtros
 */
function clearFilters() {
  searchQuery.value = ''
  filterStatus.value = 'todos'
  filterAccess.value = 'todos'
}

/**
 * Obtener iniciales del nombre
 */
function getInitials(name) {
  if (!name) return '??'
  const parts = name.split(' ')
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
}

/**
 * Obtener clase CSS para badge de rol
 */
function getRoleBadgeClass(role) {
  const classes = {
    'admin': 'bg-purple-100 text-purple-700',
    'usuario': 'bg-blue-100 text-blue-700'
  }
  return classes[role] || 'bg-gray-100 text-gray-700'
}

/**
 * Obtener etiqueta de rol
 */
function getRoleLabel(role) {
  const labels = {
    'admin': 'Administrador',
    'usuario': 'Usuario'
  }
  return labels[role] || role
}

/**
 * Obtener clase CSS para badge de estado
 */
function getStatusBadgeClass(activo) {
  return activo 
    ? 'bg-green-100 text-green-700' 
    : 'bg-red-100 text-red-700'
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadEmployees()
})
</script>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>