<!-- ============================================================ -->
<!-- ARCHIVO 30/31: src/App.vue -->
<!-- Módulo: Componente Raíz -->
<!-- Descripción: Componente principal con layout condicional -->
<!-- ============================================================ -->

<template>
  <div id="app">
    <!-- Layout para páginas autenticadas (con Header + Sidebar) -->
    <div v-if="showLayout" class="flex h-screen overflow-hidden">
      <!-- Sidebar -->
      <AppSidebar />
      
      <!-- Contenido principal -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Header -->
        <AppHeader />
        
        <!-- Main content area -->
        <main class="flex-1 overflow-y-auto bg-gray-50 p-6">
          <router-view />
        </main>
      </div>
    </div>

    <!-- Sin layout para páginas públicas (solo Login) -->
    <router-view v-else />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'

// ============= COMPOSABLES =============
const route = useRoute()

// ============= COMPUTED =============
/**
 * Determinar si debe mostrar el layout (Header + Sidebar)
 * Solo se muestra en rutas autenticadas (no en /login)
 */
const showLayout = computed(() => {
  // No mostrar layout en la página de login
  return route.path !== '/login'
})
</script>

<style>
/* Estilos globales si son necesarios */
#app {
  height: 100vh;
  overflow: hidden;
}
</style>