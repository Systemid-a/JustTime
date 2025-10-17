<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
      <!-- Header -->
      <div class="flex items-center space-x-3 p-6 border-b border-gray-200">
        <component 
          :is="iconComponent" 
          :class="iconColorClass"
          class="h-6 w-6"
        />
        <h3 class="text-xl font-semibold text-gray-900">{{ title }}</h3>
      </div>

      <!-- Contenido -->
      <div class="p-6">
        <p class="text-gray-600">{{ message }}</p>
      </div>

      <!-- Botones -->
      <div class="flex items-center justify-end space-x-3 p-6 bg-gray-50 border-t border-gray-200">
        <button
          @click="$emit('cancel')"
          :disabled="loading"
          class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-white font-medium transition-colors disabled:opacity-50"
        >
          {{ cancelText }}
        </button>
        <button
          @click="$emit('confirm')"
          :disabled="loading"
          :class="[
            'px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center',
            confirmButtonClass
          ]"
        >
          <Loader2 v-if="loading" class="h-5 w-5 mr-2 animate-spin" />
          {{ loading ? loadingText : confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { AlertCircle, AlertTriangle, Info, CheckCircle, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    default: 'Confirmar acción'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  },
  loadingText: {
    type: String,
    default: 'Procesando...'
  },
  type: {
    type: String,
    default: 'warning', // 'danger', 'warning', 'info', 'success'
    validator: (value) => ['danger', 'warning', 'info', 'success'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['confirm', 'cancel'])

// Computed properties para estilos dinámicos
const iconComponent = computed(() => {
  const icons = {
    danger: AlertCircle,
    warning: AlertTriangle,
    info: Info,
    success: CheckCircle
  }
  return icons[props.type] || AlertTriangle
})

const iconColorClass = computed(() => {
  const colors = {
    danger: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
    success: 'text-green-600'
  }
  return colors[props.type] || 'text-yellow-600'
})

const confirmButtonClass = computed(() => {
  const classes = {
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    warning: 'bg-yellow-600 hover:bg-yellow-700 text-white',
    info: 'bg-blue-600 hover:bg-blue-700 text-white',
    success: 'bg-green-600 hover:bg-green-700 text-white'
  }
  return classes[props.type] || 'bg-yellow-600 hover:bg-yellow-700 text-white'
})
</script>