# Archivo: app/routers/employee_routes.py
# Descripción: Rutas API para empleados - /api/empleados/*
# Funcionalidad: CRUD de empleados con gestión de usuarios y roles

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.employee_controller import EmpleadoController
from app.schemas.employee_schema import (
    EmpleadoCreate, 
    EmpleadoConUsuarioCreate,
    EmpleadoUpdate, 
    EmpleadoResponse,
    VincularUsuarioRequest
)
from app.services.utility_service import UtilityService

router = APIRouter()


def get_empleado_controller(db: Session = Depends(get_db)) -> EmpleadoController:
    """Dependency para obtener controlador de empleados"""
    from app.models.empleado import Empleado
    from app.factory import BaseRepository
    empleado_repo = BaseRepository(Empleado, db)
    return EmpleadoController(empleado_repo)


@router.get("/", response_model=dict)
async def get_empleados(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    incluir_inactivos: bool = Query(False, description="Incluir empleados inactivos"),
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Obtener lista de empleados.
    Por defecto solo muestra empleados activos.
    """
    try:
        empleados = empleado_controller.get_all_empleados(
            skip=skip, 
            limit=limit, 
            incluir_inactivos=incluir_inactivos
        )
        
        return UtilityService.success_response(
            data=empleados,
            message=f"Se encontraron {len(empleados)} empleados"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener empleados: {str(e)}"
        )


@router.get("/{empleado_id}", response_model=dict)
async def get_empleado(
    empleado_id: int,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """Obtener empleado específico por ID con información de usuario si existe"""
    try:
        empleado = empleado_controller.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        return UtilityService.success_response(
            data=empleado,
            message="Empleado obtenido exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener empleado: {str(e)}"
        )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_empleado_simple(
    empleado_data: EmpleadoCreate,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Crear empleado SIN usuario asociado.
    Solo crea el registro de empleado.
    """
    try:
        empleado = empleado_controller.create_empleado_sin_usuario(
            empleado_data.model_dump()
        )
        
        return UtilityService.success_response(
            data=empleado,
            message="Empleado creado exitosamente (sin usuario)"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al crear empleado: {str(e)}"
        )


@router.post("/con-usuario", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_empleado_con_usuario(
    empleado_data: EmpleadoConUsuarioCreate,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Crear empleado CON usuario y configuración asociados.
    
    Crea:
    1. Empleado (nombre, telefono, puesto)
    2. Usuario (email, password) vinculado al empleado
    3. Configuración con el rol especificado ('admin' o 'usuario')
    
    Roles:
    - 'admin': Puede crear, modificar y eliminar
    - 'usuario': Solo puede ver sin modificar
    """
    try:
        # Separar datos
        empleado_dict = {
            "nombre": empleado_data.nombre,
            "telefono": empleado_data.telefono,
            "puesto": empleado_data.puesto
        }
        
        usuario_dict = {
            "nombre": empleado_data.nombre,
            "email": empleado_data.email,
            "password": empleado_data.password
        }
        
        # Crear empleado con usuario
        empleado = empleado_controller.create_empleado_con_usuario(
            empleado_data=empleado_dict,
            usuario_data=usuario_dict,
            rol=empleado_data.rol
        )
        
        return UtilityService.success_response(
            data=empleado,
            message=f"Empleado y usuario creados exitosamente con rol '{empleado_data.rol}'"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al crear empleado con usuario: {str(e)}"
        )


@router.put("/{empleado_id}", response_model=dict)
async def update_empleado(
    empleado_id: int,
    empleado_data: EmpleadoUpdate,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Actualizar datos de empleado.
    Solo actualiza campos del empleado, no del usuario.
    """
    try:
        # Filtrar datos None
        update_data = {
            k: v for k, v in empleado_data.model_dump().items() 
            if v is not None
        }
        
        if not update_data:
            raise HTTPException(
                status_code=400, 
                detail="No hay datos para actualizar"
            )
        
        empleado = empleado_controller.update(empleado_id, update_data)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        return UtilityService.success_response(
            data=empleado,
            message="Empleado actualizado exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al actualizar empleado: {str(e)}"
        )


@router.delete("/{empleado_id}", response_model=dict)
async def delete_empleado(
    empleado_id: int,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Eliminar empleado (soft delete).
    Marca el empleado como inactivo.
    Si tiene usuario asociado, también se desactiva.
    """
    try:
        success = empleado_controller.delete(empleado_id)
        if not success:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        return UtilityService.success_response(
            message="Empleado desactivado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al eliminar empleado: {str(e)}"
        )


@router.post("/{empleado_id}/vincular-usuario", response_model=dict)
async def vincular_usuario_a_empleado(
    empleado_id: int,
    vincular_data: VincularUsuarioRequest,
    empleado_controller: EmpleadoController = Depends(get_empleado_controller)
):
    """
    Vincular un usuario existente a un empleado existente.
    Útil cuando se crea el usuario primero y luego se vincula al empleado.
    """
    try:
        empleado = empleado_controller.vincular_usuario_existente(
            empleado_id=empleado_id,
            usuario_id=vincular_data.usuario_id
        )
        
        return UtilityService.success_response(
            data=empleado,
            message="Usuario vinculado al empleado exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al vincular usuario: {str(e)}"
        )