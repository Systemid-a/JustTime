# Archivo 03/43: app/config.py
# Descripción: Configuraciones del sistema - VERSIÓN CORREGIDA SIN ERRORES
# Funcionalidad: Settings centralizados para base de datos, JWT y aplicación

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuraciones centralizadas del sistema JustTime"""
    
    # Configuración de la aplicación
    app_name: str = "JustTime"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Configuración de base de datos PostgreSQL - CONTRASEÑA CORREGIDA
    database_url: str = "postgresql://postgres:hola1234@localhost:5432/justtime"
    
    # Configuración JWT para autenticación
    secret_key: str = "justtime-secret-key-2024-proyecto-graduacion-ingenieria"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 horas
    
    # Configuración de archivos
    upload_directory: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Configuración de paginación
    default_page_size: int = 10
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorar campos extra del .env


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuraciones del sistema con cache"""
    return Settings()


# Instancia global de configuraciones
settings = get_settings()

# Configuraciones específicas por módulo
DATABASE_CONFIG = {
    "url": settings.database_url,
    "echo": False,
    "pool_size": 5,
    "max_overflow": 10
}

JWT_CONFIG = {
    "secret_key": settings.secret_key,
    "algorithm": settings.algorithm,
    "expire_minutes": settings.access_token_expire_minutes
}

FILE_CONFIG = {
    "upload_dir": settings.upload_directory,
    "max_size": settings.max_file_size,
    "allowed_ext": [".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]
}