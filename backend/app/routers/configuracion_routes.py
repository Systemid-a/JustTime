# Archivo: app/routers/configuracion_routes.py
# Descripción: Rutas API para configuraciones - /api/configuraciones/*
# Funcionalidad: CRUD de configuraciones de usuario

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.configuracion_controller import ConfiguracionController
from app.schemas.configuracion_schema import ConfiguracionCreate, ConfiguracionUpdate, ConfiguracionResponse
from app.services.utility_service import UtilityService

router = APIRouter()


def get_config_controller(db: Session = Depends(get_db)) -> ConfiguracionController:
    """Dependency para obtener controlador de configuraciones"""
    config_repo = RepositoryFactory.create_configuracion_repository(db)
    return ConfiguracionController(config_repo)


@router.get("/", response_model=dict)
async def get_all_configs(
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Obtener todas las configuraciones (uso administrativo)"""
    try:
        configs = config_controller.repository.get_all()
        config_dicts = [config_controller._config_to_dict(c) for c in configs]
        
        return UtilityService.success_response(
            data=config_dicts,
            message=f"Se encontraron {len(config_dicts)} configuraciones"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener configuraciones")


@router.get("/{config_id}", response_model=dict)
async def get_config(
    config_id: int,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Obtener configuración específica por ID"""
    try:
        config = config_controller.get_by_id(config_id)
        if not config:
            raise HTTPException(status_code=404, detail="Configuración no encontrada")
        
        return UtilityService.success_response(
            data=config,
            message="Configuración obtenida exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener configuración")


@router.get("/usuario/{usuario_id}", response_model=dict)
async def get_config_by_usuario(
    usuario_id: int,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Obtener configuración de un usuario específico"""
    try:
        config = config_controller.get_by_usuario(usuario_id)
        if not config:
            raise HTTPException(status_code=404, detail="Configuración no encontrada para este usuario")
        
        return UtilityService.success_response(
            data=config,
            message="Configuración del usuario obtenida exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener configuración del usuario")


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_config(
    config_data: ConfiguracionCreate,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Crear nueva configuración"""
    try:
        config = config_controller.create(config_data.model_dump())
        return UtilityService.success_response(
            data=config,
            message="Configuración creada exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear configuración")


@router.put("/{config_id}", response_model=dict)
async def update_config(
    config_id: int,
    config_data: ConfiguracionUpdate,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Actualizar configuración existente"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in config_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        config = config_controller.update(config_id, update_data)
        if not config:
            raise HTTPException(status_code=404, detail="Configuración no encontrada")
        
        return UtilityService.success_response(
            data=config,
            message="Configuración actualizada exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar configuración")


@router.put("/usuario/{usuario_id}", response_model=dict)
async def update_config_by_usuario(
    usuario_id: int,
    config_data: ConfiguracionUpdate,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Actualizar configuración por ID de usuario"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in config_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        config = config_controller.update_by_usuario(usuario_id, update_data)
        if not config:
            raise HTTPException(status_code=404, detail="Configuración no encontrada para este usuario")
        
        return UtilityService.success_response(
            data=config,
            message="Configuración del usuario actualizada exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar configuración del usuario")


@router.delete("/{config_id}", response_model=dict)
async def delete_config(
    config_id: int,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Eliminar configuración"""
    try:
        success = config_controller.delete(config_id)
        if not success:
            raise HTTPException(status_code=404, detail="Configuración no encontrada")
        
        return UtilityService.success_response(
            message="Configuración eliminada exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar configuración")


@router.delete("/usuario/{usuario_id}", response_model=dict)
async def delete_config_by_usuario(
    usuario_id: int,
    config_controller: ConfiguracionController = Depends(get_config_controller)
):
    """Eliminar configuración por ID de usuario"""
    try:
        success = config_controller.delete_by_usuario(usuario_id)
        if not success:
            raise HTTPException(status_code=404, detail="Configuración no encontrada para este usuario")
        
        return UtilityService.success_response(
            message="Configuración del usuario eliminada exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar configuración del usuario")