<!-- ============================================================ -->
<!-- ARCHIVO: src/pages/ConfigurationPage.vue -->
<!-- Módulo: Páginas -->
<!-- Descripción: Página de configuración del usuario -->
<!-- ============================================================ -->

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Configuración</h2>
          <p class="text-sm text-gray-500 mt-1">
            Personaliza tu experiencia en JustTime
          </p>
        </div>
        
        <!-- Indicador de cambios guardados -->
        <div
          v-if="showSaveNotification"
          class="flex items-center gap-2 text-green-600 animate-fade-in"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span class="text-sm font-medium">Cambios guardados</span>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="flex-1 overflow-auto p-6 bg-gray-50">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Cargando configuración...</p>
        </div>
      </div>

      <!-- Formulario de Configuración -->
      <div v-else class="max-w-4xl mx-auto space-y-6">
        <!-- Sección: Apariencia -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-blue-100 rounded-lg">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-800">Apariencia</h3>
                <p class="text-sm text-gray-600">Personaliza la interfaz visual</p>
              </div>
            </div>
          </div>

          <div class="p-6 space-y-4">
            <!-- Tema -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">
                Tema de la interfaz
              </label>
              <div class="grid grid-cols-2 gap-4">
                <!-- Opción: Tema Claro -->
                <button
                  @click="handleThemeChange('claro')"
                  :class="[
                    'relative p-4 rounded-lg border-2 transition-all',
                    formData.tema === 'claro'
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  ]"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex-shrink-0 w-12 h-12 rounded-lg bg-white border-2 border-gray-200 flex items-center justify-center">
                      <svg class="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    </div>
                    <div class="flex-1 text-left">
                      <div class="font-medium text-gray-900">Claro</div>
                      <div class="text-xs text-gray-500">Tema predeterminado</div>
                    </div>
                  </div>
                  <div
                    v-if="formData.tema === 'claro'"
                    class="absolute top-2 right-2 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center"
                  >
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </button>

                <!-- Opción: Tema Oscuro -->
                <button
                  @click="handleThemeChange('oscuro')"
                  :class="[
                    'relative p-4 rounded-lg border-2 transition-all',
                    formData.tema === 'oscuro'
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  ]"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex-shrink-0 w-12 h-12 rounded-lg bg-gray-800 border-2 border-gray-700 flex items-center justify-center">
                      <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    </div>
                    <div class="flex-1 text-left">
                      <div class="font-medium text-gray-900">Oscuro</div>
                      <div class="text-xs text-gray-500">Reduce la fatiga visual</div>
                    </div>
                  </div>
                  <div
                    v-if="formData.tema === 'oscuro'"
                    class="absolute top-2 right-2 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center"
                  >
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección: Idioma -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-800">Idioma</h3>
                <p class="text-sm text-gray-600">Configura el idioma de la interfaz</p>
              </div>
            </div>
          </div>

          <div class="p-6">
            <div class="grid grid-cols-2 gap-4">
              <!-- Español -->
              <button
                @click="handleLanguageChange('es')"
                :class="[
                  'relative p-4 rounded-lg border-2 transition-all',
                  formData.idioma === 'es'
                    ? 'border-green-600 bg-green-50'
                    : 'border-gray-300 hover:border-gray-400'
                ]"
              >
                <div class="flex items-center gap-3">
                  <div class="flex-shrink-0 text-3xl">🇪🇸</div>
                  <div class="flex-1 text-left">
                    <div class="font-medium text-gray-900">Español</div>
                    <div class="text-xs text-gray-500">Spanish</div>
                  </div>
                </div>
                <div
                  v-if="formData.idioma === 'es'"
                  class="absolute top-2 right-2 w-6 h-6 bg-green-600 rounded-full flex items-center justify-center"
                >
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </button>

              <!-- English -->
              <button
                @click="handleLanguageChange('en')"
                :class="[
                  'relative p-4 rounded-lg border-2 transition-all',
                  formData.idioma === 'en'
                    ? 'border-green-600 bg-green-50'
                    : 'border-gray-300 hover:border-gray-400'
                ]"
              >
                <div class="flex items-center gap-3">
                  <div class="flex-shrink-0 text-3xl">🇬🇧</div>
                  <div class="flex-1 text-left">
                    <div class="font-medium text-gray-900">English</div>
                    <div class="text-xs text-gray-500">Inglés</div>
                  </div>
                </div>
                <div
                  v-if="formData.idioma === 'en'"
                  class="absolute top-2 right-2 w-6 h-6 bg-green-600 rounded-full flex items-center justify-center"
                >
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Sección: Información del Usuario (Solo lectura) -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-purple-50 to-pink-50 px-6 py-4 border-b border-gray-200">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-800">Perfil de Usuario</h3>
                <p class="text-sm text-gray-600">Información de tu cuenta</p>
              </div>
            </div>
          </div>

          <div class="p-6 space-y-4">
            <!-- Rol -->
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-white rounded-lg">
                  <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-700">Rol en el sistema</div>
                  <div class="text-xs text-gray-500">Tu nivel de acceso</div>
                </div>
              </div>
              <span
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium',
                  formData.rol === 'admin'
                    ? 'bg-red-100 text-red-700'
                    : 'bg-blue-100 text-blue-700'
                ]"
              >
                {{ formData.rol === 'admin' ? '👑 Administrador' : '👤 Usuario' }}
              </span>
            </div>

            <!-- Info adicional -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="flex-1">
                  <h4 class="text-sm font-medium text-blue-900 mb-1">Sobre los roles</h4>
                  <p class="text-xs text-blue-700">
                    Los administradores tienen acceso completo al sistema. Los usuarios regulares tienen acceso limitado. 
                    Contacta a un administrador si necesitas cambiar tu rol.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useConfigStore } from '@/stores/configStore'
import { useAuthStore } from '@/stores/authStore'

// ============= STORES =============
const configStore = useConfigStore()
const authStore = useAuthStore()

// ============= STATE =============
const loading = ref(false)
const showSaveNotification = ref(false)

const formData = reactive({
  idioma: 'es',
  rol: 'usuario',
  tema: 'claro'
})

// ============= MÉTODOS =============

/**
 * Cargar configuración del usuario actual
 */
async function loadConfig() {
  loading.value = true
  
  try {
    if (authStore.user?.id_usuario) {
      await configStore.fetchUserConfig(authStore.user.id_usuario)
      
      // Sincronizar formData con los datos del store
      if (configStore.currentConfig) {
        formData.idioma = configStore.currentConfig.idioma
        formData.rol = configStore.currentConfig.rol
        formData.tema = configStore.currentConfig.tema
      }
    }
  } catch (error) {
    console.error('Error al cargar configuración:', error)
  } finally {
    loading.value = false
  }
}

/**
 * Cambiar tema
 */
async function handleThemeChange(newTheme) {
  console.log('🎨 Intentando cambiar tema a:', newTheme)
  
  if (formData.tema === newTheme) {
    console.log('⚠️ El tema ya está seleccionado')
    return
  }
  
  // Actualizar formData optimistamente
  const previousTheme = formData.tema
  formData.tema = newTheme
  
  try {
    if (!authStore.user?.id_usuario) {
      throw new Error('Usuario no autenticado')
    }
    
    console.log('📡 Guardando tema en backend...')
    await configStore.changeTheme(authStore.user.id_usuario, newTheme)
    console.log('✅ Tema guardado exitosamente')
    showSuccessNotification()
  } catch (error) {
    console.error('❌ Error al cambiar tema:', error)
    console.error('Detalles del error:', error.response?.data || error.message)
    
    // Revertir cambio
    formData.tema = previousTheme
    
    alert('Error al guardar el tema. Por favor, intenta de nuevo.\n' + (error.message || 'Error desconocido'))
  }
}

/**
 * Cambiar idioma
 */
async function handleLanguageChange(newLanguage) {
  console.log('🌍 Intentando cambiar idioma a:', newLanguage)
  
  if (formData.idioma === newLanguage) {
    console.log('⚠️ El idioma ya está seleccionado')
    return
  }
  
  // Actualizar formData optimistamente
  const previousLanguage = formData.idioma
  formData.idioma = newLanguage
  
  try {
    if (!authStore.user?.id_usuario) {
      throw new Error('Usuario no autenticado')
    }
    
    console.log('📡 Guardando idioma en backend...')
    await configStore.changeLanguage(authStore.user.id_usuario, newLanguage)
    console.log('✅ Idioma guardado exitosamente')
    showSuccessNotification()
  } catch (error) {
    console.error('❌ Error al cambiar idioma:', error)
    console.error('Detalles del error:', error.response?.data || error.message)
    
    // Revertir cambio
    formData.idioma = previousLanguage
    
    alert('Error al guardar el idioma. Por favor, intenta de nuevo.\n' + (error.message || 'Error desconocido'))
  }
}

/**
 * Mostrar notificación de éxito
 */
function showSuccessNotification() {
  console.log('📢 Mostrando notificación de éxito')
  showSaveNotification.value = true
  
  // Ocultar después de 3 segundos
  setTimeout(() => {
    showSaveNotification.value = false
  }, 3000)
}

// ============= LIFECYCLE =============
onMounted(() => {
  loadConfig()
})
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

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>