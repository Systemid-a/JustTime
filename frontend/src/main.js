// ============================================================
// ARCHIVO 31/31: src/main.js
// Módulo: Principal
// Descripción: Punto de entrada de la aplicación Vue
// ============================================================

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Importar estilos de Tailwind CSS
import './assets/main.css'

// ============= CREAR APLICACIÓN =============
const app = createApp(App)

// ============= CONFIGURAR PINIA (Estado Global) =============
const pinia = createPinia()
app.use(pinia)

// ============= CONFIGURAR ROUTER =============
app.use(router)

// ============= MONTAR APLICACIÓN =============
app.mount('#app')

// ============= MENSAJE DE CONSOLA =============
console.log('%c⚖️ JustTime iniciado correctamente', 'color: #6366f1; font-size: 16px; font-weight: bold;')
console.log('%cMódulo LOGIN funcionando ✅', 'color: #10b981; font-size: 14px;')