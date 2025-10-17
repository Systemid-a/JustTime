# Archivo 16/43: app/models/configuracion.py
# Descripción: Modelo SQLAlchemy para tabla configuraciones - Ajustes de usuario
# Funcionalidad: Configuraciones personalizadas por usuario (tema, idioma, rol)

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Configuracion(Base):
    """
    Modelo Configuracion - Tabla configuraciones
    Ajustes personalizados por usuario (relación 1:1)
    Coincide exactamente con script SQL
    """
    __tablename__ = 'configuraciones'
    
    # Campos según script SQL exacto
    id_configuracion = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id_fk = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False, unique=True)
    idioma = Column(String(10), default='es')
    rol = Column(String(20), default='usuario')
    tema = Column(String(10), default='claro')
    
    # Constraints CHECK como en script SQL
    __table_args__ = (
        CheckConstraint("idioma IN ('es', 'en')", name='ck_configuraciones_idioma'),
        CheckConstraint("rol IN ('admin', 'usuario')", name='ck_configuraciones_rol'),
        CheckConstraint("tema IN ('claro', 'oscuro')", name='ck_configuraciones_tema'),
    )
    
    # Relación 1:1 con usuario
    usuario = relationship("Usuario", back_populates="configuracion")
    
    def __repr__(self):
        return f"<Configuracion(id_configuracion={self.id_configuracion}, rol={self.rol}, tema={self.tema})>"