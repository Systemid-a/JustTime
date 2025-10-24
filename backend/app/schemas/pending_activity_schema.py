# Archivo: app/schemas/pending_activity_schema.py
# Descripción: Schemas Pydantic para validación de actividades pendientes
# Funcionalidad: Validación para sistema de recordatorios y actividades

from pydantic import Field
from typing import Optional, Literal
from datetime import datetime
from app.schemas.base_schema import BaseSchema


class PendingActivityCreate(BaseSchema):
    """Schema para crear actividad pendiente"""
    descripcion: str = Field(..., min_length=3, max_length=1000, description="Descripción de la actividad")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha y hora de vencimiento")
    completada: Optional[bool] = Field(default=False, description="Estado de completado")
    usuario_id_fk: int = Field(..., description="ID del usuario responsable")
    proyecto_id_fk: Optional[int] = Field(None, description="ID del proyecto asociado")
    prioridad: Optional[Literal["baja", "media", "alta"]] = Field(default="media", description="Prioridad de la actividad")


class PendingActivityUpdate(BaseSchema):
    """Schema para actualizar actividad pendiente"""
    descripcion: Optional[str] = Field(None, min_length=3, max_length=1000)
    fecha_vencimiento: Optional[datetime] = None
    completada: Optional[bool] = None
    usuario_id_fk: Optional[int] = None
    proyecto_id_fk: Optional[int] = None
    prioridad: Optional[Literal["baja", "media", "alta"]] = None


class PendingActivityResponse(BaseSchema):
    """Schema para respuesta de actividad pendiente"""
    id_actividad_pendiente: int
    descripcion: str
    fecha_vencimiento: Optional[datetime]
    completada: bool
    usuario_id_fk: int
    proyecto_id_fk: Optional[int]
    prioridad: str
    
    class Config:
        from_attributes = True