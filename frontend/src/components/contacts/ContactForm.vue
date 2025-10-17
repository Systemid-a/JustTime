<!-- ============================================================
     ARCHIVO 11/31: src/components/contacts/ContactForm.vue
     Módulo: Contactos
     Descripción: Formulario adaptativo para crear/editar contactos
     ============================================================ -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Tipo de Contacto -->
    <div>
      <label for="tipo" class="block text-sm font-medium text-gray-700 mb-2">
        Tipo de Contacto *
      </label>
      <div class="grid grid-cols-2 gap-3">
        <button
          type="button"
          @click="formData.tipo = 'persona'"
          :class="[
            'flex items-center justify-center px-4 py-3 border-2 rounded-lg transition-all',
            formData.tipo === 'persona'
              ? 'border-blue-500 bg-blue-50 text-blue-700'
              : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
          ]"
        >
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
          </svg>
          <span class="font-medium">Persona</span>
        </button>
        <button
          type="button"
          @click="formData.tipo = 'empresa'"
          :class="[
            'flex items-center justify-center px-4 py-3 border-2 rounded-lg transition-all',
            formData.tipo === 'empresa'
              ? 'border-green-500 bg-green-50 text-green-700'
              : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
          ]"
        >
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd" />
          </svg>
          <span class="font-medium">Empresa</span>
        </button>
      </div>
    </div>

    <!-- Nombre / Razón Social (Adaptativo) -->
    <div>
      <label for="nombre" class="block text-sm font-medium text-gray-700 mb-2">
        {{ nombreLabel }}
      </label>
      <input
        id="nombre"
        v-model="formData.nombre"
        type="text"
        required
        :placeholder="nombrePlaceholder"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        :class="{ 'border-red-500': errors.nombre }"
      />
      <p v-if="errors.nombre" class="mt-1 text-sm text-red-600">
        {{ errors.nombre }}
      </p>
    </div>

    <!-- Email -->
    <div>
      <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
        Correo Electrónico
      </label>
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <input
          id="email"
          v-model="formData.email"
          type="email"
          placeholder="ejemplo@correo.com"
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          :class="{ 'border-red-500': errors.email }"
        />
      </div>
      <p v-if="errors.email" class="mt-1 text-sm text-red-600">
        {{ errors.email }}
      </p>
    </div>

    <!-- Teléfono -->
    <div>
      <label for="telefono" class="block text-sm font-medium text-gray-700 mb-2">
        Teléfono
      </label>
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </div>
        <input
          id="telefono"
          v-model="formData.telefono"
          type="tel"
          placeholder="5551-2345"
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
      </div>
    </div>

    <!-- Dirección -->
    <div>
      <label for="direccion" class="block text-sm font-medium text-gray-700 mb-2">
        Dirección
      </label>
      <div class="relative">
        <div class="absolute top-3 left-3 pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <textarea
          id="direccion"
          v-model="formData.direccion"
          rows="3"
          placeholder="Zona 10, Ciudad de Guatemala"
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
        ></textarea>
      </div>
    </div>

    <!-- Estado Activo -->
    <div class="flex items-center">
      <input
        id="activo"
        v-model="formData.activo"
        type="checkbox"
        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
      />
      <label for="activo" class="ml-2 block text-sm text-gray-900">
        Contacto activo
      </label>
    </div>

    <!-- Divider -->
    <div class="border-t border-gray-200"></div>

    <!-- Botones de Acción -->
    <div class="flex justify-end gap-3">
      <button
        type="button"
        @click="$emit('cancel')"
        :disabled="loading"
        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Cancelar
      </button>
      <button
        type="submit"
        :disabled="loading || !isFormValid"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <svg 
          v-if="loading" 
          class="animate-spin h-4 w-4 text-white" 
          fill="none" 
          viewBox="0 0 24 24"
        >
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ loading ? 'Guardando...' : (isEditMode ? 'Actualizar' : 'Guardar') }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// ============= PROPS =============
const props = defineProps({
  contact: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// ============= EMITS =============
const emit = defineEmits(['submit', 'cancel'])

// ============= ESTADO LOCAL =============
const formData = ref({
  nombre: '',
  email: '',
  telefono: '',
  tipo: 'persona',
  direccion: '',
  activo: true
})

const errors = ref({
  nombre: '',
  email: ''
})

// ============= COMPUTED =============

/**
 * Detectar si estamos en modo edición
 */
const isEditMode = computed(() => {
  return props.contact !== null
})

/**
 * Label adaptativo para el campo nombre según el tipo
 */
const nombreLabel = computed(() => {
  return formData.value.tipo === 'persona' 
    ? 'Nombre Completo *' 
    : 'Razón Social *'
})

/**
 * Placeholder adaptativo para el campo nombre según el tipo
 */
const nombrePlaceholder = computed(() => {
  return formData.value.tipo === 'persona'
    ? 'Ej: Ana María García López'
    : 'Ej: Bufete Jurídico López & Asociados'
})

/**
 * Validar si el formulario es válido
 */
const isFormValid = computed(() => {
  return formData.value.nombre.trim().length > 0
})

// ============= WATCHERS =============

/**
 * Cargar datos del contacto en modo edición
 */
watch(
  () => props.contact,
  (newContact) => {
    if (newContact) {
      formData.value = {
        nombre: newContact.nombre || '',
        email: newContact.email || '',
        telefono: newContact.telefono || '',
        tipo: newContact.tipo || 'persona',
        direccion: newContact.direccion || '',
        activo: newContact.activo !== undefined ? newContact.activo : true
      }
    }
  },
  { immediate: true }
)

/**
 * Validar nombre en tiempo real
 */
watch(
  () => formData.value.nombre,
  (newNombre) => {
    if (newNombre.trim().length === 0) {
      errors.value.nombre = 'El nombre es obligatorio'
    } else if (newNombre.trim().length < 3) {
      errors.value.nombre = 'El nombre debe tener al menos 3 caracteres'
    } else {
      errors.value.nombre = ''
    }
  }
)

/**
 * Validar email en tiempo real
 */
watch(
  () => formData.value.email,
  (newEmail) => {
    if (newEmail && newEmail.trim().length > 0) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(newEmail)) {
        errors.value.email = 'El formato del email no es válido'
      } else {
        errors.value.email = ''
      }
    } else {
      errors.value.email = ''
    }
  }
)

// ============= MÉTODOS =============

/**
 * Manejar submit del formulario
 */
const handleSubmit = () => {
  // Validar antes de enviar
  if (!isFormValid.value) {
    return
  }

  // Validar email si existe
  if (formData.value.email && errors.value.email) {
    return
  }

  // Limpiar datos vacíos opcionales
  const dataToSubmit = {
    ...formData.value,
    email: formData.value.email.trim() || null,
    telefono: formData.value.telefono.trim() || null,
    direccion: formData.value.direccion.trim() || null
  }

  emit('submit', dataToSubmit)
}
</script>