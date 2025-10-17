# Archivo 40/43: app/routers/contact_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.factory import RepositoryFactory
from app.controllers.contact_controller import ContactController
from app.schemas.contact_schema import ContactCreate, ContactUpdate, ContactResponse
from app.services.utility_service import UtilityService

router = APIRouter()


def get_contact_controller(db: Session = Depends(get_db)) -> ContactController:
    """Dependency para obtener controlador de contactos"""
    contact_repo = RepositoryFactory.create_contact_repository(db)
    return ContactController(contact_repo)


@router.get("/", response_model=dict)
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    tipo: Optional[str] = Query(None, regex="^(persona|empresa)$"),
    contact_controller: ContactController = Depends(get_contact_controller)
):
    """Obtener lista de contactos con filtros opcionales"""
    try:
        if tipo:
            contacts = contact_controller.get_by_type(tipo)
        else:
            contacts = contact_controller.get_all_contacts(skip=skip, limit=limit)
        
        return UtilityService.success_response(
            data=contacts,
            message=f"Se encontraron {len(contacts)} contactos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener contactos")


@router.get("/{id_contacto}", response_model=dict)
async def get_contact(
    id_contacto: int,
    contact_controller: ContactController = Depends(get_contact_controller)
):
    """Obtener contacto específico por ID"""
    try:
        contact = contact_controller.get_contact_by_id(id_contacto)
        if not contact:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        return UtilityService.success_response(
            data=contact,
            message="Contacto obtenido exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener contacto")


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: ContactCreate,
    contact_controller: ContactController = Depends(get_contact_controller)
):
    """Crear nuevo contacto"""
    try:
        contact = contact_controller.create(contact_data.model_dump())
        return UtilityService.success_response(
            data=contact,
            message="Contacto creado exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear contacto")


@router.put("/{id_contacto}", response_model=dict)
async def update_contact(
    id_contacto: int,
    contact_data: ContactUpdate,
    contact_controller: ContactController = Depends(get_contact_controller)
):
    """Actualizar contacto existente"""
    try:
        # Filtrar datos None
        update_data = {k: v for k, v in contact_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        contact = contact_controller.update_contact(id_contacto, update_data)
        if not contact:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        return UtilityService.success_response(
            data=contact,
            message="Contacto actualizado exitosamente"
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar contacto")


@router.delete("/{id_contacto}", response_model=dict)
async def delete_contact(
    id_contacto: int,
    contact_controller: ContactController = Depends(get_contact_controller)
):
    """Eliminar contacto"""
    try:
        success = contact_controller.delete(id_contacto)
        if not success:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        return UtilityService.success_response(
            message="Contacto eliminado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar contacto")