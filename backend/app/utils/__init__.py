# Archivo 41/43: app/utils/__init__.py
# Descripción: Inicialización del módulo de utilidades
# Funcionalidad: Excepciones personalizadas y constantes del sistema

from .exceptions import JustTimeException, ValidationError, AuthenticationError
from .constants import *

__all__ = [
    "JustTimeException",
    "ValidationError", 
    "AuthenticationError",
    "HTTP_STATUS",
    "TASK_STATES",
    "PROJECT_STATES", 
    "PRIORITIES",
    "USER_ROLES"
]