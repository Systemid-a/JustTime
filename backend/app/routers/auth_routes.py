# Archivo 37/43: app/routers/auth_routes.py - VERSIÓN FINAL ✅
# Descripción: Rutas API para autenticación - /api/auth/*
# Funcionalidad: Login, registro y validación de usuarios
# ✅ IMPLEMENTADO: Endpoint /me incluye rol, idioma y tema desde configuraciones

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
    """
    Registrar nuevo usuario en el sistema.
    
    Crea automáticamente:
    - Usuario en tabla 'usuarios'
    - Empleado en tabla 'empleados' (relación 1:1)
    - Configuración en tabla 'configuraciones' con rol='usuario'
    
    Args:
        user_data: Datos del usuario (nombre, email, password)
        
    Returns:
        Información del usuario creado
        
    Raises:
        HTTPException 400: Si el email ya está registrado o datos inválidos
        HTTPException 500: Si ocurre un error interno del servidor
    """
    try:
        user = auth_controller.register_user(user_data.model_dump())
        return UtilityService.success_response(
            data={
                "id_usuario": user.id_usuario,
                "nombre": user.nombre,
                "email": user.email,
                "mensaje": "Usuario, empleado y configuración creados exitosamente"
            },
            message="Registro exitoso"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"❌ Error en register_user endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al registrar usuario"
        )


@router.post("/login", response_model=dict)
async def login_user(
    login_data: UserLogin,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """
    Iniciar sesión y obtener token JWT.
    
    Args:
        login_data: Email y contraseña del usuario
        
    Returns:
        Token JWT y datos del usuario (incluyendo rol)
        
    Raises:
        HTTPException 401: Si las credenciales son inválidas
        HTTPException 500: Si ocurre un error interno del servidor
    """
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
        print(f"❌ Error en login endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al procesar login"
        )


@router.get("/me", response_model=dict)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """
    Obtener información del usuario actual autenticado.
    
    Retorna datos del usuario incluyendo:
    - id_usuario
    - nombre
    - email
    - rol (desde tabla configuraciones)
    - idioma (desde tabla configuraciones)
    - tema (desde tabla configuraciones)
    - activo
    
    Args:
        authorization: Header con token JWT (formato: Bearer <token>)
        
    Returns:
        Información completa del usuario autenticado
        
    Raises:
        HTTPException 401: Si no hay token o es inválido
        HTTPException 403: Si el usuario está inactivo
        HTTPException 404: Si el usuario no existe
        HTTPException 500: Si ocurre un error interno
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
                detail="Usuario inactivo. Contacte al administrador."
            )
        
        # Obtener configuración del usuario (rol, idioma, tema)
        from app.models.configuracion import Configuracion
        configuracion = db.query(Configuracion).filter(
            Configuracion.usuario_id_fk == user.id_usuario
        ).first()
        
        # Valores por defecto si no existe configuración
        rol = configuracion.rol if configuracion else 'usuario'
        idioma = configuracion.idioma if configuracion else 'es'
        tema = configuracion.tema if configuracion else 'claro'
        
        # Construir respuesta completa
        user_data = {
            "id_usuario": user.id_usuario,
            "nombre": user.nombre,
            "email": user.email,
            "rol": rol,           # Desde tabla configuraciones
            "idioma": idioma,     # Desde tabla configuraciones
            "tema": tema,         # Desde tabla configuraciones
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
        print(f"❌ Error en get_current_user endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener usuario actual"
        )


@router.post("/verify-token", response_model=dict)
async def verify_token(
    token: str,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    """
    Verificar validez de un token JWT.
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        Payload del token si es válido
        
    Raises:
        HTTPException 401: Si el token es inválido o expirado
        HTTPException 500: Si ocurre un error interno
    """
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
                detail="Token inválido o expirado"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en verify_token endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al verificar token"
        )