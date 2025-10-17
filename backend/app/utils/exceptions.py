# Archivo 42/43: app/utils/exceptions.py
# Descripción: Excepciones personalizadas del sistema
# Funcionalidad: Manejo de errores específicos de JustTime

from fastapi import HTTPException
from typing import Any, Dict, Optional


class JustTimeException(HTTPException):
    """
    Excepción base personalizada para JustTime.
    Extiende HTTPException con información adicional.
    """
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str = "general_error",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_type = error_type


class ValidationError(JustTimeException):
    """Excepción para errores de validación de datos"""
    
    def __init__(self, detail: str, field: str = None):
        super().__init__(
            status_code=400,
            detail=detail,
            error_type="validation_error"
        )
        self.field = field


class AuthenticationError(JustTimeException):
    """Excepción para errores de autenticación"""
    
    def __init__(self, detail: str = "Credenciales inválidas"):
        super().__init__(
            status_code=401,
            detail=detail,
            error_type="authentication_error",
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(JustTimeException):
    """Excepción para errores de autorización"""
    
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            status_code=403,
            detail=detail,
            error_type="authorization_error"
        )


class NotFoundError(JustTimeException):
    """Excepción para recursos no encontrados"""
    
    def __init__(self, resource: str = "Recurso", detail: str = None):
        if not detail:
            detail = f"{resource} no encontrado"
        super().__init__(
            status_code=404,
            detail=detail,
            error_type="not_found_error"
        )


class BusinessLogicError(JustTimeException):
    """Excepción para errores de lógica de negocio"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_type="business_logic_error"
        )