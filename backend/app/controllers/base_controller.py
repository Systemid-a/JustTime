# Archivo 21/43: app/controllers/base_controller.py
# Descripción: Controlador base con operaciones CRUD genéricas
# Funcionalidad: Base común para todos los controladores del sistema

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.factory import BaseRepository


class BaseController(ABC):
    """
    Controlador base abstracto con operaciones CRUD comunes.
    Implementa patrón MVC como controlador base.
    """
    
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Obtener registro por ID"""
        return self.repository.get_by_id(id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """Obtener todos los registros con paginación"""
        return self.repository.get_all(skip=skip, limit=limit)
    
    def create(self, data: Dict[str, Any]) -> Any:
        """Crear nuevo registro"""
        return self.repository.create(data)
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        """Actualizar registro existente"""
        return self.repository.update(id, data)
    
    def delete(self, id: int) -> bool:
        """Eliminar registro"""
        return self.repository.delete(id)
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos específicos de cada entidad"""
        pass