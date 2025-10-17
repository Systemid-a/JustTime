<!-- ============================================================ -->
<!-- ARCHIVO 15/31: src/pages/LoginPage.vue -->
<!-- Módulo: Páginas -->
<!-- Descripción: Página de autenticación con diseño profesional -->
<!-- ============================================================ -->

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 via-blue-500 to-purple-500 px-4">
    <!-- Tarjeta de Login -->
    <div class="w-full max-w-md">
      <div class="bg-white rounded-2xl shadow-2xl p-8">
        <!-- Logo y Título -->
        <div class="text-center mb-8">
          <div class="text-6xl mb-4">⚖️</div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">JustTime</h1>
          <p class="text-gray-600">Sistema de Gestión Jurídica</p>
        </div>

        <!-- Mensaje de error -->
        <div 
          v-if="errorMessage" 
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3"
        >
          <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p class="text-sm text-red-700">{{ errorMessage }}</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Campo Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                autocomplete="email"
                placeholder="ejemplo@correo.com"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                :class="{ 'border-red-300 bg-red-50': errors.email }"
                @input="clearFieldError('email')"
              />
            </div>
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
          </div>

          <!-- Campo Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="••••••••"
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                :class="{ 'border-red-300 bg-red-50': errors.password }"
                @input="clearFieldError('password')"
              />
              <!-- Botón mostrar/ocultar password -->
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Eye v-if="!showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
                <EyeOff v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
          </div>

          <!-- Botón Submit -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-md transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
            <span>{{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
          </button>
        </form>

        <!-- Footer -->
        <div class="mt-6 text-center text-sm text-gray-600">
          <p>¿Olvidaste tu contraseña? <a href="#" class="text-indigo-600 hover:text-indigo-700 font-medium">Recuperar</a></p>
        </div>
      </div>

      <!-- Información adicional -->
      <div class="mt-4 text-center text-white text-sm">
        <p>© 2025 JustTime - Sistema de Gestión Jurídica</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { Mail, Lock, Eye, EyeOff, Loader2, AlertCircle } from 'lucide-vue-next'
import { REGEX, MENSAJES_ERROR } from '@/utils/constants'

// ============= COMPOSABLES =============
const router = useRouter()
const authStore = useAuthStore()

// ============= ESTADO =============
const formData = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

// ============= MÉTODOS =============

/**
 * Validar formulario antes de enviar
 */
function validateForm() {
  let isValid = true
  
  // Limpiar errores previos
  errors.email = ''
  errors.password = ''
  errorMessage.value = ''

  // Validar email
  if (!formData.email.trim()) {
    errors.email = 'El correo electrónico es requerido'
    isValid = false
  } else if (!REGEX.EMAIL.test(formData.email)) {
    errors.email = 'Formato de correo inválido'
    isValid = false
  }

  // Validar password
  if (!formData.password) {
    errors.password = 'La contraseña es requerida'
    isValid = false
  } else if (formData.password.length < 6) {
    errors.password = 'La contraseña debe tener al menos 6 caracteres'
    isValid = false
  }

  return isValid
}

/**
 * Limpiar error de un campo específico
 */
function clearFieldError(field) {
  errors[field] = ''
  errorMessage.value = ''
}

/**
 * Manejar submit del formulario
 */
async function handleSubmit() {
  // Validar formulario
  if (!validateForm()) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    // Llamar al store de autenticación
    await authStore.login(formData.email, formData.password)
    
    // Si el login es exitoso, redirigir al dashboard
    router.push('/dashboard')
  } catch (error) {
    // Mostrar mensaje de error user-friendly
    if (error.status === 401) {
      errorMessage.value = MENSAJES_ERROR.AUTENTICACION
    } else if (error.status === 0) {
      errorMessage.value = MENSAJES_ERROR.RED
    } else {
      errorMessage.value = error.message || MENSAJES_ERROR.SERVIDOR
    }
  } finally {
    isLoading.value = false
  }
}
</script>