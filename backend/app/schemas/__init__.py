# Archivo 26/43: app/schemas/__init__.py
# Descripción: Inicialización del módulo de schemas Pydantic
# Funcionalidad: Validación de datos de entrada y salida de la API

from .base_schema import BaseSchema
from .user_schema import UserCreate, UserUpdate, UserResponse
from .task_schema import TaskCreate, TaskUpdate, TaskResponse
from .project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from .contact_schema import ContactCreate, ContactUpdate, ContactResponse
from .template_schema import TemplateCreate, TemplateUpdate, TemplateResponse 
from .pending_activity_schema import PendingActivityCreate, PendingActivityUpdate, PendingActivityResponse
from .configuracion_schema import ConfiguracionCreate, ConfiguracionUpdate, ConfiguracionResponse
from .employee_schema import EmpleadoCreate, EmpleadoConUsuarioCreate, EmpleadoUpdate, EmpleadoResponse, VincularUsuarioRequest

__all__ = [
    "BaseSchema",
    "UserCreate", "UserUpdate", "UserResponse",
    "TaskCreate", "TaskUpdate", "TaskResponse", 
    "ProjectCreate", "ProjectUpdate", "ProjectResponse",
    "ContactCreate", "ContactUpdate", "ContactResponse",
    "TemplateCreate", "TemplateUpdate", "TemplateResponse",
    "PendingActivityCreate", "PendingActivityUpdate", "PendingActivityResponse",
    "ConfiguracionCreate", "ConfiguracionUpdate", "ConfiguracionResponse",
    "EmpleadoCreate", "EmpleadoConUsuarioCreate", "EmpleadoUpdate", "EmpleadoResponse", "VincularUsuarioRequest",
]