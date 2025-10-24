# Archivo: app/controllers/pending_activity_controller.py
# Descripción: Controlador de actividades pendientes - Sistema de recordatorios
# Funcionalidad: CRUD de actividades con estados completada/pendiente

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.factory import BaseRepository


class PendingActivityController(BaseController):
    """
    Controlador de actividades pendientes.
    Maneja recordatorios y actividades por completar.
    """
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de actividad pendiente"""
        required_fields = ["descripcion", "usuario_id_fk"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValueError(f"Campo {field} es requerido")
        
        # Validar prioridad si se proporciona
        if "prioridad" in data:
            valid_priorities = ["baja", "media", "alta"]
            if data["prioridad"] not in valid_priorities:
                raise ValueError(f"Prioridad debe ser una de: {valid_priorities}")
        
        # Validar que completada sea booleano
        if "completada" in data and not isinstance(data["completada"], bool):
            raise ValueError("El campo completada debe ser booleano")
        
        return data
    
    def _activity_to_dict(self, activity) -> Optional[Dict[str, Any]]:
        """
        Convertir objeto ActividadPendiente a diccionario para serialización.
        Maneja correctamente las relaciones con otros objetos SQLAlchemy.
        """
        if activity is None:
            return None
        
        try:
            # Crear diccionario base con campos simples
            activity_dict = {
                "id_actividad_pendiente": activity.id_actividad_pendiente,
                "descripcion": activity.descripcion,
                "completada": activity.completada,
                "prioridad": activity.prioridad if hasattr(activity, 'prioridad') else "media",
                "usuario_id_fk": activity.usuario_id_fk,
                "proyecto_id_fk": activity.proyecto_id_fk
            }
            
            # Manejar fecha_vencimiento (puede ser None)
            if hasattr(activity, 'fecha_vencimiento') and activity.fecha_vencimiento:
                if isinstance(activity.fecha_vencimiento, datetime):
                    activity_dict["fecha_vencimiento"] = activity.fecha_vencimiento.isoformat()
                else:
                    activity_dict["fecha_vencimiento"] = activity.fecha_vencimiento
            else:
                activity_dict["fecha_vencimiento"] = None
            
            # Manejar relación con Usuario
            if hasattr(activity, 'usuario') and activity.usuario is not None:
                try:
                    activity_dict["usuario_nombre"] = activity.usuario.nombre
                except Exception:
                    activity_dict["usuario_nombre"] = None
            else:
                activity_dict["usuario_nombre"] = None
            
            # Manejar relación con Proyecto
            if hasattr(activity, 'proyecto') and activity.proyecto is not None:
                try:
                    activity_dict["proyecto_nombre"] = activity.proyecto.nombre
                except Exception:
                    activity_dict["proyecto_nombre"] = None
            else:
                activity_dict["proyecto_nombre"] = None
            
            return activity_dict
            
        except Exception as e:
            print(f"Error en _activity_to_dict: {e}")
            return {
                "id_actividad_pendiente": getattr(activity, 'id_actividad_pendiente', None),
                "descripcion": getattr(activity, 'descripcion', 'Error al cargar'),
                "completada": getattr(activity, 'completada', False),
                "prioridad": "media",
                "fecha_vencimiento": None,
                "usuario_id_fk": getattr(activity, 'usuario_id_fk', None),
                "proyecto_id_fk": getattr(activity, 'proyecto_id_fk', None),
                "usuario_nombre": None,
                "proyecto_nombre": None
            }
    
    def get_by_usuario(self, usuario_id: int) -> List[Dict[str, Any]]:
        """Obtener actividades de un usuario específico"""
        try:
            activities = self.repository.db.query(self.repository.model).filter(
                self.repository.model.usuario_id_fk == usuario_id
            ).all()
            
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_by_usuario: {e}")
            return []
    
    def get_pendientes(self, usuario_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener actividades pendientes (no completadas)"""
        try:
            query = self.repository.db.query(self.repository.model).filter(
                self.repository.model.completada == False
            )
            
            if usuario_id:
                query = query.filter(self.repository.model.usuario_id_fk == usuario_id)
            
            activities = query.all()
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_pendientes: {e}")
            return []
    
    def get_completadas(self, usuario_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener actividades completadas"""
        try:
            query = self.repository.db.query(self.repository.model).filter(
                self.repository.model.completada == True
            )
            
            if usuario_id:
                query = query.filter(self.repository.model.usuario_id_fk == usuario_id)
            
            activities = query.all()
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_completadas: {e}")
            return []
    
    def marcar_completada(self, activity_id: int, completada: bool = True) -> Optional[Dict[str, Any]]:
        """Marcar actividad como completada o pendiente"""
        try:
            updated_activity = self.update(activity_id, {"completada": completada})
            return self._activity_to_dict(updated_activity)
        except Exception as e:
            print(f"Error en marcar_completada: {e}")
            return None
    
    def get_by_proyecto(self, proyecto_id: int) -> List[Dict[str, Any]]:
        """Obtener actividades de un proyecto específico"""
        try:
            activities = self.repository.db.query(self.repository.model).filter(
                self.repository.model.proyecto_id_fk == proyecto_id
            ).all()
            
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_by_proyecto: {e}")
            return []
    
    def get_by_prioridad(self, prioridad: str, usuario_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener actividades por prioridad"""
        try:
            query = self.repository.db.query(self.repository.model).filter(
                self.repository.model.prioridad == prioridad
            )
            
            if usuario_id:
                query = query.filter(self.repository.model.usuario_id_fk == usuario_id)
            
            activities = query.all()
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_by_prioridad: {e}")
            return []
    
    def get_vencidas(self, usuario_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener actividades vencidas (no completadas y fecha pasada)"""
        try:
            now = datetime.now()
            query = self.repository.db.query(self.repository.model).filter(
                self.repository.model.completada == False,
                self.repository.model.fecha_vencimiento < now
            )
            
            if usuario_id:
                query = query.filter(self.repository.model.usuario_id_fk == usuario_id)
            
            activities = query.all()
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_vencidas: {e}")
            return []
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nueva actividad pendiente y retornar como diccionario"""
        try:
            validated_data = self.validate_data(data)
            activity = self.repository.create(validated_data)
            return self._activity_to_dict(activity)
        except Exception as e:
            print(f"Error en create activity: {e}")
            raise e
    
    def get_all_activities(self, skip: int = 0, limit: int = 100, completada: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtener todas las actividades con filtros opcionales"""
        try:
            query = self.repository.db.query(self.repository.model)
            
            if completada is not None:
                query = query.filter(self.repository.model.completada == completada)
            
            activities = query.offset(skip).limit(limit).all()
            return [self._activity_to_dict(activity) for activity in activities]
        except Exception as e:
            print(f"Error en get_all_activities: {e}")
            return []
    
    def get_by_id(self, activity_id: int) -> Optional[Dict[str, Any]]:
        """Obtener actividad por ID como diccionario"""
        try:
            activity = self.repository.get_by_id(activity_id)
            return self._activity_to_dict(activity)
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def update(self, activity_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar actividad y retornar como diccionario"""
        try:
            if "prioridad" in data:
                valid_priorities = ["baja", "media", "alta"]
                if data["prioridad"] not in valid_priorities:
                    raise ValueError(f"Prioridad debe ser una de: {valid_priorities}")
            
            if "completada" in data and not isinstance(data["completada"], bool):
                raise ValueError("El campo completada debe ser booleano")
            
            updated_activity = self.repository.update(activity_id, data)
            return self._activity_to_dict(updated_activity)
        except Exception as e:
            print(f"Error en update activity: {e}")
            raise e
    
    def delete(self, activity_id: int) -> bool:
        """Eliminar actividad"""
        try:
            return self.repository.delete(activity_id)
        except Exception as e:
            print(f"Error en delete activity: {e}")
            return False