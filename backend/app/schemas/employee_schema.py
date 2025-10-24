# Archivo: app/schemas/employee_schema.py
# Descripción: Schemas Pydantic para validación de empleados
# Funcionalidad: Validación para CRUD de empleados con usuarios

from pydantic import Field, EmailStr
from typing import Optional, Literal
from datetime import date
from app.schemas.base_schema import BaseSchema


class EmpleadoBase(BaseSchema):
    """Schema base para empleado"""
    nombre: str = Field(..., min_length=3, max_length=150, description="Nombre completo del empleado")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    puesto: Optional[str] = Field(None, max_length=100, description="Puesto o cargo")
    activo: Optional[bool] = Field(default=True, description="Estado del empleado")


class EmpleadoCreate(EmpleadoBase):
    """Schema para crear empleado sin usuario"""
    pass


class EmpleadoConUsuarioCreate(BaseSchema):
    """
    Schema para crear empleado con usuario asociado.
    Incluye datos del empleado, credenciales de usuario y rol.
    """
    # Datos del empleado
    nombre: str = Field(..., min_length=3, max_length=150, description="Nombre completo")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono")
    puesto: Optional[str] = Field(None, max_length=100, description="Puesto o cargo")
    
    # Datos del usuario
    email: EmailStr = Field(..., description="Email para login")
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña")
    
    # Rol del usuario
    rol: Literal["admin", "usuario"] = Field(
        default="usuario",
        description="Rol: 'admin' (crear/modificar/eliminar) o 'usuario' (solo ver)"
    )


class EmpleadoUpdate(BaseSchema):
    """Schema para actualizar empleado"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    puesto: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None


class EmpleadoResponse(BaseSchema):
    """
    Schema para respuesta de empleado.
    Incluye información del usuario asociado si existe.
    """
    id_empleado: int
    nombre: str
    telefono: Optional[str]
    puesto: Optional[str]
    activo: bool
    fecha_ingreso: Optional[date]
    
    # Información del usuario asociado
    tiene_usuario: bool
    usuario_id: Optional[int]
    usuario_email: Optional[str]
    rol: Optional[str]
    
    class Config:
        from_attributes = True


class VincularUsuarioRequest(BaseSchema):
    """Schema para vincular usuario existente a empleado"""
    usuario_id: int = Field(..., gt=0, description="ID del usuario a vincular")