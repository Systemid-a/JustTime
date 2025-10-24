# Archivo: app/controllers/employee_controller.py
# Descripción: Controlador de empleados - Gestión de personal
# Funcionalidad: CRUD de empleados con vinculación opcional a usuarios

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.factory import BaseRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmpleadoController(BaseController):
    """
    Controlador de empleados para gestión de personal.
    Maneja la creación de empleados con o sin usuario asociado.
    """
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de empleado"""
        required_fields = ["nombre"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo {field} es requerido")
        
        # Validar teléfono si se proporciona
        if "telefono" in data and data["telefono"]:
            if len(data["telefono"]) > 20:
                raise ValueError("Teléfono no puede exceder 20 caracteres")
        
        return data
    
    def _empleado_to_dict(self, empleado) -> Optional[Dict[str, Any]]:
        """
        Convertir objeto Empleado a diccionario para serialización.
        Incluye información del usuario asociado si existe.
        """
        if empleado is None:
            return None
        
        try:
            # Crear diccionario base con campos simples
            empleado_dict = {
                "id_empleado": empleado.id_empleado,
                "nombre": empleado.nombre,
                "telefono": empleado.telefono,
                "puesto": empleado.puesto,
                "activo": empleado.activo
            }
            
            # Manejar fecha_ingreso
            if hasattr(empleado, 'fecha_ingreso') and empleado.fecha_ingreso:
                if isinstance(empleado.fecha_ingreso, datetime):
                    empleado_dict["fecha_ingreso"] = empleado.fecha_ingreso.isoformat()
                else:
                    empleado_dict["fecha_ingreso"] = empleado.fecha_ingreso
            else:
                empleado_dict["fecha_ingreso"] = None
            
            # Manejar relación con Usuario
            empleado_dict["tiene_usuario"] = False
            empleado_dict["usuario_id"] = None
            empleado_dict["usuario_email"] = None
            empleado_dict["rol"] = None
            
            if hasattr(empleado, 'usuario') and empleado.usuario is not None:
                try:
                    empleado_dict["tiene_usuario"] = True
                    empleado_dict["usuario_id"] = empleado.usuario.id_usuario
                    empleado_dict["usuario_email"] = empleado.usuario.email
                    
                    # Obtener rol desde configuración
                    if hasattr(empleado.usuario, 'configuracion') and empleado.usuario.configuracion:
                        empleado_dict["rol"] = empleado.usuario.configuracion.rol
                except Exception as e:
                    print(f"Error obteniendo datos de usuario: {e}")
            
            return empleado_dict
            
        except Exception as e:
            print(f"Error en _empleado_to_dict: {e}")
            return {
                "id_empleado": getattr(empleado, 'id_empleado', None),
                "nombre": getattr(empleado, 'nombre', 'Error al cargar'),
                "telefono": None,
                "puesto": None,
                "activo": True,
                "fecha_ingreso": None,
                "tiene_usuario": False
            }
    
    def create_empleado_con_usuario(self, empleado_data: Dict[str, Any], 
                                    usuario_data: Dict[str, Any], 
                                    rol: str = "usuario") -> Dict[str, Any]:
        """
        Crear empleado con usuario y configuración asociados.
        
        Args:
            empleado_data: Datos del empleado (nombre, telefono, puesto)
            usuario_data: Datos del usuario (nombre, email, password)
            rol: Rol del usuario ('admin' o 'usuario')
        
        Returns:
            Diccionario con el empleado creado y sus relaciones
        """
        try:
            # Validar rol
            if rol not in ['admin', 'usuario']:
                raise ValueError("El rol debe ser 'admin' o 'usuario'")
            
            # 1. Crear empleado primero (sin usuario)
            empleado_validado = self.validate_data(empleado_data)
            empleado = self.repository.create(empleado_validado)
            
            # 2. Importar modelos necesarios
            from app.models.usuario import Usuario
            from app.models.configuracion import Configuracion
            
            # 3. Crear usuario con empleado_id_fk
            password_hash = pwd_context.hash(usuario_data["password"])
            usuario = Usuario(
                nombre=usuario_data.get("nombre", empleado.nombre),
                email=usuario_data["email"],
                password=password_hash,
                empleado_id_fk=empleado.id_empleado,
                activo=True
            )
            self.repository.db.add(usuario)
            self.repository.db.flush()  # Para obtener el id_usuario
            
            # 4. Crear configuración con el rol
            configuracion = Configuracion(
                usuario_id_fk=usuario.id_usuario,
                rol=rol,
                idioma='es',
                tema='claro'
            )
            self.repository.db.add(configuracion)
            
            # 5. Commit final
            self.repository.db.commit()
            self.repository.db.refresh(empleado)
            
            return self._empleado_to_dict(empleado)
            
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en create_empleado_con_usuario: {e}")
            raise e
    
    def create_empleado_sin_usuario(self, empleado_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear empleado sin usuario asociado (solo datos de empleado).
        
        Args:
            empleado_data: Datos del empleado (nombre, telefono, puesto)
        
        Returns:
            Diccionario con el empleado creado
        """
        try:
            empleado_validado = self.validate_data(empleado_data)
            empleado = self.repository.create(empleado_validado)
            return self._empleado_to_dict(empleado)
        except Exception as e:
            print(f"Error en create_empleado_sin_usuario: {e}")
            raise e
    
    def get_all_empleados(self, skip: int = 0, limit: int = 100, 
                         incluir_inactivos: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener todos los empleados con filtros opcionales.
        
        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a devolver
            incluir_inactivos: Si True, incluye empleados inactivos
        
        Returns:
            Lista de diccionarios con empleados
        """
        try:
            from sqlalchemy.orm import joinedload
            from app.models.usuario import Usuario
            
            query = self.repository.db.query(self.repository.model).options(
                joinedload(self.repository.model.usuario).joinedload(Usuario.configuracion)
            )
            
            if not incluir_inactivos:
                query = query.filter(self.repository.model.activo == True)
            
            empleados = query.offset(skip).limit(limit).all()
            return [self._empleado_to_dict(emp) for emp in empleados]
        except Exception as e:
            print(f"Error en get_all_empleados: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_by_id(self, empleado_id: int) -> Optional[Dict[str, Any]]:
        """Obtener empleado por ID como diccionario"""
        try:
            empleado = self.repository.get_by_id(empleado_id)
            return self._empleado_to_dict(empleado)
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def update(self, empleado_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar empleado y retornar como diccionario"""
        try:
            updated_empleado = self.repository.update(empleado_id, data)
            return self._empleado_to_dict(updated_empleado)
        except Exception as e:
            print(f"Error en update empleado: {e}")
            raise e
    
    def delete(self, empleado_id: int) -> bool:
        """
        Eliminar empleado (soft delete - marcar como inactivo).
        Si tiene usuario asociado, también se desactiva.
        """
        try:
            empleado = self.repository.get_by_id(empleado_id)
            if not empleado:
                return False
            
            # Soft delete del empleado
            empleado.activo = False
            
            # Si tiene usuario, también desactivarlo
            if hasattr(empleado, 'usuario') and empleado.usuario:
                empleado.usuario.activo = False
            
            self.repository.db.commit()
            return True
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en delete empleado: {e}")
            return False
    
    def vincular_usuario_existente(self, empleado_id: int, usuario_id: int) -> Optional[Dict[str, Any]]:
        """
        Vincular un empleado existente con un usuario existente.
        
        Args:
            empleado_id: ID del empleado
            usuario_id: ID del usuario
        
        Returns:
            Diccionario con el empleado actualizado
        """
        try:
            from app.models.usuario import Usuario
            
            # Verificar que el empleado existe
            empleado = self.repository.get_by_id(empleado_id)
            if not empleado:
                raise ValueError("Empleado no encontrado")
            
            # Verificar que el usuario existe
            usuario = self.repository.db.query(Usuario).filter(
                Usuario.id_usuario == usuario_id
            ).first()
            if not usuario:
                raise ValueError("Usuario no encontrado")
            
            # Verificar que el usuario no esté vinculado a otro empleado
            if usuario.empleado_id_fk and usuario.empleado_id_fk != empleado_id:
                raise ValueError("El usuario ya está vinculado a otro empleado")
            
            # Vincular
            usuario.empleado_id_fk = empleado_id
            self.repository.db.commit()
            self.repository.db.refresh(empleado)
            
            return self._empleado_to_dict(empleado)
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en vincular_usuario_existente: {e}")
            raise e