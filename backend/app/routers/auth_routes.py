# Archivo 37/43: app/routers/auth_routes.py (VERSIÓN COMPLETA CORREGIDA)
# Descripción: Rutas API para autenticación - /api/auth/*
# Funcionalidad: Login, registro y validación de usuarios

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError, jwt

from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.utility_service import UtilityService
from app.config import JWT_CONFIG

router = APIRouter()

def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    """Dependency para obtener controlador de autenticación"""
    user_repo = RepositoryFactory.create_user_repository(db)
    return AuthController(user_repo)


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """Registrar nuevo usuario en el sistema"""
    try:
        user = auth_controller.register_user(user_data.model_dump())
        return UtilityService.success_response(
            data={"id_usuario": user.id_usuario, "email": user.email},
            message="Usuario registrado exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/login", response_model=dict)
async def login_user(
    login_data: UserLogin,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """Iniciar sesión y obtener token JWT"""
    try:
        result = auth_controller.login(login_data.email, login_data.password)
        return UtilityService.success_response(
            data=result,
            message="Login exitoso"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/me", response_model=dict)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """
    Obtener información del usuario actual autenticado
    ✅ VERSIÓN CORREGIDA - Decodifica el JWT y retorna datos reales del usuario
    """
    try:
        # Verificar que el header Authorization existe
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó token de autenticación",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extraer el token del header "Bearer <token>"
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Formato de token inválido. Use: Bearer <token>",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        token = parts[1]
        
        # Decodificar el token JWT
        try:
            payload = jwt.decode(
                token,
                JWT_CONFIG["secret_key"],
                algorithms=[JWT_CONFIG["algorithm"]]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido: sin identificador de usuario"
                )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido o expirado: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Obtener el usuario de la base de datos
        user = auth_controller.repository.get_by_id(int(user_id))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Retornar datos del usuario (sin la contraseña)
        user_data = {
            "id_usuario": user.id_usuario,
            "nombre": user.nombre,
            "email": user.email,
            "rol": "admin" if hasattr(user, 'rol') else "usuario",
            "activo": user.activo
        }
        
        return UtilityService.success_response(
            data=user_data,
            message="Usuario autenticado"
        )
        
    except HTTPException:
        # Re-lanzar excepciones HTTP sin modificar
        raise
    except Exception as e:
        print(f"❌ Error en get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/verify-token")
async def verify_token(
    token: str,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """Verificar validez de token JWT"""
    try:
        payload = auth_controller.verify_token(token)
        if payload:
            return UtilityService.success_response(
                data=payload,
                message="Token válido"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")