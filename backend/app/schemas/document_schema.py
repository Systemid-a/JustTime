# Archivo: app/schemas/document_schema.py
# Descripción: Schemas Pydantic para validación de documentos
# Funcionalidad: Validación de datos para upload, actualización y respuesta de documentos

from pydantic import Field, validator
from typing import Optional
from datetime import datetime
from app.schemas.base_schema import BaseSchema


class DocumentCreate(BaseSchema):
    """Schema para crear nuevo documento (solo metadatos, el archivo se maneja aparte)"""
    nombre_archivo: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre del archivo"
    )
    tipo_archivo: Optional[str] = Field(
        None,
        max_length=50,
        description="Tipo/extensión del archivo (PDF, DOCX, JPG, etc.)"
    )
    proyecto_id_fk: Optional[int] = Field(
        None,
        description="ID del proyecto al que pertenece (puede ser NULL para documentos generales)"
    )
    subido_por_fk: Optional[int] = Field(
        None,
        description="ID del usuario que subió el archivo"
    )
    
    @validator('nombre_archivo')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre del archivo no puede estar vacío')
        return v.strip()
    
    @validator('tipo_archivo')
    def normalizar_tipo(cls, v):
        if v:
            # Normalizar extensión (convertir a minúsculas, agregar punto si falta)
            v = v.strip().lower()
            if not v.startswith('.'):
                v = f'.{v}'
        return v


class DocumentUpdate(BaseSchema):
    """Schema para actualizar documento existente"""
    nombre_archivo: Optional[str] = Field(None, min_length=1, max_length=255)
    tipo_archivo: Optional[str] = Field(None, max_length=50)
    proyecto_id_fk: Optional[int] = None
    
    @validator('tipo_archivo')
    def normalizar_tipo(cls, v):
        if v:
            v = v.strip().lower()
            if not v.startswith('.'):
                v = f'.{v}'
        return v


class DocumentResponse(BaseSchema):
    """Schema para respuesta de documento"""
    id_documento: int
    nombre_archivo: str
    ruta_archivo: str
    tipo_archivo: Optional[str]
    proyecto_id_fk: Optional[int]
    subido_por_fk: Optional[int]
    fecha_subida: Optional[datetime]
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseSchema):
    """Schema para listado de documentos"""
    documentos: list[DocumentResponse]
    total: int
    por_tipo: dict
    por_proyecto: dict


class DocumentUploadResponse(BaseSchema):
    """Schema para respuesta de upload exitoso"""
    success: bool
    message: str
    documento: DocumentResponse


class DocumentValidationError(BaseSchema):
    """Schema para errores de validación de archivo"""
    success: bool = False
    error: str
    details: Optional[str] = None


class DocumentFilterParams(BaseSchema):
    """Schema para parámetros de filtrado de documentos"""
    proyecto_id: Optional[int] = Field(None, description="Filtrar por proyecto")
    tipo_archivo: Optional[str] = Field(None, description="Filtrar por tipo de archivo")
    usuario_id: Optional[int] = Field(None, description="Filtrar por usuario que subió")
    fecha_desde: Optional[datetime] = Field(None, description="Documentos desde esta fecha")
    fecha_hasta: Optional[datetime] = Field(None, description="Documentos hasta esta fecha")