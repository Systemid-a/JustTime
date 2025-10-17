# Archivo 46/46: app/routers/analytics_routes.py
# Descripción: Rutas API para módulo de análisis y reportes
# Funcionalidad: Endpoints REST para estadísticas de proyectos, categorías, estados y contactos

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.models.proyecto import Proyecto
from app.models.categoria_proyecto import CategoriaProyecto
from app.models.contacto import Contacto
from app.models.tarea import Tarea
from app.routers.auth_routes import get_current_user


# Crear router
router = APIRouter()


@router.get(
    "/casos-por-categoria",
    summary="Obtener casos por categoría",
    description="Retorna la cantidad de casos agrupados por categoría jurídica"
)
async def get_casos_por_categoria(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener casos por categoría"""
    try:
        # Query con JOIN para obtener datos de categoría
        results = db.query(
            CategoriaProyecto.id_categoria_proyecto,
            CategoriaProyecto.nombre,
            CategoriaProyecto.color,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).outerjoin(
            Proyecto, 
            Proyecto.categoria_id_fk == CategoriaProyecto.id_categoria_proyecto
        ).group_by(
            CategoriaProyecto.id_categoria_proyecto,
            CategoriaProyecto.nombre,
            CategoriaProyecto.color
        ).all()
        
        # Formatear datos
        data = []
        total_casos = 0
        
        for result in results:
            item = {
                "categoria_id": result.id_categoria_proyecto,
                "categoria_nombre": result.nombre,
                "categoria_color": result.color,
                "total_casos": result.total_casos
            }
            data.append(item)
            total_casos += result.total_casos
        
        return {
            "success": True,
            "data": data,
            "total": total_casos
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener casos por categoría: {str(e)}"
        )


@router.get(
    "/casos-por-estado",
    summary="Obtener casos por estado",
    description="Retorna la cantidad de casos agrupados por estado"
)
async def get_casos_por_estado(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener casos por estado"""
    try:
        # Contar total de proyectos
        total_proyectos = db.query(func.count(Proyecto.id_proyecto)).scalar()
        
        if total_proyectos == 0:
            return {
                "success": True,
                "data": [],
                "total": 0
            }
        
        # Contar por estado
        results = db.query(
            Proyecto.estado,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).group_by(
            Proyecto.estado
        ).all()
        
        # Formatear datos con porcentajes
        data = []
        for result in results:
            porcentaje = round((result.total_casos / total_proyectos) * 100, 2)
            item = {
                "estado": result.estado,
                "total_casos": result.total_casos,
                "porcentaje": porcentaje
            }
            data.append(item)
        
        return {
            "success": True,
            "data": data,
            "total": total_proyectos
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener casos por estado: {str(e)}"
        )


@router.get(
    "/casos-por-contacto",
    summary="Obtener top contactos con más casos",
    description="Retorna los contactos con más casos registrados"
)
async def get_casos_por_contacto(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener top contactos con más casos"""
    try:
        # Query principal
        results = db.query(
            Contacto.id_contacto,
            Contacto.nombre,
            Contacto.tipo,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).join(
            Proyecto,
            Proyecto.contacto_id_fk == Contacto.id_contacto
        ).group_by(
            Contacto.id_contacto,
            Contacto.nombre,
            Contacto.tipo
        ).order_by(
            func.count(Proyecto.id_proyecto).desc()
        ).limit(limit).all()
        
        # Formatear datos y obtener desglose por estado
        data = []
        for contacto in results:
            # Contar casos activos
            casos_activos = db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(
                Proyecto.contacto_id_fk == contacto.id_contacto,
                Proyecto.estado == 'activo'
            ).scalar()
            
            # Contar casos finalizados
            casos_finalizados = db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(
                Proyecto.contacto_id_fk == contacto.id_contacto,
                Proyecto.estado == 'finalizado'
            ).scalar()
            
            item = {
                "contacto_id": contacto.id_contacto,
                "contacto_nombre": contacto.nombre,
                "contacto_tipo": contacto.tipo,
                "total_casos": contacto.total_casos,
                "casos_activos": casos_activos or 0,
                "casos_finalizados": casos_finalizados or 0
            }
            data.append(item)
        
        return {
            "success": True,
            "data": data,
            "total_contactos": len(data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener casos por contacto: {str(e)}"
        )


@router.get(
    "/casos-contacto/{contacto_id}",
    summary="Obtener estadísticas de un contacto específico"
)
async def get_casos_contacto_especifico(
    contacto_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de un contacto específico"""
    try:
        # Verificar que el contacto existe
        contacto = db.query(Contacto).filter(
            Contacto.id_contacto == contacto_id
        ).first()
        
        if not contacto:
            raise HTTPException(
                status_code=404,
                detail="Contacto no encontrado"
            )
        
        # Contar casos por estado
        casos_activos = db.query(
            func.count(Proyecto.id_proyecto)
        ).filter(
            Proyecto.contacto_id_fk == contacto_id,
            Proyecto.estado == 'activo'
        ).scalar()
        
        casos_pausados = db.query(
            func.count(Proyecto.id_proyecto)
        ).filter(
            Proyecto.contacto_id_fk == contacto_id,
            Proyecto.estado == 'pausado'
        ).scalar()
        
        casos_finalizados = db.query(
            func.count(Proyecto.id_proyecto)
        ).filter(
            Proyecto.contacto_id_fk == contacto_id,
            Proyecto.estado == 'finalizado'
        ).scalar()
        
        total_casos = (casos_activos or 0) + (casos_pausados or 0) + (casos_finalizados or 0)
        
        return {
            "success": True,
            "data": {
                "contacto_id": contacto.id_contacto,
                "contacto_nombre": contacto.nombre,
                "contacto_tipo": contacto.tipo,
                "total_casos": total_casos,
                "casos_activos": casos_activos or 0,
                "casos_pausados": casos_pausados or 0,
                "casos_finalizados": casos_finalizados or 0
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener datos del contacto: {str(e)}"
        )


@router.get(
    "/resumen-completo",
    summary="Obtener resumen completo de analytics"
)
async def get_resumen_completo(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener resumen completo con todas las estadísticas"""
    try:
        # Estadísticas de proyectos
        total_proyectos = db.query(func.count(Proyecto.id_proyecto)).scalar() or 0
        
        proyectos_activos = db.query(func.count(Proyecto.id_proyecto)).filter(
            Proyecto.estado == 'activo'
        ).scalar() or 0
        
        proyectos_pausados = db.query(func.count(Proyecto.id_proyecto)).filter(
            Proyecto.estado == 'pausado'
        ).scalar() or 0
        
        proyectos_finalizados = db.query(func.count(Proyecto.id_proyecto)).filter(
            Proyecto.estado == 'finalizado'
        ).scalar() or 0
        
        # Casos por categoría
        results_categoria = db.query(
            CategoriaProyecto.id_categoria_proyecto,
            CategoriaProyecto.nombre,
            CategoriaProyecto.color,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).outerjoin(
            Proyecto,
            Proyecto.categoria_id_fk == CategoriaProyecto.id_categoria_proyecto
        ).group_by(
            CategoriaProyecto.id_categoria_proyecto,
            CategoriaProyecto.nombre,
            CategoriaProyecto.color
        ).all()
        
        casos_por_categoria = [
            {
                "categoria_id": r.id_categoria_proyecto,
                "categoria_nombre": r.nombre,
                "categoria_color": r.color,
                "total_casos": r.total_casos
            }
            for r in results_categoria
        ]
        
        # Casos por estado
        results_estado = db.query(
            Proyecto.estado,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).group_by(Proyecto.estado).all()
        
        casos_por_estado = []
        for r in results_estado:
            porcentaje = round((r.total_casos / total_proyectos * 100) if total_proyectos > 0 else 0, 2)
            casos_por_estado.append({
                "estado": r.estado,
                "total_casos": r.total_casos,
                "porcentaje": porcentaje
            })
        
        # Top contactos
        results_contactos = db.query(
            Contacto.id_contacto,
            Contacto.nombre,
            Contacto.tipo,
            func.count(Proyecto.id_proyecto).label('total_casos')
        ).join(
            Proyecto,
            Proyecto.contacto_id_fk == Contacto.id_contacto
        ).group_by(
            Contacto.id_contacto,
            Contacto.nombre,
            Contacto.tipo
        ).order_by(
            func.count(Proyecto.id_proyecto).desc()
        ).limit(10).all()
        
        top_contactos = []
        for c in results_contactos:
            activos = db.query(func.count(Proyecto.id_proyecto)).filter(
                Proyecto.contacto_id_fk == c.id_contacto,
                Proyecto.estado == 'activo'
            ).scalar() or 0
            
            finalizados = db.query(func.count(Proyecto.id_proyecto)).filter(
                Proyecto.contacto_id_fk == c.id_contacto,
                Proyecto.estado == 'finalizado'
            ).scalar() or 0
            
            top_contactos.append({
                "contacto_id": c.id_contacto,
                "contacto_nombre": c.nombre,
                "contacto_tipo": c.tipo,
                "total_casos": c.total_casos,
                "casos_activos": activos,
                "casos_finalizados": finalizados
            })
        
        # Estadísticas de tareas
        total_tareas = db.query(func.count(Tarea.id_tarea)).scalar() or 0
        
        tareas_nuevas = db.query(func.count(Tarea.id_tarea)).filter(
            Tarea.estado == 'nuevo'
        ).scalar() or 0
        
        tareas_en_progreso = db.query(func.count(Tarea.id_tarea)).filter(
            Tarea.estado == 'en_progreso'
        ).scalar() or 0
        
        tareas_finalizadas = db.query(func.count(Tarea.id_tarea)).filter(
            Tarea.estado == 'finalizado'
        ).scalar() or 0
        
        return {
            "success": True,
            "data": {
                "total_proyectos": total_proyectos,
                "proyectos_activos": proyectos_activos,
                "proyectos_pausados": proyectos_pausados,
                "proyectos_finalizados": proyectos_finalizados,
                "casos_por_categoria": casos_por_categoria,
                "casos_por_estado": casos_por_estado,
                "top_contactos": top_contactos,
                "total_tareas": total_tareas,
                "tareas_nuevas": tareas_nuevas,
                "tareas_en_progreso": tareas_en_progreso,
                "tareas_finalizadas": tareas_finalizadas
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener resumen completo: {str(e)}"
        )




























