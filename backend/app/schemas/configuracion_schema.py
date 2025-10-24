# Archivo: app/schemas/configuracion_schema.py
# Descripción: Schemas Pydantic para validación de configuraciones
# Funcionalidad: Validación de ajustes de usuario (idioma, rol, tema)

from pydantic import Field
from typing import Optional, Literal
from app.schemas.base_schema import BaseSchema


class ConfiguracionCreate(BaseSchema):
    """Schema para crear configuración"""
    usuario_id_fk: int = Field(..., description="ID del usuario")
    idioma: Optional[Literal["es", "en"]] = Field(default="es", description="Idioma de la interfaz")
    rol: Optional[Literal["admin", "usuario"]] = Field(default="usuario", description="Rol del usuario")
    tema: Optional[Literal["claro", "oscuro"]] = Field(default="claro", description="Tema de la interfaz")


class ConfiguracionUpdate(BaseSchema):
    """Schema para actualizar configuración"""
    idioma: Optional[Literal["es", "en"]] = None
    rol: Optional[Literal["admin", "usuario"]] = None
    tema: Optional[Literal["claro", "oscuro"]] = None


class ConfiguracionResponse(BaseSchema):
    """Schema para respuesta de configuración"""
    id_configuracion: int
    usuario_id_fk: int
    idioma: str
    rol: str
    tema: str
    
    class Config:
        from_attributes = True