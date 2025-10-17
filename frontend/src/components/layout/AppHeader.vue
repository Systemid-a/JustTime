<!-- ============================================================ -->
<!-- ARCHIVO 1/31: src/components/layout/AppHeader.vue -->
<!-- Módulo: Layout -->
<!-- Descripción: Header principal con información del usuario -->
<!-- ============================================================ -->

<template>
  <header class="h-16 bg-indigo-600 shadow-md flex items-center justify-between px-6">
    <!-- Logo y nombre de la app -->
    <div class="flex items-center gap-3">
      <span class="text-3xl">⚖️</span>
      <h1 class="text-2xl font-bold text-white">JustTime</h1>
    </div>

    <!-- Información del usuario y logout -->
    <div class="flex items-center gap-4">
      <!-- Nombre y rol del usuario -->
      <div class="text-right">
        <p class="text-white font-semibold">{{ userName }}</p>
        <p class="text-indigo-200 text-sm">{{ userRole }}</p>
      </div>

      <!-- Botón de logout -->
      <button
        @click="handleLogout"
        class="flex items-center gap-2 px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-lg transition-all duration-200"
        title="Cerrar sesión"
      >
        <LogOut class="w-5 h-5" />
        <span class="hidden md:inline">Salir</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { LogOut } from 'lucide-vue-next'

// ============= COMPOSABLES =============
const router = useRouter()
const authStore = useAuthStore()

// ============= COMPUTED =============
const userName = computed(() => authStore.userName)
const userRole = computed(() => {
  // Capitalizar la primera letra del rol
  const role = authStore.userRole
  return role.charAt(0).toUpperCase() + role.slice(1)
})

// ============= MÉTODOS =============
/**
 * Cerrar sesión y redirigir al login
 */
function handleLogout() {
  // Confirmar antes de cerrar sesión
  if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
    // Llamar al logout del store
    authStore.logout()
    
    // Redirigir al login
    router.push('/login')
  }
}
</script>