# Archivo 15/43: app/models/actividad_pendiente.py
# Descripción: Modelo SQLAlchemy para tabla actividades_pendientes - Recordatorios
# Funcionalidad: Sistema de recordatorios y actividades pendientes por usuario

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class ActividadPendiente(Base):
    """
    Modelo ActividadPendiente - Tabla actividades_pendientes
    Sistema de recordatorios y actividades pendientes
    Coincide exactamente con script SQL
    """
    __tablename__ = 'actividades_pendientes'
    
    # Campos según script SQL exacto
    id_actividad_pendiente = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=True)
    completada = Column(Boolean, default=False)
    usuario_id_fk = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    proyecto_id_fk = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=True)
    prioridad = Column(String(10), default='media')
    
    # Constraint CHECK como en script SQL
    __table_args__ = (
        CheckConstraint("prioridad IN ('baja', 'media', 'alta')", name='ck_actividades_prioridad'),
    )
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="actividades_pendientes")
    proyecto = relationship("Proyecto", back_populates="actividades_pendientes")
    
    def __repr__(self):
        return f"<ActividadPendiente(id_actividad_pendiente={self.id_actividad_pendiente}, completada={self.completada})>"