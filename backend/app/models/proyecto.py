# Archivo 12/43: app/models/proyecto.py
# Descripción: Modelo SQLAlchemy para tabla proyectos - Casos jurídicos principales
# Funcionalidad: Gestión completa de casos legales con categorías y contactos

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Proyecto(Base):
    """
    Modelo Proyecto - Tabla proyectos
    Casos jurídicos completos vinculados a contactos y categorías
    Coincide exactamente con script SQL
    """
    __tablename__ = 'proyectos'
    
    # Campos según script SQL exacto
    id_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, default=func.current_date())
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(20), default='activo')
    contacto_id_fk = Column(Integer, ForeignKey('contactos.id_contacto'), nullable=True)
    categoria_id_fk = Column(Integer, ForeignKey('categorias_proyecto.id_categoria_proyecto'), nullable=True)
    prioridad = Column(String(10), default='media')
    
    # Constraints CHECK como en script SQL
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'pausado', 'finalizado')", name='ck_proyectos_estado'),
        CheckConstraint("prioridad IN ('baja', 'media', 'alta')", name='ck_proyectos_prioridad'),
    )
    
    # Relaciones
    contacto = relationship("Contacto", back_populates="proyectos")
    categoria = relationship("CategoriaProyecto", back_populates="proyectos")
    tareas = relationship("Tarea", back_populates="proyecto")
    documentos = relationship("Documento", back_populates="proyecto")
    actividades_pendientes = relationship("ActividadPendiente", back_populates="proyecto")
    empleados = relationship("EmpleadoProyecto", back_populates="proyecto")
    
    def __repr__(self):
        return f"<Proyecto(id_proyecto={self.id_proyecto}, nombre={self.nombre}, estado={self.estado})>"