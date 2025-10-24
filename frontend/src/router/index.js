// ============================================================
// ARCHIVO 28/31: src/router/index.js - ACTUALIZADO CON ANALYTICS
// Módulo: Router
// Descripción: Vue Router simplificado con guards de autenticación
// ⭐ AGREGADO: Ruta de analytics para reportes y estadísticas
// ============================================================


import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

// ============= IMPORTAR PÁGINAS =============
import LoginPage from '@/pages/LoginPage.vue'
import HomePage from '@/pages/HomePage.vue'

// ============= DEFINIR RUTAS =============
const routes = [
  {
    path: '/',
    redirect: to => {
      // Redirigir según autenticación
      const authStore = useAuthStore()
      return authStore.isAuthenticated ? '/dashboard' : '/login'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: {
      requiresAuth: false,
      title: 'Iniciar Sesión - JustTime'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: HomePage,
    meta: {
      requiresAuth: true,
      title: 'Dashboard - JustTime'
    }
  },
  // Rutas protegidas futuras
  {
    path: '/tablero',
    name: 'Tablero',
    component: () => import('@/pages/TasksPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tablero Kanban - JustTime'
    }
  },
  {
    path: '/tareas',
    name: 'Tareas',
    component: () => import('@/pages/TasksPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tareas - JustTime'
    }
  },
  {
    path: '/proyectos',
    name: 'Proyectos',
    component: () => import('@/pages/ProjectsPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Proyectos - JustTime'
    }
  },
  {
    path: '/contactos',
    name: 'Contactos',
    component: () => import('@/pages/ContactsPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Contactos - JustTime'
    }
  },
  {
    path: '/documentos',
    name: 'Documentos',
    component: () => import('@/pages/DocumentsPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Documentos - JustTime'
    }
  },
  // Ruta de Analytics/Reportes
  {
    path: '/analisis',
    name: 'Analisis',
    component: () => import('@/pages/AnalyticsPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Análisis y Reportes - JustTime'
    }
  },
  {
    path: '/actividades-pendientes',
    name: 'ActividadesPendientes',
    component: () => import('@/pages/PendingActivitiesPage.vue'), 
    meta: {
      requiresAuth: true,
      title: 'Actividades Pendientes - JustTime'
    }
  },
  {
    path: '/plantillas',
    name: 'Plantillas',
    component: () => import('@/pages/TemplatesPage.vue'), 
    meta: {
      requiresAuth: true,
      title: 'Plantillas - JustTime'
    }
  },
  // ⭐ NUEVO: Ruta de Empleados
  {
    path: '/empleados',
    name: 'Empleados',
    component: () => import('@/pages/EmployeesPage.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: false, // Cambiar a true si solo admins pueden acceder
      title: 'Empleados - JustTime'
    }
  },
  {
    path: '/configuracion',
    name: 'Configuracion',
    component: () => import('@/pages/ConfigurationPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Configuración - JustTime'
    }
  },
  
  // Ruta 404 - No encontrado
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

// ============= CREAR ROUTER =============
const router = createRouter({
  history: createWebHistory(),
  routes
})

// ============= NAVIGATION GUARD =============
/**
 * Verificar autenticación antes de cada navegación
 */
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Actualizar título de la página
  document.title = to.meta.title || 'JustTime'
  
  // Verificar si la ruta requiere autenticación
  const requiresAuth = to.meta.requiresAuth
  const requiresAdmin = to.meta.requiresAdmin
  
  if (requiresAuth) {
    // Ruta protegida: verificar autenticación
    if (authStore.isAuthenticated) {
      // Usuario autenticado
      
      // ⭐ NUEVO: Verificar si requiere permisos de administrador
      if (requiresAdmin && !authStore.isAdmin) {
        // Usuario no es admin, redirigir al dashboard
        console.warn('Acceso denegado: se requieren permisos de administrador')
        next('/dashboard')
        return
      }
      
      // Permitir acceso
      next()
    } else {
      // Usuario no autenticado, verificar si hay token en localStorage
      const hasToken = authStore.token
      
      if (hasToken) {
        // Hay token, intentar obtener datos del usuario
        try {
          await authStore.fetchCurrentUser()
          
          // ⭐ NUEVO: Verificar permisos después de cargar usuario
          if (requiresAdmin && !authStore.isAdmin) {
            console.warn('Acceso denegado: se requieren permisos de administrador')
            next('/dashboard')
            return
          }
          
          next()
        } catch (error) {
          // Token inválido o error, redirigir al login
          console.error('Error al verificar autenticación:', error)
          next('/login')
        }
      } else {
        // No hay token, redirigir al login
        next('/login')
      }
    }
  } else {
    // Ruta pública
    if (to.path === '/login' && authStore.isAuthenticated) {
      // Si está autenticado e intenta ir al login, redirigir al dashboard
      next('/dashboard')
    } else {
      next()
    }
  }
})

// ============= EXPORTAR ROUTER =============
export default router 