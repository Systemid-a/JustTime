# Archivo 45/46: app/controllers/analytics_controller.py
# Descripción: Controlador de analytics con lógica de análisis y reportes
# Funcionalidad: Análisis estadístico de proyectos, categorías, estados y contactos

from typing import Dict, Any, List, Optional
from sqlalchemy import func, case
from app.controllers.base_controller import BaseController
from app.models.proyecto import Proyecto
from app.models.categoria_proyecto import CategoriaProyecto
from app.models.contacto import Contacto
from app.models.tarea import Tarea


class AnalyticsController(BaseController):
    """
    Controlador de Analytics/Reportes
    Proporciona estadísticas y análisis de casos jurídicos
    """
    
    def get_casos_por_categoria(self) -> Dict[str, Any]:
        """
        Obtener cantidad de casos agrupados por categoría
        Incluye nombre y color de cada categoría
        """
        try:
            # Query con JOIN para obtener datos de categoría
            results = self.repository.db.query(
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
            print(f"Error en get_casos_por_categoria: {e}")
            return {
                "success": False,
                "data": [],
                "total": 0,
                "error": str(e)
            }
    
    def get_casos_por_estado(self) -> Dict[str, Any]:
        """
        Obtener cantidad de casos agrupados por estado
        Incluye porcentaje de cada estado
        """
        try:
            # Contar total de proyectos
            total_proyectos = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).scalar()
            
            if total_proyectos == 0:
                return {
                    "success": True,
                    "data": [],
                    "total": 0
                }
            
            # Contar por estado
            results = self.repository.db.query(
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
            print(f"Error en get_casos_por_estado: {e}")
            return {
                "success": False,
                "data": [],
                "total": 0,
                "error": str(e)
            }
    
    def get_casos_por_contacto(self, limit: int = 10) -> Dict[str, Any]:
        """
        Obtener top contactos con más casos
        Incluye casos activos y finalizados por contacto
        """
        try:
            # Subquery para contar casos activos
            casos_activos_sq = self.repository.db.query(
                Proyecto.contacto_id_fk,
                func.count(Proyecto.id_proyecto).label('activos')
            ).filter(
                Proyecto.estado == 'activo'
            ).group_by(
                Proyecto.contacto_id_fk
            ).subquery()
            
            # Subquery para contar casos finalizados
            casos_finalizados_sq = self.repository.db.query(
                Proyecto.contacto_id_fk,
                func.count(Proyecto.id_proyecto).label('finalizados')
            ).filter(
                Proyecto.estado == 'finalizado'
            ).group_by(
                Proyecto.contacto_id_fk
            ).subquery()
            
            # Query principal con JOINs
            results = self.repository.db.query(
                Contacto.id_contacto,
                Contacto.nombre,
                Contacto.tipo,
                func.count(Proyecto.id_proyecto).label('total_casos'),
                func.coalesce(casos_activos_sq.c.activos, 0).label('casos_activos'),
                func.coalesce(casos_finalizados_sq.c.finalizados, 0).label('casos_finalizados')
            ).join(
                Proyecto,
                Proyecto.contacto_id_fk == Contacto.id_contacto
            ).outerjoin(
                casos_activos_sq,
                casos_activos_sq.c.contacto_id_fk == Contacto.id_contacto
            ).outerjoin(
                casos_finalizados_sq,
                casos_finalizados_sq.c.contacto_id_fk == Contacto.id_contacto
            ).group_by(
                Contacto.id_contacto,
                Contacto.nombre,
                Contacto.tipo,
                casos_activos_sq.c.activos,
                casos_finalizados_sq.c.finalizados
            ).order_by(
                func.count(Proyecto.id_proyecto).desc()
            ).limit(limit).all()
            
            # Formatear datos
            data = []
            for result in results:
                item = {
                    "contacto_id": result.id_contacto,
                    "contacto_nombre": result.nombre,
                    "contacto_tipo": result.tipo,
                    "total_casos": result.total_casos,
                    "casos_activos": result.casos_activos,
                    "casos_finalizados": result.casos_finalizados
                }
                data.append(item)
            
            return {
                "success": True,
                "data": data,
                "total_contactos": len(data)
            }
            
        except Exception as e:
            print(f"Error en get_casos_por_contacto: {e}")
            return {
                "success": False,
                "data": [],
                "total_contactos": 0,
                "error": str(e)
            }
    
    def get_casos_por_contacto_especifico(self, contacto_id: int) -> Dict[str, Any]:
        """
        Obtener estadísticas de un contacto específico
        """
        try:
            # Verificar que el contacto existe
            contacto = self.repository.db.query(Contacto).filter(
                Contacto.id_contacto == contacto_id
            ).first()
            
            if not contacto:
                return {
                    "success": False,
                    "error": "Contacto no encontrado",
                    "data": None
                }
            
            # Contar casos por estado
            casos_activos = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(
                Proyecto.contacto_id_fk == contacto_id,
                Proyecto.estado == 'activo'
            ).scalar()
            
            casos_pausados = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(
                Proyecto.contacto_id_fk == contacto_id,
                Proyecto.estado == 'pausado'
            ).scalar()
            
            casos_finalizados = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(
                Proyecto.contacto_id_fk == contacto_id,
                Proyecto.estado == 'finalizado'
            ).scalar()
            
            total_casos = casos_activos + casos_pausados + casos_finalizados
            
            data = {
                "contacto_id": contacto.id_contacto,
                "contacto_nombre": contacto.nombre,
                "contacto_tipo": contacto.tipo,
                "total_casos": total_casos,
                "casos_activos": casos_activos,
                "casos_pausados": casos_pausados,
                "casos_finalizados": casos_finalizados
            }
            
            return {
                "success": True,
                "data": data
            }
            
        except Exception as e:
            print(f"Error en get_casos_por_contacto_especifico: {e}")
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }
    
    def get_resumen_completo(self) -> Dict[str, Any]:
        """
        Obtener resumen completo con todas las estadísticas
        Incluye proyectos, categorías, estados, contactos y tareas
        """
        try:
            # Estadísticas de proyectos
            total_proyectos = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).scalar()
            
            proyectos_activos = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(Proyecto.estado == 'activo').scalar()
            
            proyectos_pausados = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(Proyecto.estado == 'pausado').scalar()
            
            proyectos_finalizados = self.repository.db.query(
                func.count(Proyecto.id_proyecto)
            ).filter(Proyecto.estado == 'finalizado').scalar()
            
            # Estadísticas de tareas
            total_tareas = self.repository.db.query(
                func.count(Tarea.id_tarea)
            ).scalar()
            
            tareas_nuevas = self.repository.db.query(
                func.count(Tarea.id_tarea)
            ).filter(Tarea.estado == 'nuevo').scalar()
            
            tareas_en_progreso = self.repository.db.query(
                func.count(Tarea.id_tarea)
            ).filter(Tarea.estado == 'en_progreso').scalar()
            
            tareas_finalizadas = self.repository.db.query(
                func.count(Tarea.id_tarea)
            ).filter(Tarea.estado == 'finalizado').scalar()
            
            # Obtener datos de otros métodos
            casos_por_categoria = self.get_casos_por_categoria()
            casos_por_estado = self.get_casos_por_estado()
            top_contactos = self.get_casos_por_contacto(limit=10)
            
            return {
                "success": True,
                "data": {
                    # Resumen general
                    "total_proyectos": total_proyectos,
                    "proyectos_activos": proyectos_activos,
                    "proyectos_pausados": proyectos_pausados,
                    "proyectos_finalizados": proyectos_finalizados,
                    
                    # Casos por categoría
                    "casos_por_categoria": casos_por_categoria.get("data", []),
                    
                    # Casos por estado
                    "casos_por_estado": casos_por_estado.get("data", []),
                    
                    # Top contactos
                    "top_contactos": top_contactos.get("data", []),
                    
                    # Estadísticas de tareas
                    "total_tareas": total_tareas,
                    "tareas_nuevas": tareas_nuevas,
                    "tareas_en_progreso": tareas_en_progreso,
                    "tareas_finalizadas": tareas_finalizadas
                }
            }
            
        except Exception as e:
            print(f"Error en get_resumen_completo: {e}")
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }