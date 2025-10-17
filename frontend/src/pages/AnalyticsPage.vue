<!-- ============================================================
ARCHIVO: src/pages/AnalyticsPage.vue - VERSIÓN CORREGIDA
Módulo: Páginas
Descripción: Vista de análisis y reportes con gráficas interactivas
✅ CORREGIDO: Manejo de respuesta del servicio analytics
============================================================ -->

<template>
  <div class="analytics-page">
    <!-- Header de la página -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">📊 Análisis y Reportes</h1>
        <p class="page-subtitle">Estadísticas y métricas de casos jurídicos</p>
      </div>
      
      <!-- Botón para refrescar datos -->
      <button 
        @click="cargarDatos" 
        :disabled="loading"
        class="btn-refresh"
      >
        <span v-if="loading">🔄 Cargando...</span>
        <span v-else>🔄 Actualizar</span>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading && !datosCompletos" class="loading-container">
      <div class="spinner"></div>
      <p>Cargando estadísticas...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <p>❌ {{ error }}</p>
      <button @click="cargarDatos" class="btn-retry">Reintentar</button>
    </div>

    <!-- Contenido principal -->
    <div v-else-if="datosCompletos" class="analytics-content">
      
      <!-- Tarjetas de resumen general -->
      <div class="stats-cards">
        <div class="stat-card card-blue">
          <div class="stat-icon">📁</div>
          <div class="stat-info">
            <p class="stat-label">Total Proyectos</p>
            <p class="stat-value">{{ datosCompletos.total_proyectos || 0 }}</p>
          </div>
        </div>

        <div class="stat-card card-green">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Activos</p>
            <p class="stat-value">{{ datosCompletos.proyectos_activos || 0 }}</p>
          </div>
        </div>

        <div class="stat-card card-yellow">
          <div class="stat-icon">⏸️</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Pausados</p>
            <p class="stat-value">{{ datosCompletos.proyectos_pausados || 0 }}</p>
          </div>
        </div>

        <div class="stat-card card-gray">
          <div class="stat-icon">✔️</div>
          <div class="stat-info">
            <p class="stat-label">Proyectos Finalizados</p>
            <p class="stat-value">{{ datosCompletos.proyectos_finalizados || 0 }}</p>
          </div>
        </div>
      </div>

      <!-- Sección de gráficas -->
      <div class="charts-section">
        
        <!-- Casos por Categoría -->
        <div class="chart-container">
          <div class="chart-header">
            <h2 class="chart-title">Casos por Categoría</h2>
            <div class="chart-controls">
              <button 
                @click="tipoGraficaCategoria = 'bar'" 
                :class="{ active: tipoGraficaCategoria === 'bar' }"
                class="btn-chart-type"
              >
                📊 Barras
              </button>
              <button 
                @click="tipoGraficaCategoria = 'pie'" 
                :class="{ active: tipoGraficaCategoria === 'pie' }"
                class="btn-chart-type"
              >
                🥧 Circular
              </button>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="chartCategoria"></canvas>
          </div>
        </div>

        <!-- Casos por Estado -->
        <div class="chart-container">
          <div class="chart-header">
            <h2 class="chart-title">Casos por Estado</h2>
            <div class="chart-controls">
              <button 
                @click="tipoGraficaEstado = 'bar'" 
                :class="{ active: tipoGraficaEstado === 'bar' }"
                class="btn-chart-type"
              >
                📊 Barras
              </button>
              <button 
                @click="tipoGraficaEstado = 'doughnut'" 
                :class="{ active: tipoGraficaEstado === 'doughnut' }"
                class="btn-chart-type"
              >
                🍩 Dona
              </button>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="chartEstado"></canvas>
          </div>
        </div>

      </div>

      <!-- Filtro por contacto -->
      <div class="filter-section">
        <div class="filter-header">
          <h2 class="section-title">🔍 Filtrar por Cliente/Contacto</h2>
        </div>
        <div class="filter-content">
          <select 
            v-model="contactoSeleccionado" 
            @change="filtrarPorContacto"
            class="select-contacto"
          >
            <option value="">-- Seleccionar contacto --</option>
            <option 
              v-for="contacto in datosCompletos.top_contactos" 
              :key="contacto.contacto_id"
              :value="contacto.contacto_id"
            >
              {{ contacto.contacto_nombre }} ({{ contacto.total_casos }} casos)
            </option>
          </select>

          <div v-if="datosContactoSeleccionado" class="contacto-stats">
            <h3>📋 Estadísticas de {{ datosContactoSeleccionado.contacto_nombre }}</h3>
            <div class="contacto-info">
              <div class="info-item">
                <span class="label">Tipo:</span>
                <span class="value">{{ datosContactoSeleccionado.contacto_tipo === 'persona' ? '👤 Persona' : '🏢 Empresa' }}</span>
              </div>
              <div class="info-item">
                <span class="label">Total de casos:</span>
                <span class="value">{{ datosContactoSeleccionado.total_casos }}</span>
              </div>
              <div class="info-item">
                <span class="label">Casos activos:</span>
                <span class="value text-green">{{ datosContactoSeleccionado.casos_activos }}</span>
              </div>
              <div class="info-item">
                <span class="label">Casos pausados:</span>
                <span class="value text-yellow">{{ datosContactoSeleccionado.casos_pausados }}</span>
              </div>
              <div class="info-item">
                <span class="label">Casos finalizados:</span>
                <span class="value text-gray">{{ datosContactoSeleccionado.casos_finalizados }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Clientes -->
      <div class="top-clientes-section">
        <h2 class="section-title">👥 Top 10 Clientes con Más Casos</h2>
        <div class="table-container">
          <table class="clientes-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Cliente</th>
                <th>Tipo</th>
                <th>Total Casos</th>
                <th>Activos</th>
                <th>Finalizados</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(contacto, index) in datosCompletos.top_contactos" 
                :key="contacto.contacto_id"
                @click="seleccionarContacto(contacto.contacto_id)"
                class="table-row-clickable"
              >
                <td>{{ index + 1 }}</td>
                <td class="nombre-cliente">{{ contacto.contacto_nombre }}</td>
                <td>
                  <span :class="['badge', contacto.contacto_tipo === 'persona' ? 'badge-person' : 'badge-company']">
                    {{ contacto.contacto_tipo === 'persona' ? '👤 Persona' : '🏢 Empresa' }}
                  </span>
                </td>
                <td class="text-center"><strong>{{ contacto.total_casos }}</strong></td>
                <td class="text-center text-green">{{ contacto.casos_activos }}</td>
                <td class="text-center text-gray">{{ contacto.casos_finalizados }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Estadísticas de Tareas -->
      <div class="tareas-stats-section">
        <h2 class="section-title">📝 Estadísticas de Tareas</h2>
        <div class="tareas-cards">
          <div class="tarea-card card-light-blue">
            <div class="tarea-icon">📋</div>
            <div class="tarea-info">
              <p class="tarea-label">Total Tareas</p>
              <p class="tarea-value">{{ datosCompletos.total_tareas || 0 }}</p>
            </div>
          </div>
          <div class="tarea-card card-light-gray">
            <div class="tarea-icon">🆕</div>
            <div class="tarea-info">
              <p class="tarea-label">Nuevas</p>
              <p class="tarea-value">{{ datosCompletos.tareas_nuevas || 0 }}</p>
            </div>
          </div>
          <div class="tarea-card card-light-yellow">
            <div class="tarea-icon">⏳</div>
            <div class="tarea-info">
              <p class="tarea-label">En Progreso</p>
              <p class="tarea-value">{{ datosCompletos.tareas_en_progreso || 0 }}</p>
            </div>
          </div>
          <div class="tarea-card card-light-green">
            <div class="tarea-icon">✅</div>
            <div class="tarea-info">
              <p class="tarea-label">Finalizadas</p>
              <p class="tarea-value">{{ datosCompletos.tareas_finalizadas || 0 }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import analyticsService from '@/services/analyticsService'

// Import Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
  PieController,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Registrar componentes y controladores
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
  PieController,
  Title,
  Tooltip,
  Legend
)

// ============= ESTADO REACTIVO =============
const loading = ref(false)
const error = ref(null)
const datosCompletos = ref(null)
const contactoSeleccionado = ref('')
const datosContactoSeleccionado = ref(null)

// Tipo de gráficas
const tipoGraficaCategoria = ref('bar')
const tipoGraficaEstado = ref('doughnut')

// Referencias a canvas
const chartCategoria = ref(null)
const chartEstado = ref(null)

// Instancias de gráficas
let chartCategoriaInstance = null
let chartEstadoInstance = null

// ============= MÉTODOS =============

/**
 * Cargar todos los datos de analytics
 * ✅ CORREGIDO: Manejo directo de response.data
 */
async function cargarDatos() {
  loading.value = true
  error.value = null
  
  try {
    // El servicio ya devuelve response.data directamente
    const datos = await analyticsService.getResumenCompleto()
    
    console.log('✅ Datos recibidos del backend:', datos)
    
    // Verificar que tengamos datos válidos
    if (!datos) {
      throw new Error('No se recibieron datos del servidor')
    }
    
    datosCompletos.value = datos.data || datos
    
    // Esperar a que el DOM se actualice antes de crear gráficas
    await nextTick()
    crearGraficas()
    
  } catch (err) {
    console.error('❌ Error al cargar analytics:', err)
    
    // Mensaje de error más específico
    if (err.status === 401) {
      error.value = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
    } else if (err.status === 0) {
      error.value = 'No se puede conectar con el servidor. Verifica que el backend esté ejecutándose.'
    } else {
      error.value = err.message || 'Error al cargar estadísticas. Por favor, intente nuevamente.'
    }
  } finally {
    loading.value = false
  }
}

/**
 * Crear gráficas de Chart.js
 */
function crearGraficas() {
  if (!datosCompletos.value) return
  
  // Verificar que existan los datos necesarios
  if (!datosCompletos.value.casos_por_categoria || !datosCompletos.value.casos_por_estado) {
    console.warn('⚠️ Faltan datos para crear las gráficas')
    return
  }
  
  // Destruir gráficas existentes
  if (chartCategoriaInstance) chartCategoriaInstance.destroy()
  if (chartEstadoInstance) chartEstadoInstance.destroy()
  
  // Crear gráfica de categorías
  crearGraficaCategoria()
  
  // Crear gráfica de estados
  crearGraficaEstado()
}

/**
 * Crear gráfica de casos por categoría
 */
function crearGraficaCategoria() {
  if (!chartCategoria.value) return
  
  const ctx = chartCategoria.value.getContext('2d')
  const datos = datosCompletos.value.casos_por_categoria
  
  const labels = datos.map(item => item.categoria_nombre)
  const values = datos.map(item => item.total_casos)
  const colors = datos.map(item => item.categoria_color)
  
  const config = {
    type: tipoGraficaCategoria.value,
    data: {
      labels: labels,
      datasets: [{
        label: 'Cantidad de Casos',
        data: values,
        backgroundColor: colors,
        borderColor: colors.map(color => color),
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: tipoGraficaCategoria.value === 'pie',
          position: 'bottom'
        },
        title: {
          display: false
        }
      },
      scales: tipoGraficaCategoria.value === 'bar' ? {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      } : {}
    }
  }
  
  chartCategoriaInstance = new ChartJS(ctx, config)
}

/**
 * Crear gráfica de casos por estado
 */
function crearGraficaEstado() {
  if (!chartEstado.value) return
  
  const ctx = chartEstado.value.getContext('2d')
  const datos = datosCompletos.value.casos_por_estado
  
  const labels = datos.map(item => item.estado_nombre)
  const values = datos.map(item => item.total_casos)
  const colors = ['#10b981', '#f59e0b', '#6b7280'] // Verde, Amarillo, Gris
  
  const config = {
    type: tipoGraficaEstado.value,
    data: {
      labels: labels,
      datasets: [{
        label: 'Cantidad de Casos',
        data: values,
        backgroundColor: colors,
        borderColor: colors,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: 'bottom'
        },
        title: {
          display: false
        }
      },
      scales: tipoGraficaEstado.value === 'bar' ? {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      } : {}
    }
  }
  
  chartEstadoInstance = new ChartJS(ctx, config)
}

/**
 * Filtrar estadísticas por contacto
 */
async function filtrarPorContacto() {
  if (!contactoSeleccionado.value) {
    datosContactoSeleccionado.value = null
    return
  }
  
  try {
    const datos = await analyticsService.getCasosContactoEspecifico(contactoSeleccionado.value)
    datosContactoSeleccionado.value = datos
    console.log('✅ Datos del contacto:', datos)
  } catch (err) {
    console.error('❌ Error al cargar datos del contacto:', err)
    error.value = 'Error al cargar estadísticas del contacto'
  }
}

/**
 * Seleccionar contacto desde la tabla
 */
function seleccionarContacto(contactoId) {
  contactoSeleccionado.value = contactoId
  filtrarPorContacto()
}

// ============= WATCHERS =============

// Recrear gráfica de categoría cuando cambia el tipo
watch(tipoGraficaCategoria, () => {
  if (datosCompletos.value) {
    crearGraficaCategoria()
  }
})

// Recrear gráfica de estado cuando cambia el tipo
watch(tipoGraficaEstado, () => {
  if (datosCompletos.value) {
    crearGraficaEstado()
  }
})

// ============= LIFECYCLE =============
onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
/* ============= LAYOUT PRINCIPAL ============= */
.analytics-page {
  padding: 2rem;
  background: #f9fafb;
  min-height: 100vh;
}

/* ============= HEADER ============= */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6b7280;
  font-size: 1rem;
}

.btn-refresh {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-refresh:hover:not(:disabled) {
  background: #4f46e5;
  transform: translateY(-2px);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ============= LOADING/ERROR ============= */
.loading-container,
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-container p {
  color: #ef4444;
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.btn-retry {
  padding: 0.75rem 1.5rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-retry:hover {
  background: #4f46e5;
}

/* ============= TARJETAS ESTADÍSTICAS ============= */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.card-blue { border-left-color: #3b82f6; }
.card-green { border-left-color: #10b981; }
.card-yellow { border-left-color: #f59e0b; }
.card-gray { border-left-color: #6b7280; }

.stat-icon {
  font-size: 2.5rem;
}

.stat-info {
  flex: 1;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
}

/* ============= GRÁFICAS ============= */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
}

.btn-chart-type {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-chart-type.active {
  background: #6366f1;
  color: white;
}

.chart-wrapper {
  position: relative;
  height: 300px;
}

.chart-wrapper canvas {
  max-height: 300px;
}

/* ============= FILTRO DE CONTACTO ============= */
.filter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filter-header {
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.select-contacto {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
}

.contacto-stats {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #6366f1;
}

.contacto-stats h3 {
  font-size: 1.125rem;
  margin-bottom: 1rem;
  color: #1f2937;
}

.contacto-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: white;
  border-radius: 0.375rem;
}

.info-item .label {
  color: #6b7280;
  font-weight: 500;
}

.info-item .value {
  font-weight: 600;
  color: #1f2937;
}

.text-green { color: #10b981 !important; }
.text-yellow { color: #f59e0b !important; }
.text-gray { color: #6b7280 !important; }

/* ============= TOP CLIENTES ============= */
.top-clientes-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.table-container {
  overflow-x: auto;
  margin-top: 1rem;
}

.clientes-table {
  width: 100%;
  border-collapse: collapse;
}

.clientes-table thead {
  background: #f9fafb;
}

.clientes-table th {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #6b7280;
  border-bottom: 2px solid #e5e7eb;
}

.clientes-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.table-row-clickable {
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-row-clickable:hover {
  background: #f9fafb;
}

.nombre-cliente {
  font-weight: 500;
  color: #1f2937;
}

.text-center {
  text-align: center;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge-person {
  background: #dbeafe;
  color: #1e40af;
}

.badge-company {
  background: #e0e7ff;
  color: #4338ca;
}

/* ============= ESTADÍSTICAS DE TAREAS ============= */
.tareas-stats-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tareas-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.tarea-card {
  padding: 1.25rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid;
}

.card-light-blue { 
  background: #eff6ff; 
  border-left-color: #3b82f6;
}

.card-light-gray { 
  background: #f3f4f6; 
  border-left-color: #6b7280;
}

.card-light-yellow { 
  background: #fef3c7; 
  border-left-color: #f59e0b;
}

.card-light-green { 
  background: #d1fae5; 
  border-left-color: #10b981;
}

.tarea-icon {
  font-size: 2rem;
}

.tarea-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.tarea-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
}

/* ============= RESPONSIVE ============= */
@media (max-width: 768px) {
  .analytics-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .stats-cards, .tareas-cards {
    grid-template-columns: 1fr;
  }

  .contacto-info {
    grid-template-columns: 1fr;
  }
}
</style>