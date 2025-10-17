# Archivo 14/43: app/models/documento.py
# Descripción: Modelo SQLAlchemy para tabla documentos - Gestión de archivos
# Funcionalidad: Almacenamiento y gestión de archivos vinculados a proyectos

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Documento(Base):
    """
    Modelo Documento - Tabla documentos
    Gestión de archivos vinculados a proyectos y usuarios
    Coincide exactamente con script SQL
    """
    __tablename__ = 'documentos'
    
    # Campos según script SQL exacto
    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(Text, nullable=False)
    tipo_archivo = Column(String(50), nullable=True)
    proyecto_id_fk = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=True)
    subido_por_fk = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=True)
    fecha_subida = Column(DateTime, default=func.current_timestamp())
    
    # Relaciones
    proyecto = relationship("Proyecto", back_populates="documentos")
    usuario = relationship("Usuario", back_populates="documentos")
    
    def __repr__(self):
        return f"<Documento(id_documento={self.id_documento}, nombre_archivo={self.nombre_archivo})>"