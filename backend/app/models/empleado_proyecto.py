# Archivo 18/43: app/models/empleado_proyecto.py
# Descripción: Modelo SQLAlchemy para tabla empleado_proyecto - Relación N:N empleados-proyectos
# Funcionalidad: Asignación de múltiples empleados a múltiples proyectos

from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class EmpleadoProyecto(Base):
    """
    Modelo EmpleadoProyecto - Tabla empleado_proyecto
    Tabla intermedia para relación N:N empleados ↔ proyectos
    Coincide exactamente con script SQL
    """
    __tablename__ = 'empleado_proyecto'
    
    # Campos según script SQL exacto
    id_empleado_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    empleado_id_fk = Column(Integer, ForeignKey('empleados.id_empleado'), nullable=False)
    proyecto_id_fk = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=False)
    fecha_asignacion = Column(Date, default=func.current_date())
    
    # Constraint UNIQUE como en script SQL
    __table_args__ = (
        UniqueConstraint('empleado_id_fk', 'proyecto_id_fk', name='uq_empleado_proyecto'),
    )
    
    # Relaciones hacia las entidades principales
    empleado = relationship("Empleado", back_populates="proyectos")
    proyecto = relationship("Proyecto", back_populates="empleados")
    
    def __repr__(self):
        return f"<EmpleadoProyecto(empleado_id={self.empleado_id_fk}, proyecto_id={self.proyecto_id_fk})>"