# Archivo 43/43: app/utils/constants.py
# Descripción: Constantes del sistema JustTime
# Funcionalidad: Valores constantes para estados, prioridades y configuración

from typing import Dict, List

# Estados HTTP más utilizados
HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "VALIDATION_ERROR": 422,
    "INTERNAL_ERROR": 500
}

# Estados de tareas para sistema Kanban
TASK_STATES = {
    "NUEVO": "nuevo",
    "PROGRESO": "en_progreso", 
    "FINALIZADO": "finalizado"
}

TASK_STATES_LIST = list(TASK_STATES.values())

# Estados de proyectos jurídicos
PROJECT_STATES = {
    "ACTIVO": "activo",
    "PAUSADO": "pausado",
    "FINALIZADO": "finalizado"
}

PROJECT_STATES_LIST = list(PROJECT_STATES.values())

# Niveles de prioridad
PRIORITIES = {
    "BAJA": "baja",
    "MEDIA": "media", 
    "ALTA": "alta"
}

PRIORITIES_LIST = list(PRIORITIES.values())

# Roles de usuario
USER_ROLES = {
    "ADMIN": "admin",
    "USUARIO": "usuario"
}

USER_ROLES_LIST = list(USER_ROLES.values())

# Tipos de contacto
CONTACT_TYPES = {
    "PERSONA": "persona",
    "EMPRESA": "empresa"
}

CONTACT_TYPES_LIST = list(CONTACT_TYPES.values())

# Configuraciones de idioma
LANGUAGES = {
    "SPANISH": "es",
    "ENGLISH": "en"
}

LANGUAGES_LIST = list(LANGUAGES.values())

# Temas de la aplicación
THEMES = {
    "LIGHT": "claro",
    "DARK": "oscuro"
}

THEMES_LIST = list(THEMES.values())

# Extensiones de archivo permitidas
ALLOWED_FILE_EXTENSIONS = [
    ".pdf", ".doc", ".docx", 
    ".jpg", ".jpeg", ".png", 
    ".txt", ".rtf"
]

# Categorías jurídicas predefinidas
DEFAULT_LEGAL_CATEGORIES = [
    {"nombre": "Civil", "color": "#3b82f6", "descripcion": "Casos de derecho civil"},
    {"nombre": "Penal", "color": "#ef4444", "descripcion": "Casos de derecho penal"},
    {"nombre": "Laboral", "color": "#10b981", "descripcion": "Casos de derecho laboral"},
    {"nombre": "Comercial", "color": "#f59e0b", "descripcion": "Casos de derecho comercial"},
    {"nombre": "Familia", "color": "#8b5cf6", "descripcion": "Casos de derecho de familia"}
]

# Configuración de paginación
PAGINATION = {
    "DEFAULT_PAGE_SIZE": 10,
    "MAX_PAGE_SIZE": 100
}

# Mensajes del sistema
MESSAGES = {
    "USER_CREATED": "Usuario creado exitosamente",
    "USER_UPDATED": "Usuario actualizado exitosamente", 
    "USER_DELETED": "Usuario eliminado exitosamente",
    "LOGIN_SUCCESS": "Inicio de sesión exitoso",
    "LOGIN_FAILED": "Credenciales inválidas",
    "TASK_CREATED": "Tarea creada exitosamente",
    "TASK_UPDATED": "Tarea actualizada exitosamente",
    "PROJECT_CREATED": "Proyecto creado exitosamente",
    "PROJECT_UPDATED": "Proyecto actualizado exitosamente",
    "INVALID_DATA": "Datos inválidos proporcionados",
    "SERVER_ERROR": "Error interno del servidor",
    "NOT_FOUND": "Recurso no encontrado"
}