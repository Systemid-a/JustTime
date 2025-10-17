<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <Edit class="h-6 w-6 text-indigo-600" />
          <h3 class="text-xl font-semibold text-gray-900">Editar Plantilla</h3>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X class="h-6 w-6" />
        </button>
      </div>

      <!-- Formulario -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        
        <!-- Nombre -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Nombre de la plantilla *
          </label>
          <input
            v-model="formData.nombre"
            type="text"
            required
            placeholder="Ej: Contrato de servicios"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <!-- Categoría -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Categoría
          </label>
          <select
            v-model="formData.categoria"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">Seleccionar categoría</option>
            <option value="contrato">Contrato</option>
            <option value="demanda">Demanda</option>
            <option value="escritura">Escritura</option>
            <option value="poder">Poder</option>
            <option value="memorial">Memorial</option>
            <option value="dictamen">Dictamen</option>
            <option value="otro">Otro</option>
          </select>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Descripción
          </label>
          <textarea
            v-model="formData.descripcion"
            rows="3"
            placeholder="Descripción opcional..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          ></textarea>
        </div>

        <!-- Estado -->
        <div class="flex items-center">
          <input
            v-model="formData.activo"
            type="checkbox"
            id="activo"
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label for="activo" class="ml-2 block text-sm text-gray-900">
            Plantilla activa
          </label>
        </div>

        <!-- Mensaje de error -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <AlertCircle class="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p class="text-sm text-red-700">{{ errorMessage }}</p>
          </div>
        </div>

        <!-- Botones -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="updating || !formData.nombre"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            <Loader2 v-if="updating" class="h-5 w-5 mr-2 animate-spin" />
            <Save v-else class="h-5 w-5 mr-2" />
            {{ updating ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Edit, X, Loader2, AlertCircle, Save } from 'lucide-vue-next'
import templateService from '@/services/templateService'

const props = defineProps({
  template: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'updated'])

// Estado
const updating = ref(false)
const errorMessage = ref('')

const formData = ref({
  nombre: '',
  categoria: '',
  descripcion: '',
  activo: true
})

// Cargar datos iniciales
onMounted(() => {
  if (props.template) {
    formData.value = {
      nombre: props.template.nombre || '',
      categoria: props.template.categoria || '',
      descripcion: props.template.descripcion || '',
      activo: props.template.activo ?? true
    }
  }
})

// Submit
const handleSubmit = async () => {
  if (!formData.value.nombre) {
    errorMessage.value = 'El nombre es obligatorio'
    return
  }

  updating.value = true
  errorMessage.value = ''

  try {
    const response = await templateService.updateTemplate(
      props.template.id_plantilla,
      formData.value
    )
    
    if (response.success) {
      emit('updated', response.data)
      emit('close')
    } else {
      errorMessage.value = response.message || 'Error al actualizar'
    }
  } catch (error) {
    console.error('Error al actualizar plantilla:', error)
    errorMessage.value = error.response?.data?.detail || 'Error al actualizar plantilla'
  } finally {
    updating.value = false
  }
}
</script>