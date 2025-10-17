# Archivo 23/43: app/controllers/task_controller.py
# Descripción: Controlador de tareas - Sistema Kanban
# Funcionalidad: CRUD de tareas con estados y filtros para tablero Kanban
# ✅ ACTUALIZADO: Usa 'en_progreso' para mejor estética

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.factory import BaseRepository


class TaskController(BaseController):
    """
    Controlador de tareas para sistema Kanban.
    Maneja estados: nuevo, en_progreso, finalizado
    ✅ ACTUALIZADO para usar 'en_progreso'
    """
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de tarea"""
        required_fields = ["titulo"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo {field} es requerido")
        
        # Validar estado si se proporciona - ✅ ACTUALIZADO: 'en_progreso'
        if "estado" in data:
            valid_states = ["nuevo", "en_progreso", "finalizado"]
            if data["estado"] not in valid_states:
                raise ValueError(f"Estado debe ser uno de: {valid_states}")
        
        # Validar prioridad si se proporciona
        if "prioridad" in data:
            valid_priorities = ["baja", "media", "alta"]
            if data["prioridad"] not in valid_priorities:
                raise ValueError(f"Prioridad debe ser una de: {valid_priorities}")
        
        return data
    
    def _task_to_dict(self, task) -> Optional[Dict[str, Any]]:
        """
        Convertir objeto Task a diccionario para serialización.
        Maneja correctamente las relaciones con otros objetos SQLAlchemy.
        """
        if task is None:
            return None
        
        try:
            # Crear diccionario base con campos simples
            task_dict = {
                "id_tarea": task.id_tarea,
                "titulo": task.titulo,
                "descripcion": task.descripcion,
                "estado": task.estado,
                "prioridad": task.prioridad if hasattr(task, 'prioridad') else None,
                "proyecto_id_fk": task.proyecto_id_fk
            }
            
            # Manejar fecha_vencimiento (puede ser None)
            if hasattr(task, 'fecha_vencimiento') and task.fecha_vencimiento:
                if isinstance(task.fecha_vencimiento, datetime):
                    task_dict["fecha_vencimiento"] = task.fecha_vencimiento.isoformat()
                else:
                    task_dict["fecha_vencimiento"] = task.fecha_vencimiento
            else:
                task_dict["fecha_vencimiento"] = None
            
            # CRÍTICO: Manejar relación con Proyecto
            if hasattr(task, 'proyecto') and task.proyecto is not None:
                try:
                    task_dict["proyecto_nombre"] = task.proyecto.nombre
                except Exception as e:
                    task_dict["proyecto_nombre"] = None
            else:
                task_dict["proyecto_nombre"] = None
            
            # Agregar fechas de auditoría si existen
            if hasattr(task, 'fecha_creacion') and task.fecha_creacion:
                if isinstance(task.fecha_creacion, datetime):
                    task_dict["fecha_creacion"] = task.fecha_creacion.isoformat()
            
            return task_dict
            
        except Exception as e:
            print(f"Error en _task_to_dict: {e}")
            print(f"Task object: {task}")
            return {
                "id_tarea": getattr(task, 'id_tarea', None),
                "titulo": getattr(task, 'titulo', 'Error al cargar'),
                "estado": getattr(task, 'estado', 'nuevo'),
                "descripcion": getattr(task, 'descripcion', ''),
                "prioridad": None,
                "fecha_vencimiento": None,
                "proyecto_id_fk": getattr(task, 'proyecto_id_fk', None),
                "proyecto_nombre": None
            }
    
    def get_by_estado(self, estado: str) -> List[Dict[str, Any]]:
        """Obtener tareas por estado para tablero Kanban"""
        try:
            tasks = self.repository.db.query(self.repository.model).filter(
                self.repository.model.estado == estado
            ).all()
            
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error en get_by_estado: {e}")
            return []
    
    def get_kanban_board(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener estructura completa del tablero Kanban"""
        try:
            # ✅ ACTUALIZADO: 'en_progreso'
            return {
                "nuevo": self.get_by_estado("nuevo"),
                "en_progreso": self.get_by_estado("en_progreso"), 
                "finalizado": self.get_by_estado("finalizado")
            }
        except Exception as e:
            print(f"Error en get_kanban_board: {e}")
            return {
                "nuevo": [],
                "en_progreso": [],
                "finalizado": []
            }
    
    def update_task_estado(self, task_id: int, nuevo_estado: str) -> Optional[Dict[str, Any]]:
        """Actualizar estado de tarea para movimiento en Kanban"""
        try:
            # ✅ ACTUALIZADO: 'en_progreso'
            valid_states = ["nuevo", "en_progreso", "finalizado"]
            if nuevo_estado not in valid_states:
                raise ValueError(f"Estado inválido: {nuevo_estado}")
            
            updated_task = self.update(task_id, {"estado": nuevo_estado})
            return self._task_to_dict(updated_task)
        except Exception as e:
            print(f"Error en update_task_estado: {e}")
            return None
    
    def get_by_proyecto(self, proyecto_id: int) -> List[Dict[str, Any]]:
        """Obtener tareas de un proyecto específico"""
        try:
            tasks = self.repository.db.query(self.repository.model).filter(
                self.repository.model.proyecto_id_fk == proyecto_id
            ).all()
            
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error en get_by_proyecto: {e}")
            return []
    
    def get_by_prioridad(self, prioridad: str) -> List[Dict[str, Any]]:
        """Obtener tareas por prioridad"""
        try:
            tasks = self.repository.db.query(self.repository.model).filter(
                self.repository.model.prioridad == prioridad
            ).all()
            
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error en get_by_prioridad: {e}")
            return []
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nueva tarea y retornar como diccionario"""
        try:
            validated_data = self.validate_data(data)
            task = self.repository.create(validated_data)
            return self._task_to_dict(task)
        except Exception as e:
            print(f"Error en create task: {e}")
            raise e
    
    def get_all_tasks(self, skip: int = 0, limit: int = 100, estado: str = None) -> List[Dict[str, Any]]:
        """Obtener todas las tareas como diccionarios con filtros opcionales"""
        try:
            query = self.repository.db.query(self.repository.model)
            
            # Aplicar filtro de estado si se proporciona
            if estado and estado != "":
                query = query.filter(self.repository.model.estado == estado)
            
            tasks = query.offset(skip).limit(limit).all()
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error en get_all_tasks: {e}")
            return []
    
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Obtener tarea por ID como diccionario"""
        try:
            task = self.repository.get_by_id(task_id)
            return self._task_to_dict(task)
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def update(self, task_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar tarea y retornar como diccionario"""
        try:
            # Validar solo los campos que se van a actualizar - ✅ ACTUALIZADO: 'en_progreso'
            if "estado" in data:
                valid_states = ["nuevo", "en_progreso", "finalizado"]
                if data["estado"] not in valid_states:
                    raise ValueError(f"Estado debe ser uno de: {valid_states}")
            
            if "prioridad" in data:
                valid_priorities = ["baja", "media", "alta"]
                if data["prioridad"] not in valid_priorities:
                    raise ValueError(f"Prioridad debe ser una de: {valid_priorities}")
            
            updated_task = self.repository.update(task_id, data)
            return self._task_to_dict(updated_task)
        except Exception as e:
            print(f"Error en update task: {e}")
            raise e
    
    def delete(self, task_id: int) -> bool:
        """Eliminar tarea"""
        try:
            return self.repository.delete(task_id)
        except Exception as e:
            print(f"Error en delete task: {e}")
            return False