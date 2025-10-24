<!-- ============================================================
     ARCHIVO: src/components/employees/EmployeeForm.vue
     Módulo: Componentes / Empleados
     Descripción: Formulario para crear/editar empleado (sin usuario)
     ============================================================ -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <!-- Nombre -->
    <div>
      <label for="nombre" class="block text-sm font-medium text-gray-700 mb-1">
        Nombre completo <span class="text-red-500">*</span>
      </label>
      <input
        id="nombre"
        v-model="form.nombre"
        type="text"
        required
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="Ej: María González López"
      />
    </div>

    <!-- Teléfono -->
    <div>
      <label for="telefono" class="block text-sm font-medium text-gray-700 mb-1">
        Teléfono
      </label>
      <input
        id="telefono"
        v-model="form.telefono"
        type="tel"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="Ej: 5551-2345"
      />
    </div>

    <!-- Puesto -->
    <div>
      <label for="puesto" class="block text-sm font-medium text-gray-700 mb-1">
        Puesto
      </label>
      <input
        id="puesto"
        v-model="form.puesto"
        type="text"
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="Ej: Abogada Senior"
      />
    </div>

    <!-- Nota informativa -->
    <div class="bg-blue-50 border-l-4 border-blue-400 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-blue-700">
            Este empleado no tendrá acceso al sistema. Para crear un empleado con usuario y permisos, usa el botón "Con Usuario".
          </p>
        </div>
      </div>
    </div>

    <!-- Botones -->
    <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
      <button
        type="button"
        @click="$emit('cancel')"
        :disabled="loading"
        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
      >
        Cancelar
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
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
        <span>{{ loading ? 'Guardando...' : (employee ? 'Actualizar' : 'Crear Empleado') }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

// ============= PROPS =============
const props = defineProps({
  employee: {
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

// ============= STATE =============
const form = ref({
  nombre: '',
  telefono: '',
  puesto: ''
})

// ============= MÉTODOS =============

/**
 * Inicializar formulario con datos del empleado (si existe)
 */
function initForm() {
  if (props.employee) {
    form.value = {
      nombre: props.employee.nombre || '',
      telefono: props.employee.telefono || '',
      puesto: props.employee.puesto || ''
    }
  } else {
    form.value = {
      nombre: '',
      telefono: '',
      puesto: ''
    }
  }
}

/**
 * Enviar formulario
 */
function handleSubmit() {
  // Limpiar datos vacíos
  const data = {
    nombre: form.value.nombre.trim(),
    telefono: form.value.telefono.trim() || null,
    puesto: form.value.puesto.trim() || null
  }

  emit('submit', data)
}

// ============= WATCHERS =============
watch(() => props.employee, () => {
  initForm()
}, { immediate: true })
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