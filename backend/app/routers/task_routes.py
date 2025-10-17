# Archivo 38/40: app/routers/task_routes.py
# Descripción: Rutas API para tareas - /api/tasks/*
# Funcionalidad: CRUD de tareas y endpoints para sistema Kanban
# ✅ ACTUALIZADO: Usa 'en_progreso' para mejor estética

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.task_controller import TaskController
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.utility_service import UtilityService

router = APIRouter()

def get_task_controller(db: Session = Depends(get_db)) -> TaskController:
    """Dependency para obtener controlador de tareas"""
    task_repo = RepositoryFactory.create_task_repository(db)
    return TaskController(task_repo)

@router.get("/", response_model=dict)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    estado: Optional[str] = Query(None, regex="^(nuevo|en_progreso|finalizado)$"),  # ✅ ACTUALIZADO
    task_controller: TaskController = Depends(get_task_controller)
):
    """Obtener lista de tareas con filtros opcionales"""
    try:
        if estado:
            tasks = task_controller.get_by_estado(estado)
        else:
            tasks = task_controller.get_all_tasks(skip=skip, limit=limit)
        
        return UtilityService.success_response(
            data=tasks,
            message=f"Se encontraron {len(tasks)} tareas"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener tareas")

@router.get("/kanban", response_model=dict)
async def get_kanban_board(
    task_controller: TaskController = Depends(get_task_controller)
):
    """Obtener tablero Kanban completo con tareas agrupadas por estado"""
    try:
        kanban_data = task_controller.get_kanban_board()
        return UtilityService.success_response(
            data=kanban_data,
            message="Tablero Kanban obtenido exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener tablero Kanban")

@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller)
):
    """Obtener tarea específica por ID"""
    try:
        task = task_controller.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return UtilityService.success_response(
            data=task,
            message="Tarea obtenida exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener tarea")

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    task_controller: TaskController = Depends(get_task_controller)
):
    """Crear nueva tarea"""
    try:
        task = task_controller.create(task_data.model_dump())
        return UtilityService.success_response(
            data=task,
            message="Tarea creada exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear tarea")

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_controller: TaskController = Depends(get_task_controller)
):
    """Actualizar tarea existente"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in task_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        task = task_controller.update(task_id, update_data)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return UtilityService.success_response(
            data=task,
            message="Tarea actualizada exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar tarea")

@router.patch("/{task_id}/estado", response_model=dict)
async def update_task_estado(
    task_id: int,
    nuevo_estado: str = Query(..., regex="^(nuevo|en_progreso|finalizado)$"),  # ✅ ACTUALIZADO
    task_controller: TaskController = Depends(get_task_controller)
):
    """Actualizar estado de tarea para movimiento en Kanban"""
    try:
        task = task_controller.update_task_estado(task_id, nuevo_estado)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return UtilityService.success_response(
            data=task,
            message=f"Estado de tarea actualizado a '{nuevo_estado}'"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar estado")

@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller)
):
    """Eliminar tarea"""
    try:
        success = task_controller.delete(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return UtilityService.success_response(
            message="Tarea eliminada exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar tarea")