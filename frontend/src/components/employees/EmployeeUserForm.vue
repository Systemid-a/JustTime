<!-- ============================================================
     ARCHIVO: src/components/employees/EmployeeUserForm.vue
     Módulo: Componentes / Empleados
     Descripción: Formulario para crear empleado CON usuario y rol
     ============================================================ -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Sección: Datos del Empleado -->
    <div class="space-y-4">
      <h3 class="text-lg font-medium text-gray-900 border-b pb-2">
        Datos del Empleado
      </h3>

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

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
      </div>
    </div>

    <!-- Sección: Credenciales de Usuario -->
    <div class="space-y-4">
      <h3 class="text-lg font-medium text-gray-900 border-b pb-2">
        Credenciales de Acceso
      </h3>

      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
          Email <span class="text-red-500">*</span>
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Ej: maria@justtime.com"
        />
        <p class="mt-1 text-xs text-gray-500">
          Este será el usuario para iniciar sesión
        </p>
      </div>

      <!-- Contraseña -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
          Contraseña <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            minlength="6"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-10"
            placeholder="Mínimo 6 caracteres"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
          >
            <svg v-if="!showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
            </svg>
          </button>
        </div>
        <p class="mt-1 text-xs text-gray-500">
          Mínimo 6 caracteres. El empleado podrá cambiarla después.
        </p>
      </div>

      <!-- Rol del Usuario -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Rol del Usuario <span class="text-red-500">*</span>
        </label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <!-- Opción: Usuario -->
          <label
            :class="[
              'relative flex flex-col p-4 border-2 rounded-lg cursor-pointer transition-all',
              form.rol === 'usuario'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            ]"
          >
            <input
              type="radio"
              v-model="form.rol"
              value="usuario"
              class="sr-only"
              required
            />
            <div class="flex items-center gap-3">
              <div class="flex-shrink-0">
                <div :class="[
                  'w-12 h-12 rounded-full flex items-center justify-center',
                  form.rol === 'usuario' ? 'bg-blue-100' : 'bg-gray-100'
                ]">
                  <svg class="w-6 h-6" :class="form.rol === 'usuario' ? 'text-blue-600' : 'text-gray-400'" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold" :class="form.rol === 'usuario' ? 'text-blue-900' : 'text-gray-900'">
                    Usuario
                  </span>
                  <svg v-if="form.rol === 'usuario'" class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <p class="text-xs mt-1" :class="form.rol === 'usuario' ? 'text-blue-700' : 'text-gray-500'">
                  Solo puede ver información sin modificar
                </p>
              </div>
            </div>
          </label>

          <!-- Opción: Administrador -->
          <label
            :class="[
              'relative flex flex-col p-4 border-2 rounded-lg cursor-pointer transition-all',
              form.rol === 'admin'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            ]"
          >
            <input
              type="radio"
              v-model="form.rol"
              value="admin"
              class="sr-only"
            />
            <div class="flex items-center gap-3">
              <div class="flex-shrink-0">
                <div :class="[
                  'w-12 h-12 rounded-full flex items-center justify-center',
                  form.rol === 'admin' ? 'bg-purple-100' : 'bg-gray-100'
                ]">
                  <svg class="w-6 h-6" :class="form.rol === 'admin' ? 'text-purple-600' : 'text-gray-400'" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold" :class="form.rol === 'admin' ? 'text-purple-900' : 'text-gray-900'">
                    Administrador
                  </span>
                  <svg v-if="form.rol === 'admin'" class="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <p class="text-xs mt-1" :class="form.rol === 'admin' ? 'text-purple-700' : 'text-gray-500'">
                  Puede crear, modificar y eliminar
                </p>
              </div>
            </div>
          </label>
        </div>
      </div>
    </div>

    <!-- Nota de Seguridad -->
    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-yellow-700">
            <span class="font-medium">Importante:</span> Este empleado tendrá acceso al sistema con el rol seleccionado. Asegúrate de elegir el rol correcto.
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
        <span>{{ loading ? 'Creando...' : 'Crear Empleado con Usuario' }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'

// ============= PROPS =============
defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

// ============= EMITS =============
const emit = defineEmits(['submit', 'cancel'])

// ============= STATE =============
const showPassword = ref(false)
const form = ref({
  nombre: '',
  telefono: '',
  puesto: '',
  email: '',
  password: '',
  rol: 'usuario' // Por defecto: usuario
})

// ============= MÉTODOS =============

/**
 * Enviar formulario
 */
function handleSubmit() {
  // Validar que se haya seleccionado un rol
  if (!form.value.rol) {
    alert('Por favor selecciona un rol para el usuario')
    return
  }

  // Limpiar y preparar datos
  const data = {
    nombre: form.value.nombre.trim(),
    telefono: form.value.telefono.trim() || null,
    puesto: form.value.puesto.trim() || null,
    email: form.value.email.trim(),
    password: form.value.password,
    rol: form.value.rol
  }

  emit('submit', data)
}
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

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>