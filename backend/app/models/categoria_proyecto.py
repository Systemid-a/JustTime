# Archivo 11/43: app/models/categoria_proyecto.py
# Descripción: Modelo SQLAlchemy para tabla categorias_proyecto - Tipos de casos jurídicos
# Funcionalidad: Clasificación de proyectos por tipo de caso legal

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class CategoriaProyecto(Base):
    """
    Modelo CategoriaProyecto - Tabla categorias_proyecto
    Tipos de casos jurídicos (Civil, Penal, Laboral, etc.)
    Coincide exactamente con script SQL
    """
    __tablename__ = 'categorias_proyecto'
    
    # Campos según script SQL exacto
    id_categoria_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    color = Column(String(7), default='#4f46e5')
    descripcion = Column(Text, nullable=True)
    
    # Relaciones
    proyectos = relationship("Proyecto", back_populates="categoria")
    
    def __repr__(self):
        return f"<CategoriaProyecto(id_categoria_proyecto={self.id_categoria_proyecto}, nombre={self.nombre})>"