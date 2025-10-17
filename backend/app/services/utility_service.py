# Archivo 34/40: app/services/utility_service.py
# Descripción: Servicio de utilidades generales
# Funcionalidad: Funciones comunes y helpers del sistema

from typing import Dict, Any, List
from datetime import datetime, date
from sqlalchemy.orm import Session


class UtilityService:
    """
    Servicio de utilidades generales.
    Funciones helper y operaciones comunes del sistema.
    """
    
    @staticmethod
    def format_response(success: bool, data: Any = None, message: str = "") -> Dict[str, Any]:
        """Formatear respuesta estándar de la API"""
        return {
            "success": success,
            "data": data,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Operación exitosa") -> Dict[str, Any]:
        """Crear respuesta de éxito"""
        return UtilityService.format_response(True, data, message)
    
    @staticmethod
    def error_response(message: str = "Error en la operación", data: Any = None) -> Dict[str, Any]:
        """Crear respuesta de error"""
        return UtilityService.format_response(False, data, message)
    
    @staticmethod
    def paginate_query(query, page: int = 1, per_page: int = 10):
        """Paginar consulta SQLAlchemy"""
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)
    
    @staticmethod
    def serialize_datetime(obj: Any) -> Any:
        """Serializar objetos datetime para JSON"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        return obj
    
    @staticmethod
    def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpiar diccionario removiendo valores None"""
        return {k: v for k, v in data.items() if v is not None}
    
    @staticmethod
    def get_model_fields(model_class) -> List[str]:
        """Obtener campos de un modelo SQLAlchemy"""
        return [column.name for column in model_class.__table__.columns]