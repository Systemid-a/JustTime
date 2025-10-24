<!-- ============================================================ -->
<!-- ARCHIVO 1/31: src/components/layout/AppHeader.vue - VERSIÓN FINAL ✅ -->
<!-- Módulo: Layout -->
<!-- Descripción: Header principal con badge de ROL mejorado -->
<!-- ✅ CORREGIDO: Ahora muestra "Administrador" en lugar de "Admin" -->
<!-- ✅ AGREGADO: Badge con colores e iconos según el rol -->
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
      <!-- Nombre del usuario -->
      <div class="text-right">
        <p class="text-white font-semibold">{{ userName }}</p>
        
        <!-- ⭐ NUEVO: Badge de rol con colores e icono -->
        <div class="flex items-center justify-end gap-1.5 mt-1">
          <span 
            :class="[
              'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold',
              isAdmin 
                ? 'bg-purple-100 text-purple-800 border border-purple-300' 
                : 'bg-blue-100 text-blue-800 border border-blue-300'
            ]"
          >
            <!-- Icono según el rol -->
            <component 
              :is="isAdmin ? Crown : User" 
              :size="12" 
              :stroke-width="2.5"
            />
            <!-- ⭐ CORREGIDO: Usa userRoleName en lugar de capitalizar -->
            <span>{{ userRoleName }}</span>
          </span>
        </div>
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
import { LogOut, Crown, User } from 'lucide-vue-next'

// ============= COMPOSABLES =============
const router = useRouter()
const authStore = useAuthStore()

// ============= COMPUTED =============

/**
 * Nombre del usuario
 */
const userName = computed(() => authStore.userName)

/**
 * ⭐ CORREGIDO: Usa userRoleName del store
 * Retorna "Administrador" o "Usuario" (no "Admin" o "Usuario")
 */
const userRoleName = computed(() => authStore.userRoleName)

/**
 * Verificar si es administrador (para el icono y color)
 */
const isAdmin = computed(() => authStore.isAdmin)

// ============= MÉTODOS =============

/**
 * Cerrar sesión y redirigir al login
 */
function handleLogout() {
  // Confirmar antes de cerrar sesión
  if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
    console.log('👋 Cerrando sesión...')
    
    // Llamar al logout del store
    authStore.logout()
    
    // Redirigir al login
    router.push('/login')
    
    console.log('✅ Sesión cerrada, redirigiendo al login')
  }
}
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>