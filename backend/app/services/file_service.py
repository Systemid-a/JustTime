# Archivo 33/43: app/services/file_service.py
# Descripción: Servicio para manejo de archivos
# Funcionalidad: Subida, validación y gestión de documentos

import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import FILE_CONFIG


class FileService:
    """
    Servicio para manejo de archivos y documentos.
    Validación, subida y gestión de archivos del sistema.
    """
    
    def __init__(self):
        self.upload_dir = FILE_CONFIG["upload_dir"]
        self.max_size = FILE_CONFIG["max_size"]
        self.allowed_extensions = FILE_CONFIG["allowed_ext"]
        
        # Crear directorio si no existe
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> bool:
        """Validar archivo subido"""
        # Validar extensión
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Extensión no permitida. Permitidas: {self.allowed_extensions}"
            )
        
        # Validar tamaño (si es posible)
        if hasattr(file.file, 'seek'):
            file.file.seek(0, 2)  # Ir al final del archivo
            file_size = file.file.tell()
            file.file.seek(0)  # Volver al inicio
            
            if file_size > self.max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"Archivo muy grande. Máximo: {self.max_size/1024/1024}MB"
                )
        
        return True
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generar nombre único para el archivo"""
        file_ext = Path(original_filename).suffix
        unique_name = f"{uuid.uuid4()}{file_ext}"
        return unique_name
    
    async def save_file(self, file: UploadFile) -> dict:
        """Guardar archivo y retornar información"""
        self.validate_file(file)
        
        # Generar nombre único
        unique_filename = self.generate_unique_filename(file.filename)
        file_path = Path(self.upload_dir) / unique_filename
        
        # Guardar archivo
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        return {
            "nombre_archivo": file.filename,
            "ruta_archivo": str(file_path),
            "tipo_archivo": file.content_type,
            "tamaño": len(contents)
        }
    
    def delete_file(self, file_path: str) -> bool:
        """Eliminar archivo del sistema"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            pass
        return False