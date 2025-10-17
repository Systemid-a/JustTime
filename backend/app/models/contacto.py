# Archivo 10/43: app/models/contacto.py
# Descripción: Modelo SQLAlchemy para tabla contactos - Clientes y empresas
# Funcionalidad: Gestión de contactos vinculados a proyectos jurídicos

from sqlalchemy import Column, Integer, String, Boolean, Text, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Contacto(Base):
    """
    Modelo Contacto - Tabla contactos
    Clientes y empresas para casos jurídicos
    Coincide exactamente con script SQL
    """
    __tablename__ = 'contactos'
    
    # Campos según script SQL exacto
    id_contacto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    tipo = Column(String(20), default='persona')
    direccion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Constraint CHECK como en script SQL
    __table_args__ = (
        CheckConstraint("tipo IN ('persona', 'empresa')", name='ck_contactos_tipo'),
    )
    
    # Relaciones
    proyectos = relationship("Proyecto", back_populates="contacto")
    
    def __repr__(self):
        return f"<Contacto(id_contacto={self.id_contacto}, nombre={self.nombre}, tipo={self.tipo})>"