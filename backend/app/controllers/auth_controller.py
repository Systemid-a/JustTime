# Archivo 22/43: app/controllers/auth_controller.py - VERSIÓN CORREGIDA
# Descripción: Controlador de autenticación - Login, registro y JWT
# Funcionalidad: Manejo completo de autenticación de usuarios

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
        """Encriptar contraseña"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        """Crear token JWT"""
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
        """Registrar nuevo usuario"""
        try:
            validated_data = self.validate_data(user_data)
            
            # Verificar si email ya existe
            existing_user = self.get_user_by_email(validated_data["email"])
            if existing_user:
                raise ValueError("El email ya está registrado")
            
            # Encriptar contraseña
            validated_data["password"] = self.hash_password(validated_data["password"])
            
            return self.create(validated_data)
        except Exception as e:
            print(f"Error en register_user: {e}")
            raise e
    
    def authenticate_user(self, email: str, password: str) -> Optional[Any]:
        """Autenticar usuario con email y contraseña"""
        try:
            user = self.get_user_by_email(email)
            if user and self.verify_password(password, user.password):
                return user
            return None
        except Exception as e:
            print(f"Error en authenticate_user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Any]:
        """Obtener usuario por email"""
        try:
            # El modelo Usuario tiene el campo 'email', no 'email'
            from app.models.usuario import Usuario
            return self.repository.db.query(Usuario).filter(
                Usuario.email == email
            ).first()
        except Exception as e:
            print(f"Error en get_user_by_email: {e}")
            return None
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Proceso completo de login"""
        try:
            user = self.authenticate_user(email, password)
            if not user:
                raise ValueError("Credenciales inválidas")
            
            if not user.activo:
                raise ValueError("Usuario inactivo")
            
            # Crear token
            access_token = self.create_access_token({"sub": str(user.id_usuario)})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id_usuario": user.id_usuario,
                    "nombre": user.nombre,
                    "email": user.email,
                    "activo": user.activo
                }
            }
        except Exception as e:
            print(f"Error en login: {e}")
            raise e