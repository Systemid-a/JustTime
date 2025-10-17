<!-- ============================================================
     ARCHIVO 18/31: src/pages/ContactsPage.vue
     Módulo: Contactos
     Descripción: Vista principal de gestión de contactos
     ============================================================ -->

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Contactos</h1>
        <p class="mt-1 text-sm text-gray-500">
          Administra personas y empresas vinculadas a tus proyectos
        </p>
      </div>
      <button
        @click="openCreateModal"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>Nuevo Contacto</span>
      </button>
    </div>

    <!-- Filtros y Búsqueda -->
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <!-- Filtros por Tipo -->
      <div class="flex items-center gap-3">
        <span class="text-sm font-medium text-gray-700">Filtrar por tipo:</span>
        <div class="flex gap-2">
          <button
            @click="filterType = 'todos'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all',
              filterType === 'todos'
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            Todos
            <span v-if="filterType === 'todos'" class="ml-2 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredContacts.length }}
            </span>
          </button>
          <button
            @click="filterType = 'personas'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              filterType === 'personas'
                ? 'bg-blue-600 text-white'
                : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
            ]"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
            Personas
            <span v-if="filterType === 'personas'" class="ml-1 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredContacts.length }}
            </span>
          </button>
          <button
            @click="filterType = 'empresas'"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
              filterType === 'empresas'
                ? 'bg-green-600 text-white'
                : 'bg-green-50 text-green-700 hover:bg-green-100'
            ]"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd" />
            </svg>
            Empresas
            <span v-if="filterType === 'empresas'" class="ml-1 text-xs bg-white bg-opacity-20 px-2 py-0.5 rounded">
              {{ filteredContacts.length }}
            </span>
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
          placeholder="Buscar por nombre, email o teléfono..."
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
          Mostrando <span class="font-semibold text-gray-900">{{ filteredContacts.length }}</span> 
          {{ filteredContacts.length === 1 ? 'contacto' : 'contactos' }}
        </span>
        <button
          v-if="searchQuery || filterType !== 'todos'"
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
        <span class="text-gray-600 font-medium">Cargando contactos...</span>
      </div>
    </div>

    <!-- Lista de Contactos -->
    <ContactList
      v-else
      :contacts="filteredContacts"
      @edit-contact="openEditModal"
      @delete-contact="confirmDelete"
    />

    <!-- Modal para Crear/Editar Contacto -->
    <Modal
      :is-open="isModalOpen"
      :title="isEditMode ? 'Editar Contacto' : 'Nuevo Contacto'"
      @close="closeModal"
    >
      <ContactForm
        :contact="selectedContact"
        :loading="submitting"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
    </Modal>

    <!-- Modal de Confirmación de Eliminación -->
    <Modal
      :is-open="isDeleteModalOpen"
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
              ¿Estás seguro de que deseas eliminar el contacto 
              <span class="font-semibold">{{ contactToDelete?.nombre }}</span>?
            </p>
            <p class="mt-2 text-sm text-gray-500">
              Esta acción no se puede deshacer.
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
            <span>{{ deleting ? 'Eliminando...' : 'Eliminar' }}</span>
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ContactList from '@/components/contacts/ContactList.vue'
import ContactForm from '@/components/contacts/ContactForm.vue'
import Modal from '@/components/shared/Modal.vue'
import contactService from '@/services/contactService'

// ============= ESTADO LOCAL =============
const contacts = ref([]) // Lista de todos los contactos
const loading = ref(false) // Estado de carga inicial
const submitting = ref(false) // Estado de envío de formulario
const deleting = ref(false) // Estado de eliminación
const searchQuery = ref('') // Término de búsqueda
const filterType = ref('todos') // Filtro por tipo: 'todos', 'personas', 'empresas'

// Estados del modal de formulario
const isModalOpen = ref(false)
const selectedContact = ref(null)

// Estados del modal de eliminación
const isDeleteModalOpen = ref(false)
const contactToDelete = ref(null)

// ============= COMPUTED =============

/**
 * Detectar si estamos en modo edición
 */
const isEditMode = computed(() => {
  return selectedContact.value !== null
})

/**
 * Contactos filtrados por tipo y búsqueda
 */
const filteredContacts = computed(() => {
  let result = contacts.value

  // Filtrar por tipo
  if (filterType.value === 'personas') {
    result = result.filter(c => c.tipo === 'persona')
  } else if (filterType.value === 'empresas') {
    result = result.filter(c => c.tipo === 'empresa')
  }

  // Filtrar por búsqueda
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    result = result.filter(c => {
      const nombre = c.nombre?.toLowerCase() || ''
      const email = c.email?.toLowerCase() || ''
      const telefono = c.telefono || ''
      
      return nombre.includes(query) || 
             email.includes(query) || 
             telefono.includes(query)
    })
  }

  return result
})

// ============= MÉTODOS =============

/**
 * Cargar lista de contactos desde el backend
 */
const loadContacts = async () => {
  loading.value = true
  try {
    const response = await contactService.getContacts()
    contacts.value = response.data || []
  } catch (error) {
    console.error('Error al cargar contactos:', error)
    // Aquí podrías mostrar un toast de error
  } finally {
    loading.value = false
  }
}

/**
 * Abrir modal para crear nuevo contacto
 */
const openCreateModal = () => {
  selectedContact.value = null
  isModalOpen.value = true
}

/**
 * Abrir modal para editar contacto existente
 */
const openEditModal = (contact) => {
  selectedContact.value = { ...contact }
  isModalOpen.value = true
}

/**
 * Cerrar modal de formulario
 */
const closeModal = () => {
  isModalOpen.value = false
  selectedContact.value = null
}

/**
 * Manejar submit del formulario (crear o actualizar)
 */
const handleSubmit = async (formData) => {
  submitting.value = true
  
  try {
    if (isEditMode.value) {
      // Actualizar contacto existente
      await contactService.updateContact(selectedContact.value.id_contacto, formData)
      console.log('Contacto actualizado exitosamente')
    } else {
      // Crear nuevo contacto
      await contactService.createContact(formData)
      console.log('Contacto creado exitosamente')
    }
    
    // Recargar lista de contactos
    await loadContacts()
    
    // Cerrar modal
    closeModal()
  } catch (error) {
    console.error('Error al guardar contacto:', error)
    // Aquí podrías mostrar un toast de error
  } finally {
    submitting.value = false
  }
}

/**
 * Confirmar eliminación de contacto
 */
const confirmDelete = (contact) => {
  contactToDelete.value = contact
  isDeleteModalOpen.value = true
}

/**
 * Cancelar eliminación
 */
const cancelDelete = () => {
  isDeleteModalOpen.value = false
  contactToDelete.value = null
}

/**
 * Ejecutar eliminación del contacto
 */
const handleDelete = async () => {
  if (!contactToDelete.value) return
  
  deleting.value = true
  
  try {
    await contactService.deleteContact(contactToDelete.value.id_contacto)
    console.log('Contacto eliminado exitosamente')
    
    // Recargar lista de contactos
    await loadContacts()
    
    // Cerrar modal
    cancelDelete()
  } catch (error) {
    console.error('Error al eliminar contacto:', error)
    // Aquí podrías mostrar un toast de error
  } finally {
    deleting.value = false
  }
}

/**
 * Limpiar todos los filtros
 */
const clearFilters = () => {
  searchQuery.value = ''
  filterType.value = 'todos'
}

// ============= LIFECYCLE =============

/**
 * Cargar contactos al montar el componente
 */
onMounted(() => {
  loadContacts()
})
</script>