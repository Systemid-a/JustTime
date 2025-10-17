<!-- ============================================================
     ARCHIVO 10/31: src/components/contacts/ContactList.vue
     Módulo: Contactos
     Descripción: Tabla responsive de contactos con badges y acciones
     ============================================================ -->

<template>
  <div class="bg-white rounded-lg shadow overflow-hidden">
    <!-- Tabla responsive -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <!-- Encabezado -->
        <thead class="bg-gray-50">
          <tr>
            <th 
              scope="col" 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              @click="sortBy('nombre')"
            >
              <div class="flex items-center gap-2">
                Nombre
                <svg v-if="sortField === 'nombre'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" 
                  />
                </svg>
              </div>
            </th>
            <th 
              scope="col" 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              @click="sortBy('tipo')"
            >
              <div class="flex items-center gap-2">
                Tipo
                <svg v-if="sortField === 'tipo'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" 
                  />
                </svg>
              </div>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Teléfono
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Estado
            </th>
            <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>

        <!-- Cuerpo de la tabla -->
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Mensaje cuando no hay contactos -->
          <tr v-if="sortedContacts.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p class="mt-2 text-sm">No hay contactos para mostrar</p>
            </td>
          </tr>

          <!-- Filas de contactos -->
          <tr 
            v-for="contact in sortedContacts" 
            :key="contact.id_contacto"
            class="hover:bg-gray-50 cursor-pointer transition-colors"
            @click="$emit('edit-contact', contact)"
          >
            <!-- Nombre -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                  <span class="text-white font-semibold text-sm">
                    {{ getInitials(contact.nombre) }}
                  </span>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ contact.nombre }}
                  </div>
                  <div v-if="contact.direccion" class="text-sm text-gray-500 truncate max-w-xs">
                    {{ contact.direccion }}
                  </div>
                </div>
              </div>
            </td>

            <!-- Tipo (Badge) -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  contact.tipo === 'persona' 
                    ? 'bg-blue-100 text-blue-800' 
                    : 'bg-green-100 text-green-800'
                ]"
              >
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path 
                    v-if="contact.tipo === 'persona'"
                    fill-rule="evenodd" 
                    d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" 
                    clip-rule="evenodd" 
                  />
                  <path 
                    v-else
                    fill-rule="evenodd" 
                    d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" 
                    clip-rule="evenodd" 
                  />
                </svg>
                {{ contact.tipo === 'persona' ? 'Persona' : 'Empresa' }}
              </span>
            </td>

            <!-- Email -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">
                {{ contact.email || '-' }}
              </div>
            </td>

            <!-- Teléfono -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">
                {{ contact.telefono || '-' }}
              </div>
            </td>

            <!-- Estado (Badge) -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  contact.activo 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-gray-100 text-gray-800'
                ]"
              >
                <span 
                  :class="[
                    'w-2 h-2 rounded-full mr-1.5',
                    contact.activo ? 'bg-green-500' : 'bg-gray-400'
                  ]"
                ></span>
                {{ contact.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>

            <!-- Acciones -->
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click.stop="$emit('edit-contact', contact)"
                class="text-blue-600 hover:text-blue-900 mr-3"
                title="Editar contacto"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click.stop="$emit('delete-contact', contact)"
                class="text-red-600 hover:text-red-900"
                title="Eliminar contacto"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Footer con contador -->
    <div class="bg-gray-50 px-6 py-3 border-t border-gray-200">
      <p class="text-sm text-gray-700">
        Mostrando <span class="font-medium">{{ sortedContacts.length }}</span> 
        {{ sortedContacts.length === 1 ? 'contacto' : 'contactos' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

// ============= PROPS =============
const props = defineProps({
  contacts: {
    type: Array,
    required: true,
    default: () => []
  }
})

// ============= EMITS =============
defineEmits(['edit-contact', 'delete-contact'])

// ============= ESTADO LOCAL =============
const sortField = ref('nombre') // Campo actual de ordenamiento
const sortOrder = ref('asc') // Orden: 'asc' o 'desc'

// ============= COMPUTED =============

/**
 * Contactos ordenados según campo y orden seleccionados
 */
const sortedContacts = computed(() => {
  const contacts = [...props.contacts]
  
  return contacts.sort((a, b) => {
    let aValue = a[sortField.value]
    let bValue = b[sortField.value]
    
    // Manejar valores nulos
    if (aValue === null || aValue === undefined) aValue = ''
    if (bValue === null || bValue === undefined) bValue = ''
    
    // Convertir a minúsculas para comparación
    if (typeof aValue === 'string') aValue = aValue.toLowerCase()
    if (typeof bValue === 'string') bValue = bValue.toLowerCase()
    
    // Comparar según orden
    if (sortOrder.value === 'asc') {
      return aValue > bValue ? 1 : -1
    } else {
      return aValue < bValue ? 1 : -1
    }
  })
})

// ============= MÉTODOS =============

/**
 * Obtener iniciales del nombre para el avatar
 * @param {String} nombre - Nombre completo
 * @returns {String} Iniciales (máximo 2 caracteres)
 */
const getInitials = (nombre) => {
  if (!nombre) return '?'
  
  const words = nombre.trim().split(' ')
  if (words.length === 1) {
    return words[0].substring(0, 2).toUpperCase()
  }
  
  return (words[0][0] + words[words.length - 1][0]).toUpperCase()
}

/**
 * Cambiar ordenamiento de la tabla
 * @param {String} field - Campo por el cual ordenar
 */
const sortBy = (field) => {
  if (sortField.value === field) {
    // Si es el mismo campo, cambiar orden
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Si es diferente campo, ordenar ascendente
    sortField.value = field
    sortOrder.value = 'asc'
  }
}
</script>