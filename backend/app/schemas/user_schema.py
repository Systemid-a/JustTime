# Archivo 28/43: app/schemas/user_schema.py - VERSIÓN CORREGIDA ✅
# Descripción: Schemas Pydantic para validación de usuarios
# Funcionalidad: Validación de entrada, actualización y respuesta de usuarios

from pydantic import EmailStr, Field
from typing import Optional
from app.schemas.base_schema import BaseSchema


class UserCreate(BaseSchema):
    """Schema para crear usuario"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Email único para login")
    password: str = Field(..., min_length=6, max_length=72, description="Contraseña del usuario")  # ✅ CORREGIDO: max_length=72


class UserUpdate(BaseSchema):
    """Schema para actualizar usuario"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class UserResponse(BaseSchema):
    """Schema para respuesta de usuario (sin password)"""
    id_usuario: int
    nombre: str
    email: str
    activo: bool
    
    class Config:
        from_attributes = True


class UserLogin(BaseSchema):
    """Schema para login de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")


class TokenResponse(BaseSchema):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse