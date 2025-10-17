# Archivo 44/46: app/schemas/analytics_schema.py
# Descripción: Schemas Pydantic para validación de analytics/reportes
# Funcionalidad: Validación de datos para módulo de análisis y reportes

from pydantic import Field
from typing import Optional, List
from app.schemas.base_schema import BaseSchema


class CasosPorCategoriaItem(BaseSchema):
    """Schema para un item de casos por categoría"""
    categoria_id: int = Field(..., description="ID de la categoría")
    categoria_nombre: str = Field(..., description="Nombre de la categoría")
    categoria_color: str = Field(..., description="Color hexadecimal de la categoría")
    total_casos: int = Field(..., description="Cantidad total de casos")


class CasosPorCategoriaResponse(BaseSchema):
    """Schema para respuesta de casos por categoría"""
    data: List[CasosPorCategoriaItem]
    total: int = Field(..., description="Total de casos en todas las categorías")


class CasosPorEstadoItem(BaseSchema):
    """Schema para un item de casos por estado"""
    estado: str = Field(..., description="Estado del proyecto (activo/pausado/finalizado)")
    total_casos: int = Field(..., description="Cantidad de casos en este estado")
    porcentaje: float = Field(..., description="Porcentaje respecto al total")


class CasosPorEstadoResponse(BaseSchema):
    """Schema para respuesta de casos por estado"""
    data: List[CasosPorEstadoItem]
    total: int = Field(..., description="Total de casos")


class CasosPorContactoItem(BaseSchema):
    """Schema para un item de casos por contacto"""
    contacto_id: int = Field(..., description="ID del contacto")
    contacto_nombre: str = Field(..., description="Nombre del contacto")
    contacto_tipo: str = Field(..., description="Tipo de contacto (persona/empresa)")
    total_casos: int = Field(..., description="Cantidad total de casos del contacto")
    casos_activos: int = Field(..., description="Casos activos del contacto")
    casos_finalizados: int = Field(..., description="Casos finalizados del contacto")


class CasosPorContactoResponse(BaseSchema):
    """Schema para respuesta de casos por contacto"""
    data: List[CasosPorContactoItem]
    total_contactos: int = Field(..., description="Total de contactos con casos")


class ResumenCompletoResponse(BaseSchema):
    """Schema para respuesta completa con todas las estadísticas"""
    # Resumen general
    total_proyectos: int
    proyectos_activos: int
    proyectos_pausados: int
    proyectos_finalizados: int
    
    # Casos por categoría
    casos_por_categoria: List[CasosPorCategoriaItem]
    
    # Casos por estado
    casos_por_estado: List[CasosPorEstadoItem]
    
    # Top contactos (top 10)
    top_contactos: List[CasosPorContactoItem]
    
    # Estadísticas de tareas
    total_tareas: int
    tareas_nuevas: int
    tareas_en_progreso: int
    tareas_finalizadas: int


class FiltroAnalyticsRequest(BaseSchema):
    """Schema para filtros de analytics"""
    contacto_id: Optional[int] = Field(None, description="Filtrar por contacto específico")
    categoria_id: Optional[int] = Field(None, description="Filtrar por categoría específica")
    estado: Optional[str] = Field(None, description="Filtrar por estado (activo/pausado/finalizado)")
    fecha_desde: Optional[str] = Field(None, description="Fecha inicio formato YYYY-MM-DD")
    fecha_hasta: Optional[str] = Field(None, description="Fecha fin formato YYYY-MM-DD")