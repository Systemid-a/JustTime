# Archivo 04/43: app/database.py
# Descripción: Configuración de conexión a PostgreSQL con SQLAlchemy
# Funcionalidad: Engine, SessionLocal y Base para modelos ORM

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import asyncio
from typing import Generator

from app.config import DATABASE_CONFIG


# Configuración del engine de SQLAlchemy
engine = create_engine(
    DATABASE_CONFIG["url"],
    echo=DATABASE_CONFIG["echo"],
    pool_size=DATABASE_CONFIG["pool_size"],
    max_overflow=DATABASE_CONFIG["max_overflow"],
    poolclass=StaticPool if "sqlite" in DATABASE_CONFIG["url"] else None,
    pool_pre_ping=True,  # Verificar conexiones antes de usar
    pool_recycle=300,    # Reciclar conexiones cada 5 minutos
)

# Configuración de sesiones de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Configuración de metadatos para naming conventions
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Base declarativa para modelos ORM
Base = declarative_base(metadata=metadata)


def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos para dependency injection.
    Garantiza que la sesión se cierre correctamente después del uso.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def test_connection():
    """Verificar conectividad con la base de datos"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión a PostgreSQL exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Soluciones posibles:")
        print("   1. Verificar que PostgreSQL esté ejecutándose")
        print("   2. Crear base de datos 'justtime'")
        print("   3. Verificar credenciales (usuario: postgres, password: hola1234)")
        print("   4. Verificar puerto 5432")
        return False


async def create_tables():
    """
    Crear todas las tablas definidas en los modelos.
    Se ejecuta al iniciar la aplicación.
    """
    try:
        # Verificar conexión primero
        if not test_connection():
            print("❌ No se pudo conectar a la base de datos")
            print("⚠️  La aplicación se ejecutará sin base de datos")
            return
        
        # Importar todos los modelos para asegurar que estén registrados
        from app.models import (
            usuario, empleado, contacto, categoria_proyecto, proyecto,
            tarea, documento, actividad_pendiente, configuracion,
            plantilla, empleado_proyecto, empleado_tarea
        )
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas de base de datos creadas correctamente")
        
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        print("⚠️  La aplicación se ejecutará sin base de datos")
        # NO lanzar excepción para permitir que la app inicie


def get_db_session() -> Session:
    """
    Obtener una sesión de base de datos para uso directo.
    Usar con cuidado - recordar cerrar la sesión manualmente.
    """
    return SessionLocal()


# Función para testing y desarrollo
def reset_database():
    """
    Recrear todas las tablas (solo para desarrollo).
    ¡CUIDADO! Elimina todos los datos existentes.
    """
    try:
        print("⚠️ Recreando base de datos...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos recreada")
    except Exception as e:
        print(f"❌ Error al recrear base de datos: {e}")