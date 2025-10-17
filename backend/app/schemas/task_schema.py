# Archivo 29/43: app/schemas/task_schema.py
# Descripción: Schemas Pydantic para validación de tareas
# Funcionalidad: Validación para sistema Kanban con estados y prioridades
# ✅ ACTUALIZADO: Usa 'en_progreso' para mejor estética

from pydantic import Field
from typing import Optional, Literal
from datetime import date
from app.schemas.base_schema import BaseSchema


class TaskCreate(BaseSchema):
    """Schema para crear tarea - ✅ ACTUALIZADO: 'en_progreso'"""
    titulo: str = Field(..., min_length=3, max_length=200, description="Título de la tarea")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Descripción detallada")
    estado: Optional[Literal["nuevo", "en_progreso", "finalizado"]] = Field(default="nuevo")
    fecha_vencimiento: Optional[date] = None
    proyecto_id_fk: Optional[int] = None
    prioridad: Optional[Literal["baja", "media", "alta"]] = Field(default="media")


class TaskUpdate(BaseSchema):
    """Schema para actualizar tarea - ✅ ACTUALIZADO: 'en_progreso'"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    estado: Optional[Literal["nuevo", "en_progreso", "finalizado"]] = None
    fecha_vencimiento: Optional[date] = None
    proyecto_id_fk: Optional[int] = None
    prioridad: Optional[Literal["baja", "media", "alta"]] = None


class TaskResponse(BaseSchema):
    """Schema para respuesta de tarea"""
    id_tarea: int
    titulo: str
    descripcion: Optional[str]
    estado: str
    fecha_vencimiento: Optional[date]
    proyecto_id_fk: Optional[int]
    prioridad: str
    
    class Config:
        from_attributes = True