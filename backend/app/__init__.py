# Archivo 01/43: app/__init__.py
# Descripción: Inicialización del módulo principal de la aplicación JustTime
# Arquitectura: MVC + Factory Method para proyecto de tesis

"""
JustTime - Aplicación Web Modular para Oficinas Jurídicas
=========================================================

Módulo principal de la aplicación backend desarrollada con FastAPI.
Implementa arquitectura MVC y patrón Factory Method para gestión
de casos jurídicos, tareas Kanban, documentos y contactos.

Tecnologías:
- FastAPI + SQLAlchemy + PostgreSQL
- Autenticación JWT
- Validaciones Pydantic

Desarrollado como proyecto de graduación en Ingeniería.
"""

__version__ = "1.0.0"
__author__ = "Estudiante de Ingeniería"
__description__ = "Sistema de gestión jurídica con tablero Kanban"

# Información del proyecto para documentación académica
PROJECT_INFO = {
    "name": "JustTime",
    "version": __version__,
    "description": __description__,
    "architecture": "MVC + Factory Method",
    "entities": 12,
    "modules": [
        "authentication",
        "projects", 
        "tasks",
        "contacts",
        "documents",
        "employees",
        "templates"
    ]
}