# Archivo 44/43: app/schemas/template_schema.py - NUEVO
# Descripción: Schemas Pydantic para validación de plantillas de documentos
# Funcionalidad: Validación de datos para upload, actualización y respuesta

from pydantic import Field, validator
from typing import Optional, Literal
from datetime import datetime
from app.schemas.base_schema import BaseSchema


class TemplateCreate(BaseSchema):
    """Schema para crear nueva plantilla (metadatos, no archivo)"""
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=200, 
        description="Nombre descriptivo de la plantilla"
    )
    categoria: Optional[Literal[
        "contrato", 
        "demanda", 
        "escritura", 
        "poder", 
        "memorial",
        "dictamen",
        "otro"
    ]] = Field(None, description="Categoría jurídica de la plantilla")
    descripcion: Optional[str] = Field(
        None, 
        max_length=1000, 
        description="Descripción opcional"
    )
    
    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()


class TemplateUpdate(BaseSchema):
    """Schema para actualizar plantilla existente"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    categoria: Optional[Literal[
        "contrato", 
        "demanda", 
        "escritura", 
        "poder", 
        "memorial",
        "dictamen",
        "otro"
    ]] = None
    descripcion: Optional[str] = Field(None, max_length=1000)
    activo: Optional[bool] = None


class TemplateResponse(BaseSchema):
    """Schema para respuesta de plantilla"""
    id_plantilla: int
    nombre: str
    nombre_archivo: str
    ruta_archivo: str
    categoria: Optional[str]
    descripcion: Optional[str]
    fecha_subida: Optional[datetime]
    activo: bool
    
    class Config:
        from_attributes = True


class TemplateListResponse(BaseSchema):
    """Schema para listado de plantillas"""
    templates: list[TemplateResponse]
    total: int
    activas: int
    por_categoria: dict


class FileUploadResponse(BaseSchema):
    """Schema para respuesta de upload exitoso"""
    success: bool
    message: str
    template: TemplateResponse


class FileValidationError(BaseSchema):
    """Schema para errores de validación de archivo"""
    success: bool = False
    error: str
    details: Optional[str] = None