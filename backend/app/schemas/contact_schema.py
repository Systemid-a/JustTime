# Archivo 31/43: app/schemas/contact_schema.py
from pydantic import Field, EmailStr
from typing import Optional, Literal
from app.schemas.base_schema import BaseSchema


class ContactCreate(BaseSchema):
    """Schema para crear contacto"""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre completo o razón social")
    tipo: Literal["persona", "empresa"] = Field(..., description="Tipo de contacto")
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=500)


class ContactUpdate(BaseSchema):
    """Schema para actualizar contacto"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    tipo: Optional[Literal["persona", "empresa"]] = None
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=500)


class ContactResponse(BaseSchema):
    """Schema para respuesta de contacto"""
    id_contacto: int
    nombre: str
    tipo: str
    telefono: Optional[str]
    email: Optional[str]
    direccion: Optional[str]
    activo: bool
    
    class Config:
        from_attributes = True