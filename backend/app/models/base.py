# Archivo 07/43: app/models/base.py
# Descripción: Modelo base SQLAlchemy para herencia de modelos
# Funcionalidad: Base común para todos los modelos con configuración estándar

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer
from datetime import datetime

# Base declarativa para todos los modelos
Base = declarative_base()


class BaseModel(Base):
    """
    Modelo base abstracto para todas las entidades.
    Define configuración común y métodos utilitarios.
    """
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        # Auto-generar nombre de tabla basado en el nombre de la clase
        return cls.__name__.lower()
    
    def to_dict(self):
        """Convertir modelo a diccionario para serialización"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        """Representación string del modelo"""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"