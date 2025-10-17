# Archivo 19/43: app/models/empleado_tarea.py
# Descripción: Modelo SQLAlchemy para tabla empleado_tarea - Relación N:N empleados-tareas
# Funcionalidad: Asignación de múltiples empleados a múltiples tareas con rol y estado

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class EmpleadoTarea(Base):
    """
    Modelo EmpleadoTarea - Tabla empleado_tarea
    Tabla intermedia para relación N:N empleados ↔ tareas
    Coincide exactamente con script SQL
    """
    __tablename__ = 'empleado_tarea'
    
    # Campos según script SQL exacto
    id_empleado_tarea = Column(Integer, primary_key=True, autoincrement=True)
    empleado_id_fk = Column(Integer, ForeignKey('empleados.id_empleado'), nullable=False)
    tarea_id_fk = Column(Integer, ForeignKey('tareas.id_tarea'), nullable=False)
    rol_en_tarea = Column(String(50), default='asignado')
    fecha_asignacion = Column(DateTime, default=func.current_timestamp())
    estado_personal = Column(String(20), default='pendiente')
    
    # Constraint UNIQUE como en script SQL
    __table_args__ = (
        UniqueConstraint('empleado_id_fk', 'tarea_id_fk', name='uq_empleado_tarea'),
    )
    
    # Relaciones hacia las entidades principales
    empleado = relationship("Empleado", back_populates="tareas")
    tarea = relationship("Tarea", back_populates="empleados")
    
    def __repr__(self):
        return f"<EmpleadoTarea(empleado_id={self.empleado_id_fk}, tarea_id={self.tarea_id_fk}, rol={self.rol_en_tarea})>"