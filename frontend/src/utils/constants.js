// ============================================================
// ARCHIVO: src/utils/constants.js - ACTUALIZADO CON EMPLEADOS
// Módulo: Utilidades
// Descripción: Constantes globales del sistema JustTime
// ⭐ AGREGADO: Constantes de empleados
// ============================================================

// ============= CONFIGURACIÓN API =============
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// ============= AUTENTICACIÓN =============
export const TOKEN_KEY = 'justtime_token'

// ============= ROLES DE USUARIO =============
export const ROLES = {
  ADMIN: 'admin',
  USUARIO: 'usuario'
}

// Opciones para select/dropdowns de roles
export const ROLES_OPTIONS = [
  { value: 'admin', label: 'Administrador', icon: '👑' },
  { value: 'usuario', label: 'Usuario', icon: '👤' }
]

// ============= ESTADOS DE TAREAS =============
export const ESTADOS_TAREA = {
  NUEVO: 'nuevo',
  EN_PROGRESO: 'en_progreso',
  FINALIZADO: 'finalizado'
}

// Opciones para select/dropdowns
export const ESTADOS_TAREA_OPTIONS = [
  { value: 'nuevo', label: 'Nuevo' },
  { value: 'en_progreso', label: 'En Progreso' },
  { value: 'finalizado', label: 'Finalizado' }
]

// ============= ESTADOS DE PROYECTOS =============
export const ESTADOS_PROYECTO = {
  ACTIVO: 'activo',
  PAUSADO: 'pausado',
  FINALIZADO: 'finalizado'
}

// Opciones para select/dropdowns
export const ESTADOS_PROYECTO_OPTIONS = [
  { value: 'activo', label: 'Activo' },
  { value: 'pausado', label: 'Pausado' },
  { value: 'finalizado', label: 'Finalizado' }
]

// ============= PRIORIDADES =============
export const PRIORIDADES = {
  BAJA: 'baja',
  MEDIA: 'media',
  ALTA: 'alta'
}

// Opciones para select/dropdowns
export const PRIORIDADES_OPTIONS = [
  { value: 'baja', label: 'Baja' },
  { value: 'media', label: 'Media' },
  { value: 'alta', label: 'Alta' }
]

// ============= TIPOS DE CONTACTO =============
export const TIPOS_CONTACTO = {
  PERSONA: 'persona',
  EMPRESA: 'empresa'
}

// Opciones para select/dropdowns
export const TIPOS_CONTACTO_OPTIONS = [
  { value: 'persona', label: 'Persona' },
  { value: 'empresa', label: 'Empresa' }
]

// ============= ⭐ NUEVO: ESTADOS DE EMPLEADOS =============
export const ESTADOS_EMPLEADO = {
  ACTIVO: true,
  INACTIVO: false
}

// Opciones para select/dropdowns
export const ESTADOS_EMPLEADO_OPTIONS = [
  { value: true, label: 'Activo', color: 'green' },
  { value: false, label: 'Inactivo', color: 'red' }
]

// ============= ⭐ NUEVO: ACCESO AL SISTEMA =============
export const ACCESO_SISTEMA = {
  CON_USUARIO: 'con_usuario',
  SIN_USUARIO: 'sin_usuario'
}

export const ACCESO_SISTEMA_OPTIONS = [
  { value: 'con_usuario', label: 'Con Usuario', icon: '✓' },
  { value: 'sin_usuario', label: 'Sin Usuario', icon: '✗' }
]

// ============= CATEGORÍAS DE PROYECTOS =============
// Colores oficiales de las categorías jurídicas
export const CATEGORIAS_COLORES = {
  civil: '#3b82f6',      // blue-500
  penal: '#ef4444',      // red-500
  laboral: '#10b981',    // green-500
  comercial: '#f59e0b',  // amber-500
  familia: '#8b5cf6'     // purple-500
}

// Mapeo de categorías nombre ↔ ID (según BD)
export const CATEGORIA_MAP = {
  // Nombre → ID (para enviar al backend)
  'civil': 1,
  'penal': 2,
  'laboral': 3,
  'comercial': 4,
  'familia': 5,
  
  // ID → Nombre (para recibir del backend)
  1: 'civil',
  2: 'penal',
  3: 'laboral',
  4: 'comercial',
  5: 'familia'
}

// Opciones de categorías para selects
export const CATEGORIAS_OPTIONS = [
  { value: 'civil', label: 'Civil', id: 1 },
  { value: 'penal', label: 'Penal', id: 2 },
  { value: 'laboral', label: 'Laboral', id: 3 },
  { value: 'comercial', label: 'Comercial', id: 4 },
  { value: 'familia', label: 'Familia', id: 5 }
]

// ============= CONFIGURACIONES DE USUARIO =============

/**
 * Idiomas disponibles en la aplicación
 */
export const LANGUAGES = {
  SPANISH: 'es',
  ENGLISH: 'en'
}

export const LANGUAGE_OPTIONS = [
  { value: 'es', label: 'Español', flag: '🇪🇸' },
  { value: 'en', label: 'English', flag: '🇬🇧' }
]

/**
 * Temas disponibles en la aplicación
 */
export const THEMES = {
  LIGHT: 'claro',
  DARK: 'oscuro'
}

export const THEME_OPTIONS = [
  { value: 'claro', label: 'Claro', icon: 'sun' },
  { value: 'oscuro', label: 'Oscuro', icon: 'moon' }
]

/**
 * Roles de usuario (duplicado para configuración)
 */
export const ROLE_OPTIONS = [
  { value: 'admin', label: 'Administrador', icon: '👑' },
  { value: 'usuario', label: 'Usuario', icon: '👤' }
]

/**
 * Configuración por defecto
 */
export const DEFAULT_CONFIG = {
  idioma: LANGUAGES.SPANISH,
  rol: ROLES.USUARIO,
  tema: THEMES.LIGHT
}

// ============= MENSAJES DE ERROR =============
export const MENSAJES_ERROR = {
  RED: 'Error de conexión. Verifica tu conexión a internet.',
  AUTENTICACION: 'Credenciales inválidas. Verifica tu email y contraseña.',
  NO_AUTORIZADO: 'No tienes permisos para realizar esta acción.',
  SERVIDOR: 'Error en el servidor. Intenta nuevamente más tarde.',
  SESION_EXPIRADA: 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
}

// ============= MENSAJES DE ÉXITO =============
export const MENSAJES_EXITO = {
  LOGIN: '¡Bienvenido a JustTime!',
  LOGOUT: 'Sesión cerrada correctamente',
  GUARDADO: 'Guardado exitosamente',
  ELIMINADO: 'Eliminado correctamente',
  ACTUALIZADO: 'Actualizado correctamente',
  EMPLEADO_CREADO: 'Empleado creado exitosamente',
  EMPLEADO_CON_USUARIO_CREADO: 'Empleado y usuario creados exitosamente',
  EMPLEADO_ACTUALIZADO: 'Empleado actualizado exitosamente',
  EMPLEADO_ELIMINADO: 'Empleado desactivado correctamente'
}

// ============= VALIDACIONES =============
export const REGEX = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  TELEFONO: /^\d{8,}$/
}

// ============= FUNCIONES HELPER PARA PROYECTOS =============

/**
 * Convertir nombre de categoría a ID
 * @param {string} nombreCategoria - Nombre de la categoría (ej: "civil")
 * @returns {number|null} ID de la categoría o null
 */
export function categoriaNombreToId(nombreCategoria) {
  if (!nombreCategoria) return null
  const nombre = nombreCategoria.toLowerCase()
  return CATEGORIA_MAP[nombre] || null
}

/**
 * Convertir ID de categoría a nombre
 * @param {number} idCategoria - ID de la categoría
 * @returns {string} Nombre de la categoría
 */
export function categoriaIdToNombre(idCategoria) {
  return CATEGORIA_MAP[idCategoria] || 'sin_categoria'
}

/**
 * Obtener etiqueta legible de la categoría
 * @param {string} categoria - Nombre de la categoría
 * @returns {string} Etiqueta capitalizada
 */
export function getCategoriaLabel(categoria) {
  if (!categoria) return 'Sin categoría'
  
  const categoriaLower = categoria.toLowerCase()
  const labels = {
    'civil': 'Civil',
    'penal': 'Penal',
    'laboral': 'Laboral',
    'comercial': 'Comercial',
    'familia': 'Familia'
  }
  
  return labels[categoriaLower] || 'Sin categoría'
}

/**
 * Obtener color de la categoría
 * @param {string} categoria - Nombre de la categoría
 * @returns {string} Código hexadecimal del color
 */
export function getCategoriaColor(categoria) {
  if (!categoria) return '#6b7280' // Gris por defecto
  return CATEGORIAS_COLORES[categoria.toLowerCase()] || '#6b7280'
}

/**
 * Mapear datos del proyecto del backend al frontend
 * @param {Object} backendProject - Proyecto del backend
 * @returns {Object} Proyecto mapeado para el frontend
 */
export function mapProjectFromBackend(backendProject) {
  if (!backendProject) return null
  
  return {
    ...backendProject,
    // Convertir categoria_id_fk a nombre para el frontend
    categoria: backendProject.categoria_nombre 
      ? backendProject.categoria_nombre.toLowerCase() 
      : categoriaIdToNombre(backendProject.categoria_id_fk),
    
    // Mapear contacto_id_fk a cliente (si existe el nombre)
    cliente: backendProject.contacto_nombre || null
  }
}

/**
 * Mapear datos del proyecto del frontend al backend
 * @param {Object} frontendProject - Proyecto del frontend
 * @returns {Object} Proyecto mapeado para el backend
 */
export function mapProjectToBackend(frontendProject) {
  if (!frontendProject) return null
  
  const backendData = {
    nombre: frontendProject.nombre,
    descripcion: frontendProject.descripcion || '',
    estado: frontendProject.estado || 'activo',
    fecha_inicio: frontendProject.fecha_inicio || new Date().toISOString().split('T')[0],
    fecha_fin: frontendProject.fecha_fin || null,
    
    // Convertir nombre de categoría a ID
    categoria_id_fk: categoriaNombreToId(frontendProject.categoria),
    
    // Si viene contacto_id_fk usarlo, sino null
    contacto_id_fk: frontendProject.contacto_id_fk || null
  }
  
  // Limpiar campos undefined
  Object.keys(backendData).forEach(key => {
    if (backendData[key] === undefined) {
      delete backendData[key]
    }
  })
  
  return backendData
}

// ============= ⭐ NUEVO: FUNCIONES HELPER PARA EMPLEADOS =============

/**
 * Obtener etiqueta de rol
 * @param {string} rol - Rol del usuario
 * @returns {string} Etiqueta legible del rol
 */
export function getRolLabel(rol) {
  const labels = {
    'admin': 'Administrador',
    'usuario': 'Usuario'
  }
  return labels[rol] || 'Sin rol'
}

/**
 * Obtener clase CSS para badge de rol
 * @param {string} rol - Rol del usuario
 * @returns {string} Clases CSS para el badge
 */
export function getRolBadgeClass(rol) {
  const classes = {
    'admin': 'bg-purple-100 text-purple-700',
    'usuario': 'bg-blue-100 text-blue-700'
  }
  return classes[rol] || 'bg-gray-100 text-gray-700'
}

/**
 * Obtener clase CSS para badge de estado de empleado
 * @param {boolean} activo - Estado del empleado
 * @returns {string} Clases CSS para el badge
 */
export function getEstadoEmpleadoBadgeClass(activo) {
  return activo 
    ? 'bg-green-100 text-green-700' 
    : 'bg-red-100 text-red-700'
}

/**
 * Validar email
 * @param {string} email - Email a validar
 * @returns {boolean} True si es válido
 */
export function isValidEmail(email) {
  return REGEX.EMAIL.test(email)
}

/**
 * Validar teléfono
 * @param {string} telefono - Teléfono a validar
 * @returns {boolean} True si es válido
 */
export function isValidTelefono(telefono) {
  return REGEX.TELEFONO.test(telefono)
}