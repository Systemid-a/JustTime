# Archivo 36/43: app/routers/__init__.py
# Descripción: Inicialización del módulo de routers FastAPI
# Funcionalidad: Definición de rutas API REST para el sistema

from . import auth_routes, task_routes, project_routes,contact_routes, analytics_routes, template_routes

__all__ = [
    "auth_routes",
    "task_routes", 
    "project_routes",
    "contact_routes",
    "analytics_routes",
    "template_routes"
]
