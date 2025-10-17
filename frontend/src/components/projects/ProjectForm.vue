<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">
      {{ isEditMode ? 'Editar Proyecto' : 'Nuevo Proyecto' }}
    </h2>

    <form @submit.prevent="handleSubmit" class="space-y-5">
      <div class="form-group">
        <label for="nombre" class="block text-sm font-semibold text-gray-700 mb-2">
          Nombre del Proyecto *
        </label>
        <input
          id="nombre"
          v-model="formData.nombre"
          type="text"
          required
          minlength="3"
          class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="Ej: Divorcio García vs. García"
        />
        <p v-if="errors.nombre" class="mt-1 text-sm text-red-600">
          {{ errors.nombre }}
        </p>
      </div>

      <div class="form-group">
        <label for="descripcion" class="block text-sm font-semibold text-gray-700 mb-2">
          Descripción
        </label>
        <textarea
          id="descripcion"
          v-model="formData.descripcion"
          rows="4"
          class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
          placeholder="Describe los detalles del proyecto..."
        ></textarea>
        <p class="mt-1 text-xs text-gray-500">
          {{ formData.descripcion?.length || 0 }} / 1000 caracteres
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-group">
          <label for="categoria" class="block text-sm font-semibold text-gray-700 mb-2">
            Categoría *
          </label>
          <select
            id="categoria"
            v-model="formData.categoria"
            required
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          >
            <option value="" disabled>Selecciona una categoría</option>
            <option value="civil">Civil</option>
            <option value="penal">Penal</option>
            <option value="laboral">Laboral</option>
            <option value="comercial">Comercial</option>
            <option value="familia">Familia</option>
          </select>
        </div>

        <div class="form-group">
          <label for="estado" class="block text-sm font-semibold text-gray-700 mb-2">
            Estado *
          </label>
          <select
            id="estado"
            v-model="formData.estado"
            required
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          >
            <option value="activo">Activo</option>
            <option value="pausado">Pausado</option>
            <option value="finalizado">Finalizado</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="contacto_id_fk" class="block text-sm font-semibold text-gray-700 mb-2">
          Cliente
        </label>
        <select
          id="contacto_id_fk"
          v-model="formData.contacto_id_fk"
          class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        >
          <option :value="null">Sin cliente</option>
          <option v-for="contacto in contactos" :key="contacto.id_contacto" :value="contacto.id_contacto">
            {{ contacto.nombre }}
          </option>
        </select>
        <p v-if="loadingContacts" class="mt-1 text-xs text-gray-500">Cargando contactos...</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-group">
          <label for="fecha_inicio" class="block text-sm font-semibold text-gray-700 mb-2">
            Fecha de Inicio
          </label>
          <input
            id="fecha_inicio"
            v-model="formData.fecha_inicio"
            type="date"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>

        <div class="form-group">
          <label for="fecha_fin" class="block text-sm font-semibold text-gray-700 mb-2">
            Fecha de Fin <span class="text-gray-500 font-normal">(opcional)</span>
          </label>
          <input
            id="fecha_fin"
            v-model="formData.fecha_fin"
            type="date"
            :min="formData.fecha_inicio"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>
      </div>

      <div class="border-t border-gray-200 pt-5"></div>

      <div class="flex items-center justify-end gap-3">
        <button
          type="button"
          @click="$emit('cancel')"
          :disabled="loading"
          class="px-6 py-2.5 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancelar
        </button>
        <button
          type="submit"
          :disabled="loading || !isFormValid"
          class="px-6 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <svg v-if="loading" class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Guardando...' : 'Guardar Proyecto' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import contactService from '@/services/contactService'

const props = defineProps({
  project: { type: Object, default: null }
})

const emit = defineEmits(['save', 'cancel'])

const loading = ref(false)
const errors = ref({})
const contactos = ref([])
const loadingContacts = ref(false)

const formData = ref({
  nombre: '',
  descripcion: '',
  categoria: '',
  estado: 'activo',
  contacto_id_fk: null,
  fecha_inicio: new Date().toISOString().split('T')[0],
  fecha_fin: null
})

const isEditMode = computed(() => {
  return props.project !== null
})

const isFormValid = computed(() => {
  return (
    formData.value.nombre?.trim().length >= 3 &&
    formData.value.categoria !== '' &&
    formData.value.estado !== ''
  )
})

watch(
  () => props.project,
  (newProject) => {
    if (newProject) {
      formData.value = {
        nombre: newProject.nombre || '',
        descripcion: newProject.descripcion || '',
        categoria: newProject.categoria || '',
        estado: newProject.estado || 'activo',
        contacto_id_fk: newProject.contacto_id_fk || null,
        fecha_inicio: newProject.fecha_inicio || new Date().toISOString().split('T')[0],
        fecha_fin: newProject.fecha_fin || null
      }
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

async function loadContacts() {
  loadingContacts.value = true
  try {
    const response = await contactService.getActiveContacts()
    if (response.success && response.data) {
      contactos.value = response.data
    }
  } catch (error) {
    console.error('Error al cargar contactos:', error)
  } finally {
    loadingContacts.value = false
  }
}

async function handleSubmit() {
  errors.value = {}
  
  if (!formData.value.nombre || formData.value.nombre.trim().length < 3) {
    errors.value.nombre = 'El nombre debe tener al menos 3 caracteres'
    return
  }
  
  if (!formData.value.categoria) {
    errors.value.categoria = 'Debes seleccionar una categoría'
    return
  }
  
  if (formData.value.fecha_fin && formData.value.fecha_inicio) {
    const fechaInicio = new Date(formData.value.fecha_inicio)
    const fechaFin = new Date(formData.value.fecha_fin)
    
    if (fechaFin < fechaInicio) {
      errors.value.fecha_fin = 'La fecha de fin no puede ser anterior a la fecha de inicio'
      return
    }
  }
  
  const dataToSend = {
    nombre: formData.value.nombre.trim(),
    descripcion: formData.value.descripcion?.trim() || null,
    categoria: formData.value.categoria,
    estado: formData.value.estado,
    contacto_id_fk: formData.value.contacto_id_fk || null,
    fecha_inicio: formData.value.fecha_inicio || null,
    fecha_fin: formData.value.fecha_fin || null
  }
  
  loading.value = true
  
  try {
    emit('save', dataToSend)
  } catch (error) {
    console.error('Error al guardar proyecto:', error)
    errors.value.general = 'Hubo un error al guardar el proyecto'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  formData.value = {
    nombre: '',
    descripcion: '',
    categoria: '',
    estado: 'activo',
    contacto_id_fk: null,
    fecha_inicio: new Date().toISOString().split('T')[0],
    fecha_fin: null
  }
  errors.value = {}
}

onMounted(() => {
  loadContacts()
})
</script>