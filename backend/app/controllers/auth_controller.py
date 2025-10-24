# Archivo 22/43: app/controllers/auth_controller.py - VERSIÓN POST-MIGRACIÓN ✅
# Descripción: Controlador de autenticación - Login, registro y JWT
# Funcionalidad: Manejo completo de autenticación de usuarios
# ✅ ACTUALIZADO: Flujo cambiado - Primero Empleado, luego Usuario (como Odoo)

from typing import Dict, Any, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.controllers.base_controller import BaseController
from app.factory import BaseRepository
from app.config import JWT_CONFIG


class AuthController(BaseController):
    """
    Controlador de autenticación con JWT.
    Maneja login, registro y validación de tokens.
    
    CAMBIOS POST-MIGRACIÓN:
    ✅ Flujo actualizado: Empleado → Usuario → Configuración
    ✅ Usuario ahora tiene empleado_id_fk (apunta a empleado)
    ✅ Empleado ya NO tiene usuario_id_fk
    """
    
    def __init__(self, repository: BaseRepository):
        super().__init__(repository)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos de usuario"""
        required_fields = ["nombre", "email", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo {field} es requerido")
        return data
    
    def hash_password(self, password: str) -> str:
        """Encriptar contraseña con bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        """Crear token JWT con expiración"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWT_CONFIG["expire_minutes"])
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode, 
            JWT_CONFIG["secret_key"], 
            algorithm=JWT_CONFIG["algorithm"]
        )
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(
                token, 
                JWT_CONFIG["secret_key"], 
                algorithms=[JWT_CONFIG["algorithm"]]
            )
            return payload
        except JWTError:
            return None
    
    def register_user(self, user_data: Dict[str, Any]) -> Any:
        """
        Registrar usuario con el NUEVO FLUJO post-migración.
        
        FLUJO ACTUALIZADO (como Odoo):
        1. Crear EMPLEADO primero (sin usuario asociado)
        2. Crear USUARIO con empleado_id_fk apuntando al empleado
        3. Crear CONFIGURACIÓN con rol='usuario'
        
        ANTES (incorrecto):
        Usuario → Empleado (empleado.usuario_id_fk)
        
        AHORA (correcto):
        Empleado ← Usuario (usuario.empleado_id_fk)
        
        Args:
            user_data: Diccionario con nombre, email y password
            
        Returns:
            Usuario creado con empleado y configuración asociados
            
        Raises:
            ValueError: Si el email ya está registrado o datos inválidos
        """
        try:
            # Validar datos de entrada
            validated_data = self.validate_data(user_data)
            
            # Verificar si el email ya existe
            existing_user = self.get_user_by_email(validated_data["email"])
            if existing_user:
                raise ValueError("El email ya está registrado")
            
            # Encriptar contraseña antes de guardar
            validated_data["password"] = self.hash_password(validated_data["password"])
            
            # ==========================================
            # 1. CREAR EMPLEADO PRIMERO (SIN USUARIO)
            # ==========================================
            from app.models.empleado import Empleado
            empleado = Empleado(
                nombre=validated_data["nombre"],
                puesto="Sin asignar",           # Puesto por defecto
                telefono=None,                  # Sin teléfono inicialmente
                activo=True                     # Empleado activo
                # ✅ NO tiene usuario_id_fk (columna eliminada)
            )
            self.repository.db.add(empleado)
            self.repository.db.flush()  # Obtener el id_empleado generado
            print(f"✅ [1/3] Empleado creado: {empleado.nombre} (ID: {empleado.id_empleado})")
            
            # ==========================================
            # 2. CREAR USUARIO CON REFERENCIA AL EMPLEADO
            # ==========================================
            from app.models.usuario import Usuario
            user = Usuario(
                nombre=validated_data["nombre"],
                email=validated_data["email"],
                password=validated_data["password"],
                activo=True,
                empleado_id_fk=empleado.id_empleado  # ✅ Usuario apunta a empleado
            )
            self.repository.db.add(user)
            self.repository.db.flush()  # Obtener el id_usuario generado
            print(f"✅ [2/3] Usuario creado: {user.email} (ID: {user.id_usuario}, empleado_id: {user.empleado_id_fk})")
            
            # ==========================================
            # 3. CREAR CONFIGURACIÓN CON ROL 'usuario'
            # ==========================================
            from app.models.configuracion import Configuracion
            configuracion = Configuracion(
                usuario_id_fk=user.id_usuario,  # Relación 1:1 con usuario
                idioma='es',      # Español por defecto
                rol='usuario',    # Usuario regular (NO admin)
                tema='claro'      # Tema claro por defecto
            )
            self.repository.db.add(configuracion)
            print(f"✅ [3/3] Configuración creada (rol: usuario, idioma: es, tema: claro)")
            
            # ==========================================
            # 4. CONFIRMAR TODOS LOS CAMBIOS EN LA BD
            # ==========================================
            self.repository.db.commit()
            self.repository.db.refresh(user)
            
            print(f"🎉 Registro completo exitoso:")
            print(f"   • Empleado ID: {empleado.id_empleado}")
            print(f"   • Usuario: {user.email}")
            print(f"   • Relación: usuario.empleado_id_fk = {user.empleado_id_fk}")
            print(f"   • Configuración: Creada")
            
            return user
            
        except ValueError:
            # Re-lanzar errores de validación sin modificar
            raise
        except Exception as e:
            # Revertir TODOS los cambios si algo falla
            self.repository.db.rollback()
            print(f"❌ Error en register_user: {e}")
            raise ValueError(f"Error al registrar usuario: {str(e)}")
    
    def authenticate_user(self, email: str, password: str) -> Optional[Any]:
        """
        Autenticar usuario con email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Usuario si las credenciales son correctas, None en caso contrario
        """
        try:
            user = self.get_user_by_email(email)
            if user and self.verify_password(password, user.password):
                return user
            return None
        except Exception as e:
            print(f"Error en authenticate_user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Any]:
        """
        Obtener usuario por email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Usuario si existe, None en caso contrario
        """
        try:
            from app.models.usuario import Usuario
            return self.repository.db.query(Usuario).filter(
                Usuario.email == email
            ).first()
        except Exception as e:
            print(f"Error en get_user_by_email: {e}")
            return None
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Proceso completo de login con generación de token JWT.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Diccionario con access_token, token_type y datos del usuario (incluyendo rol)
            
        Raises:
            ValueError: Si las credenciales son inválidas o el usuario está inactivo
        """
        try:
            # Autenticar usuario
            user = self.authenticate_user(email, password)
            if not user:
                raise ValueError("Credenciales inválidas")
            
            # Verificar que el usuario esté activo
            if not user.activo:
                raise ValueError("Usuario inactivo. Contacte al administrador.")
            
            # Obtener configuración del usuario para incluir el rol
            from app.models.configuracion import Configuracion
            configuracion = self.repository.db.query(Configuracion).filter(
                Configuracion.usuario_id_fk == user.id_usuario
            ).first()
            
            # Determinar rol (fallback a 'usuario' si no tiene configuración)
            rol = configuracion.rol if configuracion else 'usuario'
            
            # Crear token JWT con datos del usuario
            access_token = self.create_access_token({
                "sub": str(user.id_usuario),
                "email": user.email,
                "rol": rol
            })
            
            # Retornar respuesta completa
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id_usuario": user.id_usuario,
                    "nombre": user.nombre,
                    "email": user.email,
                    "rol": rol,  # Incluir rol en respuesta
                    "activo": user.activo,
                    "empleado_id": user.empleado_id_fk  # ✅ Incluir referencia al empleado
                }
            }
        except ValueError:
            # Re-lanzar errores de validación
            raise
        except Exception as e:
            print(f"Error en login: {e}")
            raise ValueError("Error al procesar el login")