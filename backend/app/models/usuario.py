# Archivo 08/43: app/models/usuario.py  
# Descripción: Modelo SQLAlchemy para tabla usuarios - Sistema de autenticación
# Funcionalidad: Login, autenticación JWT y gestión de usuarios

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    """
    Modelo Usuario - Tabla usuarios
    Sistema de autenticación y control de acceso
    Coincide exactamente con script SQL
    """
    __tablename__ = 'usuarios'
    
    # Campos según script SQL exacto
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False) 
    activo = Column(Boolean, default=True)
    
    # Relaciones 1:1 y 1:N
    empleado = relationship("Empleado", back_populates="usuario", uselist=False)
    documentos = relationship("Documento", back_populates="usuario")
    actividades_pendientes = relationship("ActividadPendiente", back_populates="usuario")
    configuracion = relationship("Configuracion", back_populates="usuario", uselist=False)
    
    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, email={self.email})>"