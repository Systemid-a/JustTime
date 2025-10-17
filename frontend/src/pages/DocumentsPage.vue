<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center space-x-3">
          <FileText class="h-8 w-8 text-indigo-600" />
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Documentos</h1>
            <p class="text-sm text-gray-500 mt-1">Gestión de documentos del sistema</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Estado de Construcción -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div class="text-center py-16 px-6">
          <Construction class="h-20 w-20 text-indigo-500 mx-auto mb-6" />
          <h2 class="text-2xl font-bold text-gray-900 mb-3">Página en Construcción</h2>
          <p class="text-gray-600 max-w-md mx-auto mb-6">
            Esta sección está en desarrollo y estará disponible próximamente.
          </p>
          
          <!-- Información -->
          <div class="max-w-2xl mx-auto mt-8 bg-indigo-50 rounded-lg p-6 border border-indigo-100">
            <div class="flex items-start space-x-3">
              <Info class="h-6 w-6 text-indigo-600 flex-shrink-0 mt-1" />
              <div class="text-left">
                <h3 class="text-sm font-semibold text-indigo-900 mb-2">Funcionalidades Previstas</h3>
                <ul class="text-sm text-indigo-800 space-y-2">
                  <li class="flex items-center">
                    <CheckCircle class="h-4 w-4 mr-2 flex-shrink-0" />
                    Gestión de documentos legales
                  </li>
                  <li class="flex items-center">
                    <CheckCircle class="h-4 w-4 mr-2 flex-shrink-0" />
                    Carga y descarga de archivos
                  </li>
                  <li class="flex items-center">
                    <CheckCircle class="h-4 w-4 mr-2 flex-shrink-0" />
                    Organización por categorías
                  </li>
                  <li class="flex items-center">
                    <CheckCircle class="h-4 w-4 mr-2 flex-shrink-0" />
                    Control de versiones
                  </li>
                  <li class="flex items-center">
                    <CheckCircle class="h-4 w-4 mr-2 flex-shrink-0" />
                    Búsqueda avanzada de documentos
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Módulos Disponibles -->
          <div class="max-w-4xl mx-auto mt-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Módulos Disponibles</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <!-- Plantillas -->
              <router-link
                to="/plantillas"
                class="bg-white border-2 border-gray-200 hover:border-indigo-300 rounded-lg p-6 transition-all hover:shadow-md group"
              >
                <FileText class="h-10 w-10 text-indigo-600 mx-auto mb-3" />
                <h4 class="font-semibold text-gray-900 group-hover:text-indigo-600">Plantillas</h4>
                <p class="text-sm text-gray-500 mt-2">Gestión de plantillas Word</p>
              </router-link>

              <!-- Proyectos -->
              <router-link
                to="/proyectos"
                class="bg-white border-2 border-gray-200 hover:border-indigo-300 rounded-lg p-6 transition-all hover:shadow-md group"
              >
                <Briefcase class="h-10 w-10 text-indigo-600 mx-auto mb-3" />
                <h4 class="font-semibold text-gray-900 group-hover:text-indigo-600">Proyectos</h4>
                <p class="text-sm text-gray-500 mt-2">Gestión de proyectos</p>
              </router-link>

              <!-- Tareas -->
              <router-link
                to="/tareas"
                class="bg-white border-2 border-gray-200 hover:border-indigo-300 rounded-lg p-6 transition-all hover:shadow-md group"
              >
                <CheckSquare class="h-10 w-10 text-indigo-600 mx-auto mb-3" />
                <h4 class="font-semibold text-gray-900 group-hover:text-indigo-600">Tareas</h4>
                <p class="text-sm text-gray-500 mt-2">Tablero Kanban</p>
              </router-link>
            </div>
          </div>

          <!-- Botón Volver -->
          <div class="mt-8">
            <router-link
              to="/dashboard"
              class="inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-sm"
            >
              <ArrowLeft class="h-5 w-5 mr-2" />
              Volver al Dashboard
            </router-link>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { 
  FileText, Construction, Info, CheckCircle, 
  ArrowLeft, Briefcase, CheckSquare 
} from 'lucide-vue-next'
</script>

<style scoped>
/* Animación sutil para el icono de construcción */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>