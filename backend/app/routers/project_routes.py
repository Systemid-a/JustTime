# Archivo 39/43: app/routers/project_routes.py
# Descripción: Rutas API para proyectos - /api/projects/*
# Funcionalidad: CRUD de proyectos jurídicos con filtros y estadísticas

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.project_controller import ProjectController
from app.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.utility_service import UtilityService

router = APIRouter()

def get_project_controller(db: Session = Depends(get_db)) -> ProjectController:
    """Dependency para obtener controlador de proyectos"""
    project_repo = RepositoryFactory.create_project_repository(db)
    return ProjectController(project_repo)

@router.get("/", response_model=dict)
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    estado: Optional[str] = Query(None, regex="^(activo|pausado|finalizado)$"),
    categoria_id: Optional[int] = Query(None, ge=1),
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Obtener lista de proyectos con filtros opcionales"""
    try:
        if estado:
            projects = project_controller.get_by_estado(estado)
        elif categoria_id:
            projects = project_controller.get_by_categoria(categoria_id)
        else:
            projects = project_controller.get_all_projects(skip=skip, limit=limit)  # ✅ CORREGIDO: Cambió de get_all() a get_all_projects()
        
        return UtilityService.success_response(
            data=projects,
            message=f"Se encontraron {len(projects)} proyectos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener proyectos")

@router.get("/dashboard/stats", response_model=dict)
async def get_dashboard_stats(
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Obtener estadísticas de proyectos para dashboard"""
    try:
        stats = project_controller.get_dashboard_stats()
        return UtilityService.success_response(
            data=stats,
            message="Estadísticas obtenidas exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener estadísticas")

@router.get("/activos", response_model=dict)
async def get_active_projects(
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Obtener proyectos activos"""
    try:
        projects = project_controller.get_activos()
        return UtilityService.success_response(
            data=projects,
            message=f"Se encontraron {len(projects)} proyectos activos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener proyectos activos")

@router.get("/{project_id}", response_model=dict)
async def get_project(
    project_id: int,
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Obtener proyecto específico por ID"""
    try:
        project = project_controller.get_project_by_id(project_id)  # ✅ CORREGIDO: Cambió de get_by_id() a get_project_by_id()
        if not project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        return UtilityService.success_response(
            data=project,
            message="Proyecto obtenido exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener proyecto")

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Crear nuevo proyecto"""
    try:
        project = project_controller.create(project_data.model_dump())
        return UtilityService.success_response(
            data=project,
            message="Proyecto creado exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear proyecto")

@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Actualizar proyecto existente"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in project_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        project = project_controller.update(project_id, update_data)
        if not project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        return UtilityService.success_response(
            data=project,
            message="Proyecto actualizado exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar proyecto")

@router.patch("/{project_id}/finalizar", response_model=dict)
async def finalize_project(
    project_id: int,
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Finalizar proyecto (cambiar estado a finalizado)"""
    try:
        project = project_controller.finalizar_proyecto(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        return UtilityService.success_response(
            data=project,
            message="Proyecto finalizado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al finalizar proyecto")

@router.delete("/{project_id}", response_model=dict)
async def delete_project(
    project_id: int,
    project_controller: ProjectController = Depends(get_project_controller)
):
    """Eliminar proyecto"""
    try:
        success = project_controller.delete(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        return UtilityService.success_response(
            message="Proyecto eliminado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar proyecto")