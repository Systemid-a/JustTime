# Archivo: app/routers/pending_activity_routes.py
# Descripción: Rutas API para actividades pendientes - /api/pending-activities/*
# Funcionalidad: CRUD de actividades pendientes y recordatorios

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.pending_activity_controller import PendingActivityController
from app.schemas.pending_activity_schema import PendingActivityCreate, PendingActivityUpdate, PendingActivityResponse
from app.services.utility_service import UtilityService

router = APIRouter()

def get_pending_activity_controller(db: Session = Depends(get_db)) -> PendingActivityController:
    """Dependency para obtener controlador de actividades pendientes"""
    pending_activity_repo = RepositoryFactory.create_pending_activity_repository(db)
    return PendingActivityController(pending_activity_repo)

@router.get("/", response_model=dict)
async def get_pending_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    completada: Optional[bool] = Query(None, description="Filtrar por estado de completado"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    prioridad: Optional[str] = Query(None, regex="^(baja|media|alta)$"),
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener lista de actividades pendientes con filtros opcionales"""
    try:
        if usuario_id and completada is not None:
            # Filtrar por usuario y estado
            if completada:
                activities = pending_activity_controller.get_completadas(usuario_id=usuario_id)
            else:
                activities = pending_activity_controller.get_pendientes(usuario_id=usuario_id)
        elif usuario_id:
            activities = pending_activity_controller.get_by_usuario(usuario_id)
        elif completada is not None:
            activities = pending_activity_controller.get_all_activities(skip=skip, limit=limit, completada=completada)
        elif prioridad:
            activities = pending_activity_controller.get_by_prioridad(prioridad)
        else:
            activities = pending_activity_controller.get_all_activities(skip=skip, limit=limit)
        
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades pendientes")

@router.get("/pendientes", response_model=dict)
async def get_pendientes(
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividades pendientes (no completadas)"""
    try:
        activities = pending_activity_controller.get_pendientes(usuario_id=usuario_id)
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades pendientes"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades pendientes")

@router.get("/completadas", response_model=dict)
async def get_completadas(
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividades completadas"""
    try:
        activities = pending_activity_controller.get_completadas(usuario_id=usuario_id)
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades completadas"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades completadas")

@router.get("/vencidas", response_model=dict)
async def get_vencidas(
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividades vencidas (no completadas y con fecha pasada)"""
    try:
        activities = pending_activity_controller.get_vencidas(usuario_id=usuario_id)
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades vencidas"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades vencidas")

@router.get("/usuario/{usuario_id}", response_model=dict)
async def get_by_usuario(
    usuario_id: int,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividades de un usuario específico"""
    try:
        activities = pending_activity_controller.get_by_usuario(usuario_id)
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades para el usuario"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades del usuario")

@router.get("/proyecto/{proyecto_id}", response_model=dict)
async def get_by_proyecto(
    proyecto_id: int,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividades de un proyecto específico"""
    try:
        activities = pending_activity_controller.get_by_proyecto(proyecto_id)
        return UtilityService.success_response(
            data=activities,
            message=f"Se encontraron {len(activities)} actividades para el proyecto"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividades del proyecto")

@router.get("/{activity_id}", response_model=dict)
async def get_activity(
    activity_id: int,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Obtener actividad específica por ID"""
    try:
        activity = pending_activity_controller.get_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        return UtilityService.success_response(
            data=activity,
            message="Actividad obtenida exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener actividad")

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: PendingActivityCreate,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Crear nueva actividad pendiente"""
    try:
        activity = pending_activity_controller.create(activity_data.model_dump())
        return UtilityService.success_response(
            data=activity,
            message="Actividad creada exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear actividad")

@router.put("/{activity_id}", response_model=dict)
async def update_activity(
    activity_id: int,
    activity_data: PendingActivityUpdate,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Actualizar actividad existente"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in activity_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        activity = pending_activity_controller.update(activity_id, update_data)
        if not activity:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        return UtilityService.success_response(
            data=activity,
            message="Actividad actualizada exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar actividad")

@router.patch("/{activity_id}/completar", response_model=dict)
async def marcar_completada(
    activity_id: int,
    completada: bool = Query(True, description="Marcar como completada (true) o pendiente (false)"),
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Marcar actividad como completada o pendiente"""
    try:
        activity = pending_activity_controller.marcar_completada(activity_id, completada)
        if not activity:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        estado = "completada" if completada else "pendiente"
        return UtilityService.success_response(
            data=activity,
            message=f"Actividad marcada como {estado}"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar estado")

@router.delete("/{activity_id}", response_model=dict)
async def delete_activity(
    activity_id: int,
    pending_activity_controller: PendingActivityController = Depends(get_pending_activity_controller)
):
    """Eliminar actividad"""
    try:
        success = pending_activity_controller.delete(activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        return UtilityService.success_response(
            message="Actividad eliminada exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar actividad")