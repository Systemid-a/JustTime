# Archivo 24/43: app/controllers/project_controller.py - VERSIÓN CORREGIDA V2
# Descripción: Controlador de proyectos con tareas_count agregado
# Funcionalidad: CRUD de proyectos con categorías, estados y contador de tareas

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.factory import BaseRepository


class ProjectController(BaseController):
    """
    Controlador de proyectos/casos jurídicos.
    Maneja estados: activo, pausado, finalizado
    """
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de proyecto"""
        required_fields = ["nombre"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo {field} es requerido")
        
        # Validar estado si se proporciona
        if "estado" in data:
            valid_states = ["activo", "pausado", "finalizado"]
            if data["estado"] not in valid_states:
                raise ValueError(f"Estado debe ser uno de: {valid_states}")
        
        return data
    
    def _project_to_dict(self, project) -> Optional[Dict[str, Any]]:
        """
        Convertir objeto Project a diccionario para serialización.
        Maneja correctamente las relaciones con otros objetos SQLAlchemy.
        INCLUYE contador de tareas asociadas.
        """
        if project is None:
            return None
        
        try:
            # Crear diccionario base con campos simples
            project_dict = {
                "id_proyecto": project.id_proyecto,
                "nombre": project.nombre,
                "descripcion": project.descripcion,
                "estado": project.estado,
                "contacto_id_fk": project.contacto_id_fk,
                "categoria_id_fk": project.categoria_id_fk if hasattr(project, 'categoria_id_fk') else None
            }
            
            # Manejar fecha_inicio (puede ser None)
            if hasattr(project, 'fecha_inicio') and project.fecha_inicio:
                if isinstance(project.fecha_inicio, datetime):
                    project_dict["fecha_inicio"] = project.fecha_inicio.isoformat()
                elif hasattr(project.fecha_inicio, 'isoformat'):
                    project_dict["fecha_inicio"] = project.fecha_inicio.isoformat()
                else:
                    project_dict["fecha_inicio"] = str(project.fecha_inicio)
            else:
                project_dict["fecha_inicio"] = None
            
            # CRÍTICO: Manejar relación con Contacto
            # Si el proyecto tiene un contacto asociado (lazy loading), extraer solo el nombre
            if hasattr(project, 'contacto') and project.contacto is not None:
                try:
                    project_dict["contacto_nombre"] = project.contacto.nombre
                except Exception as e:
                    project_dict["contacto_nombre"] = None
            else:
                project_dict["contacto_nombre"] = None
            
            # CRÍTICO: Manejar relación con Categoría
            # Si el proyecto tiene una categoría asociada, extraer solo el nombre
            if hasattr(project, 'categoria') and project.categoria is not None:
                try:
                    project_dict["categoria_nombre"] = project.categoria.nombre
                except Exception as e:
                    project_dict["categoria_nombre"] = None
            else:
                project_dict["categoria_nombre"] = None
            
            # ✅ NUEVO: Agregar contador de tareas asociadas
            if hasattr(project, 'tareas') and project.tareas is not None:
                try:
                    project_dict["tareas_count"] = len(project.tareas)
                except Exception as e:
                    print(f"Error al contar tareas: {e}")
                    project_dict["tareas_count"] = 0
            else:
                project_dict["tareas_count"] = 0
            
            # Agregar fechas de auditoría si existen
            if hasattr(project, 'fecha_creacion') and project.fecha_creacion:
                if isinstance(project.fecha_creacion, datetime):
                    project_dict["fecha_creacion"] = project.fecha_creacion.isoformat()
            
            return project_dict
            
        except Exception as e:
            # Log del error para debugging
            print(f"Error en _project_to_dict: {e}")
            print(f"Project object: {project}")
            # Retornar diccionario mínimo en caso de error
            return {
                "id_proyecto": getattr(project, 'id_proyecto', None),
                "nombre": getattr(project, 'nombre', 'Error al cargar'),
                "descripcion": getattr(project, 'descripcion', ''),
                "estado": getattr(project, 'estado', 'activo'),
                "fecha_inicio": None,
                "contacto_id_fk": getattr(project, 'contacto_id_fk', None),
                "categoria_id_fk": getattr(project, 'categoria_id_fk', None),
                "contacto_nombre": None,
                "categoria_nombre": None,
                "tareas_count": 0
            }
    
    def get_by_estado(self, estado: str) -> List[Dict[str, Any]]:
        """Obtener proyectos por estado"""
        try:
            projects = self.repository.db.query(self.repository.model).filter(
                self.repository.model.estado == estado
            ).all()
            
            return [self._project_to_dict(project) for project in projects]
        except Exception as e:
            print(f"Error en get_by_estado: {e}")
            return []
    
    def get_by_categoria(self, categoria_id: int) -> List[Dict[str, Any]]:
        """Obtener proyectos por categoría"""
        try:
            projects = self.repository.db.query(self.repository.model).filter(
                self.repository.model.categoria_id_fk == categoria_id
            ).all()
            
            return [self._project_to_dict(project) for project in projects]
        except Exception as e:
            print(f"Error en get_by_categoria: {e}")
            return []
    
    def get_by_contacto(self, contacto_id: int) -> List[Dict[str, Any]]:
        """Obtener proyectos de un contacto específico"""
        try:
            projects = self.repository.db.query(self.repository.model).filter(
                self.repository.model.contacto_id_fk == contacto_id
            ).all()
            
            return [self._project_to_dict(project) for project in projects]
        except Exception as e:
            print(f"Error en get_by_contacto: {e}")
            return []
    
    def get_activos(self) -> List[Dict[str, Any]]:
        """Obtener proyectos activos"""
        return self.get_by_estado("activo")
    
    def finalizar_proyecto(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Finalizar proyecto y actualizar estado"""
        try:
            updated_project = self.update(project_id, {"estado": "finalizado"})
            return self._project_to_dict(updated_project)
        except Exception as e:
            print(f"Error en finalizar_proyecto: {e}")
            return None
    
    def get_dashboard_stats(self) -> Dict[str, int]:
        """Obtener estadísticas para dashboard"""
        try:
            total = len(self.get_all_projects())
            activos = len(self.get_by_estado("activo"))
            pausados = len(self.get_by_estado("pausado"))
            finalizados = len(self.get_by_estado("finalizado"))
            
            return {
                "total": total,
                "activos": activos,
                "pausados": pausados,
                "finalizados": finalizados
            }
        except Exception as e:
            print(f"Error en get_dashboard_stats: {e}")
            return {
                "total": 0,
                "activos": 0,
                "pausados": 0,
                "finalizados": 0
            }
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo proyecto y retornar como diccionario"""
        try:
            validated_data = self.validate_data(data)
            project = self.repository.create(validated_data)
            return self._project_to_dict(project)
        except Exception as e:
            print(f"Error en create project: {e}")
            raise e
    
    def get_all_projects(self, skip: int = 0, limit: int = 100, estado: str = None) -> List[Dict[str, Any]]:
        """Obtener todos los proyectos como diccionarios con filtros opcionales"""
        try:
            query = self.repository.db.query(self.repository.model)
            
            # Aplicar filtro de estado si se proporciona
            if estado and estado != "":
                query = query.filter(self.repository.model.estado == estado)
            
            projects = query.offset(skip).limit(limit).all()
            return [self._project_to_dict(project) for project in projects]
        except Exception as e:
            print(f"Error en get_all_projects: {e}")
            return []
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Obtener proyecto por ID como diccionario"""
        try:
            project = self.repository.get_by_id(project_id)
            return self._project_to_dict(project)
        except Exception as e:
            print(f"Error en get_project_by_id: {e}")
            return None
    
    def update(self, project_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar proyecto y retornar como diccionario"""
        try:
            # Validar solo los campos que se van a actualizar
            if "estado" in data:
                valid_states = ["activo", "pausado", "finalizado"]
                if data["estado"] not in valid_states:
                    raise ValueError(f"Estado debe ser uno de: {valid_states}")
            
            updated_project = self.repository.update(project_id, data)
            return self._project_to_dict(updated_project)
        except Exception as e:
            print(f"Error en update project: {e}")
            raise e
    
    def delete(self, project_id: int) -> bool:
        """Eliminar proyecto"""
        try:
            return self.repository.delete(project_id)
        except Exception as e:
            print(f"Error en delete project: {e}")
            return False