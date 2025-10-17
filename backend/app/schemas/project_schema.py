# Archivo 30/43: app/schemas/project_schema.py
# Descripción: Schemas Pydantic para validación de proyectos
# Funcionalidad: Validación para casos jurídicos con categorías y contactos

from pydantic import Field
from typing import Optional, Literal
from datetime import date
from app.schemas.base_schema import BaseSchema


class ProjectCreate(BaseSchema):
    """Schema para crear proyecto"""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre del proyecto/caso")
    descripcion: Optional[str] = Field(None, max_length=2000, description="Descripción del caso")
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[Literal["activo", "pausado", "finalizado"]] = Field(default="activo")
    contacto_id_fk: Optional[int] = None
    categoria_id_fk: Optional[int] = None
    prioridad: Optional[Literal["baja", "media", "alta"]] = Field(default="media")


class ProjectUpdate(BaseSchema):
    """Schema para actualizar proyecto"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[Literal["activo", "pausado", "finalizado"]] = None
    contacto_id_fk: Optional[int] = None
    categoria_id_fk: Optional[int] = None
    prioridad: Optional[Literal["baja", "media", "alta"]] = None


class ProjectResponse(BaseSchema):
    """Schema para respuesta de proyecto"""
    id_proyecto: int
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    estado: str
    contacto_id_fk: Optional[int]
    categoria_id_fk: Optional[int]
    prioridad: str
    
    class Config:
        from_attributes = True