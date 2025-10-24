# Archivo 05/43: app/factory.py - ACTUALIZADO CON EMPLEADOS
# Descripción: Factory Method pattern para acceso a base de datos (OBLIGATORIO para tesis)
# Funcionalidad: Creación centralizada de servicios y repositorios
# ⭐ AGREGADO: create_empleado_repository() y create_employee_service()

from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.models.base import Base


T = TypeVar('T', bound=Base)


class RepositoryInterface(ABC, Generic[T]):
    """Interfaz abstracta para repositorios de datos"""
    
    @abstractmethod
    def create(self, obj_data: dict) -> T:
        pass
    
    @abstractmethod
    def get_by_id(self, obj_id: int) -> T:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        pass
    
    @abstractmethod
    def update(self, obj_id: int, obj_data: dict) -> T:
        pass
    
    @abstractmethod
    def delete(self, obj_id: int) -> bool:
        pass


class BaseRepository(RepositoryInterface[T]):
    """Repositorio base con operaciones CRUD estándar"""
    
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db
    
    def create(self, obj_data: dict) -> T:
        try:
            obj = self.model(**obj_data)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            print(f"Error en create: {e}")
            raise e
    
    def get_by_id(self, obj_id: int) -> T:
        try:
            # Usar el campo de clave primaria correcto según el modelo
            if hasattr(self.model, 'id_usuario'):
                return self.db.query(self.model).filter(self.model.id_usuario == obj_id).first()
            elif hasattr(self.model, 'id_empleado'):
                return self.db.query(self.model).filter(self.model.id_empleado == obj_id).first()
            elif hasattr(self.model, 'id_proyecto'):
                return self.db.query(self.model).filter(self.model.id_proyecto == obj_id).first()
            elif hasattr(self.model, 'id_tarea'):
                return self.db.query(self.model).filter(self.model.id_tarea == obj_id).first()
            elif hasattr(self.model, 'id_plantilla'):
                return self.db.query(self.model).filter(self.model.id_plantilla == obj_id).first()
            elif hasattr(self.model, 'id_documento'):
                return self.db.query(self.model).filter(self.model.id_documento == obj_id).first()
            elif hasattr(self.model, 'id_actividad_pendiente'):
                return self.db.query(self.model).filter(self.model.id_actividad_pendiente == obj_id).first()
            elif hasattr(self.model, 'id_configuracion'):
                return self.db.query(self.model).filter(self.model.id_configuracion == obj_id).first()
            else:
                # Fallback genérico
                return self.db.query(self.model).filter(self.model.id == obj_id).first()
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            print(f"Error en get_all: {e}")
            return []
    
    def update(self, obj_id: int, obj_data: dict) -> T:
        try:
            obj = self.get_by_id(obj_id)
            if obj:
                for key, value in obj_data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                self.db.commit()
                self.db.refresh(obj)
            return obj
        except Exception as e:
            self.db.rollback()
            print(f"Error en update: {e}")
            return None
    
    def delete(self, obj_id: int) -> bool:
        try:
            obj = self.get_by_id(obj_id)
            if obj:
                self.db.delete(obj)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error en delete: {e}")
            return False


class RepositoryFactory:
    """
    Factory Method para creación de repositorios.
    Patrón requerido para el proyecto de tesis.
    """
    
    @staticmethod
    def create_repository(model: Type[T], db: Session = None) -> BaseRepository[T]:
        """
        Método factory para crear repositorios según el modelo.
        
        Args:
            model: Clase del modelo SQLAlchemy
            db: Sesión de base de datos (opcional)
        
        Returns:
            Instancia del repositorio correspondiente
        """
        if db is None:
            db = get_db_session()
        
        return BaseRepository(model, db)
    
    @staticmethod
    def create_user_repository(db: Session = None):
        """Factory específico para repositorio de usuarios"""
        from app.models.usuario import Usuario
        return RepositoryFactory.create_repository(Usuario, db)
    
    @staticmethod
    def create_empleado_repository(db: Session = None):
        """Factory específico para repositorio de empleados"""
        from app.models.empleado import Empleado
        return RepositoryFactory.create_repository(Empleado, db)
    
    @staticmethod
    def create_project_repository(db: Session = None):
        """Factory específico para repositorio de proyectos"""
        from app.models.proyecto import Proyecto
        return RepositoryFactory.create_repository(Proyecto, db)
    
    @staticmethod
    def create_task_repository(db: Session = None):
        """Factory específico para repositorio de tareas"""
        from app.models.tarea import Tarea
        return RepositoryFactory.create_repository(Tarea, db)
    
    @staticmethod
    def create_contact_repository(db: Session = None):
        """Factory específico para repositorio de contactos"""
        from app.models.contacto import Contacto
        return RepositoryFactory.create_repository(Contacto, db)
    
    @staticmethod
    def create_template_repository(db: Session = None):
        """Factory específico para repositorio de plantillas"""
        from app.models.plantilla import Plantilla
        return RepositoryFactory.create_repository(Plantilla, db)
    
    @staticmethod
    def create_document_repository(db: Session = None):
        """Factory específico para repositorio de documentos"""
        from app.models.documento import Documento
        return RepositoryFactory.create_repository(Documento, db)
    
    @staticmethod
    def create_pending_activity_repository(db: Session = None):
        """Factory específico para repositorio de actividades pendientes"""
        from app.models.actividad_pendiente import ActividadPendiente
        return RepositoryFactory.create_repository(ActividadPendiente, db)
    
    @staticmethod
    def create_configuracion_repository(db: Session = None):
        """Factory específico para repositorio de configuraciones"""
        from app.models.configuracion import Configuracion
        return RepositoryFactory.create_repository(Configuracion, db)


class ServiceFactory:
    """Factory para servicios de negocio"""
    
    @staticmethod
    def create_auth_service(db: Session = None):
        """Factory para servicio de autenticación"""
        from app.controllers.auth_controller import AuthController
        user_repo = RepositoryFactory.create_user_repository(db)
        return AuthController(user_repo)
    
    @staticmethod
    def create_employee_service(db: Session = None):
        """Factory para servicio de empleados"""
        from app.controllers.employee_controller import EmpleadoController
        empleado_repo = RepositoryFactory.create_empleado_repository(db)
        return EmpleadoController(empleado_repo)
    
    @staticmethod
    def create_project_service(db: Session = None):
        """Factory para servicio de proyectos"""
        from app.controllers.project_controller import ProjectController
        project_repo = RepositoryFactory.create_project_repository(db)
        return ProjectController(project_repo)
    
    @staticmethod
    def create_task_service(db: Session = None):
        """Factory para servicio de tareas"""
        from app.controllers.task_controller import TaskController
        task_repo = RepositoryFactory.create_task_repository(db)
        return TaskController(task_repo)
    
    @staticmethod
    def create_template_service(db: Session = None):
        """Factory para servicio de plantillas"""
        from app.controllers.plantilla_controller import TemplateController
        from app.services.file_service import FileService
        template_repo = RepositoryFactory.create_template_repository(db)
        file_service = FileService()
        return TemplateController(template_repo, file_service)
    
    @staticmethod
    def create_document_service(db: Session = None):
        """Factory para servicio de documentos"""
        from app.controllers.document_controller import DocumentController
        from app.services.file_service import FileService
        document_repo = RepositoryFactory.create_document_repository(db)
        file_service = FileService()
        return DocumentController(document_repo, file_service)
    
    @staticmethod
    def create_pending_activity_service(db: Session = None):
        """Factory para servicio de actividades pendientes"""
        from app.controllers.pending_activity_controller import PendingActivityController
        pending_activity_repo = RepositoryFactory.create_pending_activity_repository(db)
        return PendingActivityController(pending_activity_repo)
    
    @staticmethod
    def create_configuracion_service(db: Session = None):
        """Factory para servicio de configuraciones"""
        from app.controllers.configuracion_controller import ConfiguracionController
        configuracion_repo = RepositoryFactory.create_configuracion_repository(db)
        return ConfiguracionController(configuracion_repo)


# Instancia global de factories para uso en la aplicación
repository_factory = RepositoryFactory()
service_factory = ServiceFactory()