# Archivo: app/controllers/__init__.py
# Descripción: Inicialización del módulo de controllers

from .base_controller import BaseController
from .auth_controller import AuthController
from .task_controller import TaskController
from .project_controller import ProjectController
from .contact_controller import ContactController
from .analytics_controller import AnalyticsController  # ⬅️ AGREGAR ESTA LÍNEA
from .template_controller import TemplateController 
from .pending_activity_controller import PendingActivityController
from .configuracion_controller import ConfiguracionController
from .employee_controller import EmpleadoController

__all__ = [
    "BaseController",
    "AuthController",
    "TaskController",
    "ProjectController",
    "ContactController",
    "AnalyticsController",
    "TemplateController", # ⬅️ AGREGAR ESTA LÍNEA
    "PendingActivityController",
    "ConfiguracionController",
    "EmpleadoController"
]

