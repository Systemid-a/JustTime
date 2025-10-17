# Archivo 09/43: app/models/empleado.py
# Descripción: Modelo SQLAlchemy para tabla empleados - Personal de oficina jurídica  
# Funcionalidad: Gestión de empleados vinculados a usuarios

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Empleado(Base):
    """
    Modelo Empleado - Tabla empleados
    Personal de la oficina jurídica con relación 1:1 a usuarios
    Coincide exactamente con script SQL
    """
    __tablename__ = 'empleados'
    
    # Campos según script SQL exacto
    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=True)
    puesto = Column(String(100), nullable=True)
    usuario_id_fk = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(Date, default=func.current_date())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="empleado")
    proyectos = relationship("EmpleadoProyecto", back_populates="empleado")
    tareas = relationship("EmpleadoTarea", back_populates="empleado")
    
    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado}, nombre={self.nombre})>"