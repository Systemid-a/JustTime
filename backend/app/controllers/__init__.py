# Archivo: app/controllers/__init__.py
# Descripción: Inicialización del módulo de controllers

from .base_controller import BaseController
from .auth_controller import AuthController
from .task_controller import TaskController
from .project_controller import ProjectController
from .contact_controller import ContactController
from .analytics_controller import AnalyticsController  # ⬅️ AGREGAR ESTA LÍNEA
from .template_controller import TemplateController 

__all__ = [
    "BaseController",
    "AuthController",
    "TaskController",
    "ProjectController",
    "ContactController",
    "AnalyticsController",
    "TemplateController"  # ⬅️ AGREGAR ESTA LÍNEA
]

