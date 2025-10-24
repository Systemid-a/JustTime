<!-- ============================================================ -->
<!-- ARCHIVO 13/31: src/components/shared/Modal.vue -->
<!-- Módulo: Componentes Compartidos -->
<!-- Descripción: Modal genérico reutilizable para toda la app -->
<!-- ============================================================ -->

<template>
  <!-- Overlay con backdrop-blur -->
  <Transition name="modal-fade">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
      @click.self="handleClose"
    >
      <!-- Contenedor del modal -->
      <div
        :class="[
          'bg-white rounded-xl shadow-2xl overflow-hidden transition-all duration-300',
          sizeClasses
        ]"
        @click.stop
      >
        <!-- Header del modal -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gray-50">
          <h3 class="text-xl font-semibold text-gray-800">
            {{ title }}
          </h3>
          <button
            @click="handleClose"
            class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
            aria-label="Cerrar modal"
          >
            <X class="w-6 h-6" />
          </button>
        </div>

        <!-- Contenido del modal (slot principal) -->
        <div class="px-6 py-6 overflow-y-auto max-h-[70vh]">
          <slot></slot>
        </div>

        <!-- Footer del modal (slot footer) -->
        <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'
import { X } from 'lucide-vue-next'

// ============= PROPS =============
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
    default: false
  },
  title: {
    type: String,
    default: 'Modal'
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  }
})

// ============= EMITS =============
const emit = defineEmits(['close'])

// ============= COMPUTED =============
/**
 * Clases de tamaño del modal según prop size
 */
const sizeClasses = computed(() => {
  const sizes = {
    sm: 'w-full max-w-md',
    md: 'w-full max-w-2xl',
    lg: 'w-full max-w-4xl',
    xl: 'w-full max-w-6xl'
  }
  return sizes[props.size]
})

// ============= MÉTODOS =============
/**
 * Cerrar modal emitiendo evento
 */
function handleClose() {
  emit('close')
}

/**
 * Manejar tecla ESC para cerrar modal
 */
function handleEscape(event) {
  if (event.key === 'Escape' && props.isOpen) {
    handleClose()
  }
}

// ============= WATCHERS =============
/**
 * Bloquear scroll del body cuando modal está abierto
 */
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    // Bloquear scroll
    document.body.style.overflow = 'hidden'
  } else {
    // Restaurar scroll
    document.body.style.overflow = ''
  }
})

// ============= LIFECYCLE HOOKS =============
onMounted(() => {
  // Agregar listener para ESC
  window.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  // Limpiar listener
  window.removeEventListener('keydown', handleEscape)
  // Restaurar scroll por si acaso
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Animaciones de entrada/salida del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active > div,
.modal-fade-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from > div {
  transform: scale(0.9) translateY(-20px);
}

.modal-fade-leave-to > div {
  transform: scale(0.9) translateY(-20px);
}
</style>