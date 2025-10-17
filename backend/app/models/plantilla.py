# Archivo 17/43: app/models/plantilla.py
# Descripción: Modelo SQLAlchemy para tabla plantillas - Templates jurídicos reutilizables
# Funcionalidad: Plantillas de documentos para casos legales

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Plantilla(Base):
    """
    Modelo Plantilla - Tabla plantillas
    Almacenamiento de archivos .docx como plantillas reutilizables
    
    DIFERENCIA CON DOCUMENTOS:
    - Plantillas: Archivos Word (.docx) reutilizables SIN vínculo a proyectos
    - Documentos: Archivos variados VINCULADOS a proyectos específicos
    """
    __tablename__ = 'plantillas'
    
    # Campos principales
    id_plantilla = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, comment="Nombre descriptivo de la plantilla")
    
    # Campos para gestión de archivos (similar a modelo Documento)
    nombre_archivo = Column(String(255), nullable=False, comment="Nombre original del archivo .docx")
    ruta_archivo = Column(Text, nullable=False, comment="Ruta en sistema de archivos")
    
    # Metadatos del archivo
    categoria = Column(String(50), nullable=True, comment="Categoría: contrato, demanda, escritura, etc.")
    descripcion = Column(Text, nullable=True, comment="Descripción opcional de la plantilla")
    
    # Auditoría
    fecha_subida = Column(DateTime, default=func.current_timestamp(), comment="Fecha de subida")
    activo = Column(Integer, default=1, comment="1=activo, 0=eliminado (soft delete)")
    
    def __repr__(self):
        return f"<Plantilla(id={self.id_plantilla}, nombre='{self.nombre}', categoria='{self.categoria}')>"
    
    def to_dict(self):
        """Convertir a diccionario para serialización JSON"""
        return {
            'id_plantilla': self.id_plantilla,
            'nombre': self.nombre,
            'nombre_archivo': self.nombre_archivo,
            'ruta_archivo': self.ruta_archivo,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None,
            'activo': bool(self.activo)
        }