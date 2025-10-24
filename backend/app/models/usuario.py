# Archivo 08/43: app/models/usuario.py - VERSIÓN ACTUALIZADA POST-MIGRACIÓN ✅
# Descripción: Modelo SQLAlchemy para tabla usuarios - Sistema de autenticación
# Funcionalidad: Login, autenticación JWT y gestión de usuarios
# ✅ ACTUALIZADO: Ahora incluye empleado_id_fk (Usuario → Empleado)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    """
    Modelo Usuario - Tabla usuarios
    Sistema de autenticación y control de acceso
    
    CAMBIOS POST-MIGRACIÓN:
    ✅ Agregado: empleado_id_fk (apunta a empleados.id_empleado)
    ✅ Relación: Usuario → Empleado (opcional, 1:1)
    """
    __tablename__ = 'usuarios'
    
    # Campos según script SQL actualizado
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False) 
    activo = Column(Boolean, default=True)
    empleado_id_fk = Column(Integer, ForeignKey('empleados.id_empleado'), nullable=True, unique=True)  # ✅ NUEVA COLUMNA
    
    # Relaciones 1:1 y 1:N
    empleado = relationship("Empleado", back_populates="usuario", uselist=False, foreign_keys=[empleado_id_fk])  # ✅ ACTUALIZADO
    documentos = relationship("Documento", back_populates="usuario")
    actividades_pendientes = relationship("ActividadPendiente", back_populates="usuario")
    configuracion = relationship("Configuracion", back_populates="usuario", uselist=False)
    
    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, email={self.email}, empleado_id={self.empleado_id_fk})>"