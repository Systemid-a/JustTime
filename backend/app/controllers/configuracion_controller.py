# Archivo: app/controllers/configuracion_controller.py
# Descripción: Controlador de configuraciones - Ajustes de usuario
# Funcionalidad: CRUD de configuraciones con validación de restricciones

from typing import Dict, Any, Optional
from app.controllers.base_controller import BaseController


class ConfiguracionController(BaseController):
    """
    Controlador de configuraciones de usuario.
    Maneja idioma, rol y tema con validación estricta
    """
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de configuración"""
        # Validar idioma si se proporciona
        if "idioma" in data:
            valid_languages = ["es", "en"]
            if data["idioma"] not in valid_languages:
                raise ValueError(f"Idioma debe ser uno de: {valid_languages}")
        
        # Validar rol si se proporciona
        if "rol" in data:
            valid_roles = ["admin", "usuario"]
            if data["rol"] not in valid_roles:
                raise ValueError(f"Rol debe ser uno de: {valid_roles}")
        
        # Validar tema si se proporciona
        if "tema" in data:
            valid_themes = ["claro", "oscuro"]
            if data["tema"] not in valid_themes:
                raise ValueError(f"Tema debe ser uno de: {valid_themes}")
        
        return data
    
    def _config_to_dict(self, config) -> Optional[Dict[str, Any]]:
        """Convertir objeto Configuracion a diccionario para serialización"""
        if config is None:
            return None
        
        try:
            return {
                "id_configuracion": config.id_configuracion,
                "usuario_id_fk": config.usuario_id_fk,
                "idioma": config.idioma,
                "rol": config.rol,
                "tema": config.tema
            }
        except Exception as e:
            print(f"Error en _config_to_dict: {e}")
            return {
                "id_configuracion": getattr(config, 'id_configuracion', None),
                "usuario_id_fk": getattr(config, 'usuario_id_fk', None),
                "idioma": getattr(config, 'idioma', 'es'),
                "rol": getattr(config, 'rol', 'usuario'),
                "tema": getattr(config, 'tema', 'claro')
            }
    
    def get_by_usuario(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Obtener configuración de un usuario específico"""
        try:
            config = self.repository.db.query(self.repository.model).filter(
                self.repository.model.usuario_id_fk == usuario_id
            ).first()
            
            return self._config_to_dict(config)
        except Exception as e:
            print(f"Error en get_by_usuario: {e}")
            return None
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nueva configuración y retornar como diccionario"""
        try:
            # Validar que el usuario no tenga ya una configuración
            existing_config = self.get_by_usuario(data.get("usuario_id_fk"))
            if existing_config:
                raise ValueError("El usuario ya tiene una configuración. Use actualizar en su lugar.")
            
            validated_data = self.validate_data(data)
            config = self.repository.create(validated_data)
            return self._config_to_dict(config)
        except Exception as e:
            print(f"Error en create config: {e}")
            raise e
    
    def get_by_id(self, config_id: int) -> Optional[Dict[str, Any]]:
        """Obtener configuración por ID como diccionario"""
        try:
            config = self.repository.get_by_id(config_id)
            return self._config_to_dict(config)
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def update(self, config_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar configuración y retornar como diccionario"""
        try:
            validated_data = self.validate_data(data)
            updated_config = self.repository.update(config_id, validated_data)
            return self._config_to_dict(updated_config)
        except Exception as e:
            print(f"Error en update config: {e}")
            raise e
    
    def update_by_usuario(self, usuario_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar configuración por ID de usuario"""
        try:
            config = self.repository.db.query(self.repository.model).filter(
                self.repository.model.usuario_id_fk == usuario_id
            ).first()
            
            if not config:
                raise ValueError("Configuración no encontrada para este usuario")
            
            validated_data = self.validate_data(data)
            
            for key, value in validated_data.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            
            self.repository.db.commit()
            self.repository.db.refresh(config)
            
            return self._config_to_dict(config)
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en update_by_usuario: {e}")
            raise e
    
    def delete(self, config_id: int) -> bool:
        """Eliminar configuración"""
        try:
            return self.repository.delete(config_id)
        except Exception as e:
            print(f"Error en delete config: {e}")
            return False
    
    def delete_by_usuario(self, usuario_id: int) -> bool:
        """Eliminar configuración por ID de usuario"""
        try:
            config = self.repository.db.query(self.repository.model).filter(
                self.repository.model.usuario_id_fk == usuario_id
            ).first()
            
            if config:
                self.repository.db.delete(config)
                self.repository.db.commit()
                return True
            return False
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en delete_by_usuario: {e}")
            return False