# Archivo: app/routers/document_routes.py
# Descripción: Rutas API para gestión de documentos
# Endpoints: Upload, List, Download, Update, Delete, Search

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os

from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.document_controller import DocumentController
from app.schemas.document_schema import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListResponse,
    DocumentUploadResponse
)
from app.services.utility_service import UtilityService
from app.services.file_service import FileService


router = APIRouter()


def get_document_controller(db: Session = Depends(get_db)) -> DocumentController:
    """Dependency para obtener controlador de documentos"""
    from app.models.documento import Documento
    document_repo = RepositoryFactory.create_repository(Documento, db)
    file_service = FileService()
    return DocumentController(document_repo, file_service)


# ============================================================================
# ENDPOINTS DE DOCUMENTOS
# ============================================================================

@router.post("/upload", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(..., description="Archivo a subir (PDF, DOCX, JPG, etc.)"),
    proyecto_id: Optional[int] = Form(None, description="ID del proyecto (opcional)"),
    subido_por: Optional[int] = Form(None, description="ID del usuario que sube"),
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📤 **Subir nuevo documento**
    
    **Tipos de archivo soportados:**
    - Documentos: PDF, DOC, DOCX
    - Imágenes: JPG, JPEG, PNG, GIF, WEBP
    - Hojas de cálculo: XLS, XLSX, CSV
    - Texto: TXT, RTF
    - Archivos: ZIP, RAR
    
    **Tamaños máximos:**
    - Documentos: 10MB
    - Imágenes: 5MB
    - Hojas de cálculo: 15MB
    - Texto: 2MB
    - Archivos comprimidos: 50MB
    """
    try:
        document_data = {
            'proyecto_id_fk': proyecto_id,
            'subido_por_fk': subido_por
        }
        
        document = await document_controller.create_document(document_data, file)
        
        return UtilityService.success_response(
            data=document,
            message=f"Documento '{file.filename}' subido exitosamente"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en upload_document: {e}")
        raise HTTPException(status_code=500, detail="Error al subir documento")


@router.get("/", response_model=dict)
async def get_documents(
    skip: int = Query(0, ge=0, description="Elementos a saltar"),
    limit: int = Query(100, le=100, description="Límite de resultados"),
    proyecto_id: Optional[int] = Query(None, description="Filtrar por proyecto"),
    tipo_archivo: Optional[str] = Query(None, description="Filtrar por tipo (.pdf, .docx, etc.)"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📋 **Listar documentos**
    
    **Filtros disponibles:**
    - proyecto_id: Documentos de un proyecto específico
    - tipo_archivo: Por extensión (.pdf, .docx, .jpg, etc.)
    - usuario_id: Documentos subidos por un usuario
    - Paginación: skip y limit
    """
    try:
        documents = document_controller.get_all_documents(
            skip=skip,
            limit=limit,
            proyecto_id=proyecto_id,
            tipo_archivo=tipo_archivo,
            usuario_id=usuario_id
        )
        
        # Obtener estadísticas
        stats = document_controller.get_statistics()
        
        return UtilityService.success_response(
            data={
                'documentos': documents,
                'total': len(documents),
                'estadisticas': stats
            },
            message=f"Se encontraron {len(documents)} documentos"
        )
    
    except Exception as e:
        print(f"Error en get_documents: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener documentos")


@router.get("/search", response_model=dict)
async def search_documents(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    🔍 **Buscar documentos por nombre**
    
    Busca documentos que contengan el término en su nombre de archivo.
    """
    try:
        documents = document_controller.search_documents(q)
        
        return UtilityService.success_response(
            data={
                'documentos': documents,
                'total': len(documents),
                'termino_busqueda': q
            },
            message=f"Se encontraron {len(documents)} documentos"
        )
    
    except Exception as e:
        print(f"Error en search_documents: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar documentos")


@router.get("/proyecto/{proyecto_id}", response_model=dict)
async def get_documents_by_project(
    proyecto_id: int,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📁 **Obtener documentos de un proyecto específico**
    
    Retorna todos los documentos vinculados a un proyecto.
    """
    try:
        documents = document_controller.get_by_project(proyecto_id)
        
        return UtilityService.success_response(
            data={
                'documentos': documents,
                'total': len(documents),
                'proyecto_id': proyecto_id
            },
            message=f"Proyecto tiene {len(documents)} documentos"
        )
    
    except Exception as e:
        print(f"Error en get_documents_by_project: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener documentos del proyecto")


@router.get("/tipo/{tipo_archivo}", response_model=dict)
async def get_documents_by_type(
    tipo_archivo: str,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📑 **Obtener documentos por tipo de archivo**
    
    Ejemplos: pdf, docx, jpg, png, xlsx
    """
    try:
        documents = document_controller.get_by_type(tipo_archivo)
        
        return UtilityService.success_response(
            data={
                'documentos': documents,
                'total': len(documents),
                'tipo': tipo_archivo
            },
            message=f"Se encontraron {len(documents)} archivos .{tipo_archivo}"
        )
    
    except Exception as e:
        print(f"Error en get_documents_by_type: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener documentos por tipo")


@router.get("/{id_documento}", response_model=dict)
async def get_document(
    id_documento: int,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """📄 **Obtener documento específico por ID**"""
    try:
        document = document_controller.get_document_by_id(id_documento)
        
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Documento con ID {id_documento} no encontrado"
            )
        
        return UtilityService.success_response(
            data=document,
            message="Documento obtenido exitosamente"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_document: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener documento")


@router.get("/{id_documento}/download")
async def download_document(
    id_documento: int,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📥 **Descargar archivo del documento**
    
    Retorna el archivo físico para descarga en el navegador.
    """
    try:
        document = document_controller.get_document_by_id(id_documento)
        
        if not document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        file_path = document['ruta_archivo']
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Archivo físico no encontrado en el servidor"
            )
        
        # Determinar media type según extensión
        file_ext = document['tipo_archivo'] or ''
        media_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed'
        }
        
        media_type = media_types.get(file_ext, 'application/octet-stream')
        
        # Retornar archivo para descarga
        return FileResponse(
            path=file_path,
            filename=document['nombre_archivo'],
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={document['nombre_archivo']}"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en download_document: {e}")
        raise HTTPException(status_code=500, detail="Error al descargar documento")


@router.put("/{id_documento}", response_model=dict)
async def update_document(
    id_documento: int,
    document_data: DocumentUpdate,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    ✏️ **Actualizar metadatos de documento**
    
    Permite actualizar: nombre_archivo, tipo_archivo, proyecto_id_fk.
    **No** permite actualizar el archivo físico (debe subir nuevo documento).
    """
    try:
        # Filtrar campos None
        update_dict = {k: v for k, v in document_data.model_dump().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        updated_document = document_controller.update_document(id_documento, update_dict)
        
        if not updated_document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        return UtilityService.success_response(
            data=updated_document,
            message="Documento actualizado exitosamente"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en update_document: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar documento")


@router.delete("/{id_documento}", response_model=dict)
async def delete_document(
    id_documento: int,
    delete_file: bool = Query(True, description="true=eliminar archivo físico, false=solo BD"),
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    🗑️ **Eliminar documento**
    
    **Opciones:**
    - `delete_file=true` (default): Elimina archivo físico + registro BD
    - `delete_file=false`: Solo elimina registro BD, mantiene archivo
    """
    try:
        success = document_controller.delete_document(id_documento, delete_file)
        
        if not success:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        message = "Documento y archivo eliminados" if delete_file else "Documento eliminado (archivo conservado)"
        
        return UtilityService.success_response(
            data={'id_documento': id_documento, 'deleted': True, 'file_deleted': delete_file},
            message=message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en delete_document: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar documento")


@router.get("/stats/summary", response_model=dict)
async def get_statistics(
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    📊 **Obtener estadísticas de documentos**
    
    Retorna:
    - Total de documentos
    - Documentos con/sin proyecto
    - Distribución por tipo de archivo
    """
    try:
        stats = document_controller.get_statistics()
        
        return UtilityService.success_response(
            data=stats,
            message="Estadísticas obtenidas exitosamente"
        )
    
    except Exception as e:
        print(f"Error en get_statistics: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener estadísticas")