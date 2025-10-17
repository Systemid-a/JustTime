# Archivo 13/43: app/models/tarea.py
# Descripción: Modelo SQLAlchemy para tabla tareas - Sistema Kanban
# Funcionalidad: Tareas para tablero Kanban con estados y prioridades

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Tarea(Base):
    """
    Modelo Tarea - Tabla tareas
    Sistema Kanban con estados (nuevo, progreso, finalizado)
    Coincide exactamente con script SQL
    """
    __tablename__ = 'tareas'
    
    # Campos según script SQL exacto
    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default='nuevo')
    fecha_vencimiento = Column(Date, nullable=True)
    proyecto_id_fk = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=True)
    prioridad = Column(String(10), default='media')
    
    # Constraints CHECK como en script SQL
    __table_args__ = (
        CheckConstraint("estado IN ('nuevo', 'en_progreso', 'finalizado')", name='ck_tareas_estado'),
        CheckConstraint("prioridad IN ('baja', 'media', 'alta')", name='ck_tareas_prioridad'),
    )
    
    # Relaciones
    proyecto = relationship("Proyecto", back_populates="tareas")
    empleados = relationship("EmpleadoTarea", back_populates="tarea")
    
    def __repr__(self):
        return f"<Tarea(id_tarea={self.id_tarea}, titulo={self.titulo}, estado={self.estado})>"
    

    