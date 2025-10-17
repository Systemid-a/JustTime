# Archivo 46/43: app/routers/template_routes.py - NUEVO
# Descripción: Rutas API para gestión de plantillas de documentos
# Endpoints: Upload, List, Download, Update, Delete

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os

from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.template_controller import TemplateController
from app.schemas.template_schema import (
    TemplateCreate, 
    TemplateUpdate, 
    TemplateResponse,
    TemplateListResponse,
    FileUploadResponse
)
from app.services.utility_service import UtilityService
from app.services.file_service import FileService


router = APIRouter()


def get_template_controller(db: Session = Depends(get_db)) -> TemplateController:
    """Dependency para obtener controlador de plantillas"""
    from app.models.plantilla import Plantilla
    template_repo = RepositoryFactory.create_repository(Plantilla, db)
    file_service = FileService()
    return TemplateController(template_repo, file_service)


# ============================================================================
# ENDPOINTS DE PLANTILLAS
# ============================================================================

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_template(
    file: UploadFile = File(..., description="Archivo .docx de la plantilla"),
    nombre: str = Form(..., description="Nombre descriptivo de la plantilla"),
    categoria: Optional[str] = Form(None, description="Categoría jurídica"),
    descripcion: Optional[str] = Form(None, description="Descripción opcional"),
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    📤 **Subir nueva plantilla .docx**
    
    **Validaciones:**
    - Solo archivos .docx
    - Máximo 5MB
    - Nombre obligatorio
    
    **Categorías disponibles:**
    contrato, demanda, escritura, poder, memorial, dictamen, otro
    """
    try:
        template_data = {
            'nombre': nombre,
            'categoria': categoria,
            'descripcion': descripcion
        }
        
        template = await template_controller.create_template(template_data, file)
        
        return UtilityService.success_response(
            data=template,
            message=f"Plantilla '{nombre}' subida exitosamente"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en upload_template: {e}")
        raise HTTPException(status_code=500, detail="Error al subir plantilla")


@router.get("/", response_model=dict)
async def get_templates(
    skip: int = Query(0, ge=0, description="Elementos a saltar"),
    limit: int = Query(100, le=100, description="Límite de resultados"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    solo_activas: bool = Query(True, description="Solo plantillas activas"),
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    📋 **Listar plantillas**
    
    **Filtros disponibles:**
    - categoria: contrato, demanda, escritura, etc.
    - solo_activas: true/false
    - paginación: skip y limit
    """
    try:
        if categoria:
            templates = template_controller.get_by_category(categoria)
        else:
            templates = template_controller.get_all_templates(
                skip=skip, 
                limit=limit, 
                solo_activas=solo_activas
            )
        
        # Obtener estadísticas
        stats = template_controller.get_statistics()
        
        return UtilityService.success_response(
            data={
                'templates': templates,
                'total': len(templates),
                'estadisticas': stats
            },
            message=f"Se encontraron {len(templates)} plantillas"
        )
    
    except Exception as e:
        print(f"Error en get_templates: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener plantillas")


@router.get("/{id_plantilla}", response_model=dict)
async def get_template(
    id_plantilla: int,
    template_controller: TemplateController = Depends(get_template_controller)
):
    """📄 **Obtener plantilla específica por ID**"""
    try:
        template = template_controller.get_template_by_id(id_plantilla)
        
        if not template:
            raise HTTPException(
                status_code=404, 
                detail=f"Plantilla con ID {id_plantilla} no encontrada"
            )
        
        return UtilityService.success_response(
            data=template,
            message="Plantilla obtenida exitosamente"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_template: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener plantilla")


@router.get("/{id_plantilla}/download")
async def download_template(
    id_plantilla: int,
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    📥 **Descargar archivo .docx de plantilla**
    
    Retorna el archivo físico para descarga en el navegador.
    """
    try:
        template = template_controller.get_template_by_id(id_plantilla)
        
        if not template:
            raise HTTPException(status_code=404, detail="Plantilla no encontrada")
        
        file_path = template['ruta_archivo']
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail="Archivo físico no encontrado en el servidor"
            )
        
        # Retornar archivo para descarga
        return FileResponse(
            path=file_path,
            filename=template['nombre_archivo'],
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={
                "Content-Disposition": f"attachment; filename={template['nombre_archivo']}"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en download_template: {e}")
        raise HTTPException(status_code=500, detail="Error al descargar plantilla")


@router.put("/{id_plantilla}", response_model=dict)
async def update_template(
    id_plantilla: int,
    template_data: TemplateUpdate,
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    ✏️ **Actualizar metadatos de plantilla**
    
    Permite actualizar: nombre, categoría, descripción, estado activo.
    **No** permite actualizar el archivo .docx (debe subir nueva plantilla).
    """
    try:
        # Filtrar campos None
        update_dict = {k: v for k, v in template_data.model_dump().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        updated_template = template_controller.update_template(id_plantilla, update_dict)
        
        if not updated_template:
            raise HTTPException(status_code=404, detail="Plantilla no encontrada")
        
        return UtilityService.success_response(
            data=updated_template,
            message="Plantilla actualizada exitosamente"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en update_template: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar plantilla")


@router.delete("/{id_plantilla}", response_model=dict)
async def delete_template(
    id_plantilla: int,
    hard_delete: bool = Query(False, description="true=eliminar permanente, false=desactivar"),
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    🗑️ **Eliminar plantilla**
    
    **Dos modos:**
    - `hard_delete=false` (default): Soft delete - solo marca como inactiva
    - `hard_delete=true`: Elimina permanentemente archivo + registro BD ⚠️
    """
    try:
        if hard_delete:
            # Eliminación permanente
            success = template_controller.hard_delete_template(id_plantilla)
            message = "Plantilla eliminada permanentemente"
        else:
            # Soft delete
            success = template_controller.soft_delete_template(id_plantilla)
            message = "Plantilla desactivada (soft delete)"
        
        if not success:
            raise HTTPException(status_code=404, detail="Plantilla no encontrada")
        
        return UtilityService.success_response(
            data={'id_plantilla': id_plantilla, 'deleted': True},
            message=message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en delete_template: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar plantilla")


@router.get("/stats/summary", response_model=dict)
async def get_statistics(
    template_controller: TemplateController = Depends(get_template_controller)
):
    """
    📊 **Obtener estadísticas de plantillas**
    
    Retorna:
    - Total de plantillas
    - Plantillas activas/inactivas
    - Distribución por categoría
    """
    try:
        stats = template_controller.get_statistics()
        
        return UtilityService.success_response(
            data=stats,
            message="Estadísticas obtenidas exitosamente"
        )
    
    except Exception as e:
        print(f"Error en get_statistics: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener estadísticas")