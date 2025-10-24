# Archivo 03/43: app/config.py
# Descripción: Configuraciones del sistema - CON SOPORTE CORS
# Funcionalidad: Settings centralizados para base de datos, JWT, CORS y aplicación

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuraciones centralizadas del sistema JustTime"""
    
    # Configuración de la aplicación
    app_name: str = "JustTime"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Configuración de base de datos PostgreSQL
    database_url: str = "postgresql://postgres:hola1234@localhost:5432/justtime"
    
    # Configuración JWT para autenticación
    secret_key: str = "justtime-secret-key-2024-proyecto-graduacion-ingenieria"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 horas
    
    # ⭐ NUEVO: Configuración CORS - Lee desde variable de entorno
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    
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
    
    def get_cors_origins(self) -> List[str]:
        """
        Convierte la cadena CORS_ORIGINS en una lista de URLs permitidas.
        
        En Railway, CORS_ORIGINS debe ser:
        https://justtimee-production.up.railway.app
        
        En desarrollo local, será:
        http://localhost:5173,http://127.0.0.1:5173
        
        Returns:
            List[str]: Lista de orígenes permitidos para CORS
        """
        if not self.cors_origins:
            # Fallback a localhost si no hay variable de entorno
            return ["http://localhost:5173", "http://127.0.0.1:5173"]
        
        # Dividir por comas y limpiar espacios en blanco
        origins = [origin.strip() for origin in self.cors_origins.split(",")]
        
        # Filtrar orígenes vacíos
        origins = [origin for origin in origins if origin]
        
        return origins


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

# ⭐ NUEVO: Configuración CORS
CORS_CONFIG = {
    "origins": settings.get_cors_origins(),
    "credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "headers": ["*"]
}