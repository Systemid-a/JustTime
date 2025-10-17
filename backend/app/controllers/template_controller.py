# Archivo 45/43: app/controllers/template_controller.py - NUEVO
# Descripción: Controlador para gestión de plantillas de documentos
# Funcionalidad: Lógica de negocio para CRUD de plantillas .docx

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.controllers.base_controller import BaseController
from app.services.file_service import FileService
from fastapi import UploadFile, HTTPException
import os


class TemplateController(BaseController):
    """
    Controlador para gestión de plantillas de documentos Word.
    Hereda operaciones CRUD base y agrega lógica específica de plantillas.
    """
    
    def __init__(self, repository, file_service: FileService = None):
        super().__init__(repository)
        self.file_service = file_service or FileService()
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar datos específicos de plantillas.
        Implementa método abstracto de BaseController.
        """
        required_fields = ['nombre', 'nombre_archivo', 'ruta_archivo']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo '{field}' es obligatorio")
        
        # Validar categorías permitidas
        valid_categories = ['contrato', 'demanda', 'escritura', 'poder', 'memorial', 'dictamen', 'otro']
        if data.get('categoria') and data['categoria'] not in valid_categories:
            raise ValueError(f"Categoría debe ser una de: {', '.join(valid_categories)}")
        
        return data
    
    def validate_docx_file(self, file: UploadFile) -> bool:
        """
        Validar que el archivo sea .docx y cumpla restricciones.
        
        Args:
            file: Archivo subido por el usuario
            
        Returns:
            bool: True si válido
            
        Raises:
            HTTPException: Si el archivo no cumple validaciones
        """
        # Validar extensión
        if not file.filename.endswith('.docx'):
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten archivos .docx (Word)"
            )
        
        # Validar tamaño (5MB máximo)
        max_size = 5 * 1024 * 1024  # 5MB en bytes
        if hasattr(file.file, 'seek'):
            file.file.seek(0, 2)  # Ir al final
            file_size = file.file.tell()
            file.file.seek(0)  # Volver al inicio
            
            if file_size > max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"Archivo muy grande. Máximo: 5MB (actual: {file_size/1024/1024:.2f}MB)"
                )
        
        return True
    
    async def create_template(self, template_data: Dict[str, Any], file: UploadFile) -> Dict[str, Any]:
        """
        Crear nueva plantilla con archivo .docx.
        
        Args:
            template_data: Datos de la plantilla (nombre, categoria, descripcion)
            file: Archivo .docx a subir
            
        Returns:
            Dict con la plantilla creada
        """
        try:
            # Validar archivo
            self.validate_docx_file(file)
            
            # Guardar archivo físico
            file_info = await self.file_service.save_file(file)
            
            # Combinar datos
            complete_data = {
                **template_data,
                'nombre_archivo': file_info['nombre_archivo'],
                'ruta_archivo': file_info['ruta_archivo'],
                'activo': 1
            }
            
            # Validar y crear en BD
            validated_data = self.validate_data(complete_data)
            template = self.create(validated_data)
            
            return self._template_to_dict(template)
            
        except Exception as e:
            # Si falla, eliminar archivo subido
            if 'file_info' in locals():
                self.file_service.delete_file(file_info['ruta_archivo'])
            raise e
    
    def _template_to_dict(self, template) -> Dict[str, Any]:
        """Convertir objeto Plantilla a diccionario"""
        if template is None:
            return None
        
        return {
            'id_plantilla': template.id_plantilla,
            'nombre': template.nombre,
            'nombre_archivo': template.nombre_archivo,
            'ruta_archivo': template.ruta_archivo,
            'categoria': template.categoria,
            'descripcion': template.descripcion,
            'fecha_subida': template.fecha_subida.isoformat() if template.fecha_subida else None,
            'activo': bool(template.activo)
        }
    
    def get_all_templates(self, skip: int = 0, limit: int = 100, solo_activas: bool = True) -> List[Dict[str, Any]]:
        """Obtener todas las plantillas"""
        try:
            if solo_activas:
                templates = self.repository.db.query(self.repository.model).filter(
                    self.repository.model.activo == 1
                ).offset(skip).limit(limit).all()
            else:
                templates = self.repository.get_all(skip=skip, limit=limit)
            
            return [self._template_to_dict(t) for t in templates]
        except Exception as e:
            print(f"Error en get_all_templates: {e}")
            return []
    
    def get_by_category(self, categoria: str) -> List[Dict[str, Any]]:
        """Obtener plantillas por categoría"""
        try:
            templates = self.repository.db.query(self.repository.model).filter(
                self.repository.model.categoria == categoria,
                self.repository.model.activo == 1
            ).all()
            return [self._template_to_dict(t) for t in templates]
        except Exception as e:
            print(f"Error en get_by_category: {e}")
            return []
    
    def get_template_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        """Obtener plantilla por ID"""
        try:
            template = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_plantilla == template_id
            ).first()
            return self._template_to_dict(template)
        except Exception as e:
            print(f"Error en get_template_by_id: {e}")
            return None
    
    def update_template(self, template_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar metadatos de plantilla (no el archivo)"""
        try:
            template = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_plantilla == template_id
            ).first()
            
            if not template:
                return None
            
            # Actualizar solo campos permitidos
            allowed_fields = ['nombre', 'categoria', 'descripcion', 'activo']
            for key, value in update_data.items():
                if key in allowed_fields and value is not None:
                    setattr(template, key, value)
            
            self.repository.db.commit()
            self.repository.db.refresh(template)
            
            return self._template_to_dict(template)
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en update_template: {e}")
            return None
    
    def soft_delete_template(self, template_id: int) -> bool:
        """Eliminar plantilla (soft delete - marca como inactiva)"""
        try:
            template = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_plantilla == template_id
            ).first()
            
            if template:
                template.activo = 0
                self.repository.db.commit()
                return True
            return False
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en soft_delete_template: {e}")
            return False
    
    def hard_delete_template(self, template_id: int) -> bool:
        """
        Eliminar plantilla permanentemente (archivo + registro BD).
        ⚠️ CUIDADO: Esta operación es irreversible.
        """
        try:
            template = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_plantilla == template_id
            ).first()
            
            if template:
                # Eliminar archivo físico
                if os.path.exists(template.ruta_archivo):
                    os.remove(template.ruta_archivo)
                
                # Eliminar registro de BD
                self.repository.db.delete(template)
                self.repository.db.commit()
                return True
            return False
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en hard_delete_template: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de plantillas"""
        try:
            total = self.repository.db.query(self.repository.model).count()
            activas = self.repository.db.query(self.repository.model).filter(
                self.repository.model.activo == 1
            ).count()
            
            # Contar por categoría
            categorias = self.repository.db.query(
                self.repository.model.categoria
            ).filter(
                self.repository.model.activo == 1
            ).all()
            
            por_categoria = {}
            for (cat,) in categorias:
                if cat:
                    por_categoria[cat] = por_categoria.get(cat, 0) + 1
            
            return {
                'total': total,
                'activas': activas,
                'inactivas': total - activas,
                'por_categoria': por_categoria
            }
        except Exception as e:
            print(f"Error en get_statistics: {e}")
            return {'total': 0, 'activas': 0, 'inactivas': 0, 'por_categoria': {}}