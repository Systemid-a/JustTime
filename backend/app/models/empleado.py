# Archivo 09/43: app/models/empleado.py - VERSIÓN ACTUALIZADA POST-MIGRACIÓN ✅
# Descripción: Modelo SQLAlchemy para tabla empleados - Personal de oficina jurídica  
# Funcionalidad: Gestión de empleados (ahora SIN usuario obligatorio)
# ✅ ACTUALIZADO: Se eliminó usuario_id_fk (ahora empleados son independientes)

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Empleado(Base):
    """
    Modelo Empleado - Tabla empleados
    Personal de la oficina jurídica (pueden existir sin usuario)
    
    CAMBIOS POST-MIGRACIÓN:
    ❌ ELIMINADO: usuario_id_fk (ya no existe esta columna)
    ✅ Relación: Empleado ← Usuario (opcional, inversa)
    ✅ Los empleados ahora pueden existir sin usuario asociado
    """
    __tablename__ = 'empleados'
    
    # Campos según script SQL actualizado
    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=True)
    puesto = Column(String(100), nullable=True)
    # ❌ usuario_id_fk ELIMINADO - Ya no existe en la base de datos
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(Date, default=func.current_date())
    
    # Relaciones
    # ✅ La relación inversa: un empleado PUEDE tener un usuario (o no)
    usuario = relationship("Usuario", back_populates="empleado", uselist=False, foreign_keys="Usuario.empleado_id_fk")
    proyectos = relationship("EmpleadoProyecto", back_populates="empleado")
    tareas = relationship("EmpleadoTarea", back_populates="empleado")
    
    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado}, nombre={self.nombre}, puesto={self.puesto})>"