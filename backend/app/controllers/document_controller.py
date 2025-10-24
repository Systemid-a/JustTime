# Archivo: app/controllers/document_controller.py
# Descripción: Controlador para gestión de documentos
# Funcionalidad: Lógica de negocio para CRUD de documentos con manejo de archivos

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.controllers.base_controller import BaseController
from app.services.file_service import FileService
from fastapi import UploadFile, HTTPException
import os
from datetime import datetime


class DocumentController(BaseController):
    """
    Controlador para gestión de documentos.
    Hereda operaciones CRUD base y agrega lógica específica de documentos.
    
    DIFERENCIA CON PLANTILLAS:
    - Soporta múltiples tipos de archivos (PDF, DOCX, JPG, PNG, etc.)
    - Vinculado obligatoriamente o opcionalmente a proyectos
    - Sistema de categorización por tipo de archivo
    """
    
    # Tipos de archivo permitidos (extensiones)
    ALLOWED_EXTENSIONS = [
        '.pdf', '.doc', '.docx',  # Documentos
        '.jpg', '.jpeg', '.png', '.gif', '.webp',  # Imágenes
        '.xls', '.xlsx', '.csv',  # Hojas de cálculo
        '.txt', '.rtf',  # Texto plano
        '.zip', '.rar'  # Archivos comprimidos
    ]
    
    # Tamaño máximo por tipo (en MB)
    MAX_FILE_SIZES = {
        'document': 10,  # 10MB para documentos
        'image': 5,      # 5MB para imágenes
        'spreadsheet': 15,  # 15MB para hojas de cálculo
        'text': 2,       # 2MB para texto plano
        'archive': 50    # 50MB para archivos comprimidos
    }
    
    def __init__(self, repository, file_service: FileService = None):
        super().__init__(repository)
        self.file_service = file_service or FileService()
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar datos específicos de documentos.
        Implementa método abstracto de BaseController.
        """
        required_fields = ['nombre_archivo', 'ruta_archivo']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo '{field}' es obligatorio")
        
        # Validar tipo de archivo si se proporciona
        if data.get('tipo_archivo'):
            ext = data['tipo_archivo'].lower()
            if not ext.startswith('.'):
                ext = f'.{ext}'
            
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Tipo de archivo '{ext}' no permitido. "
                    f"Tipos permitidos: {', '.join(self.ALLOWED_EXTENSIONS)}"
                )
        
        return data
    
    def _get_file_category(self, extension: str) -> str:
        """Determinar categoría del archivo según su extensión"""
        extension = extension.lower()
        
        if extension in ['.pdf', '.doc', '.docx']:
            return 'document'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return 'image'
        elif extension in ['.xls', '.xlsx', '.csv']:
            return 'spreadsheet'
        elif extension in ['.txt', '.rtf']:
            return 'text'
        elif extension in ['.zip', '.rar']:
            return 'archive'
        else:
            return 'other'
    
    def validate_file(self, file: UploadFile) -> bool:
        """
        Validar que el archivo cumpla con restricciones.
        
        Args:
            file: Archivo subido por el usuario
            
        Returns:
            bool: True si válido
            
        Raises:
            HTTPException: Si el archivo no cumple validaciones
        """
        # Obtener extensión del archivo
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Validar extensión
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo '{file_ext}' no permitido. "
                       f"Tipos permitidos: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        
        # Determinar categoría y tamaño máximo permitido
        category = self._get_file_category(file_ext)
        max_size_mb = self.MAX_FILE_SIZES.get(category, 10)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Validar tamaño
        if hasattr(file.file, 'seek'):
            file.file.seek(0, 2)  # Ir al final
            file_size = file.file.tell()
            file.file.seek(0)  # Volver al inicio
            
            if file_size > max_size_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Archivo muy grande. Máximo para {category}: "
                           f"{max_size_mb}MB (actual: {file_size/1024/1024:.2f}MB)"
                )
        
        return True
    
    async def create_document(
        self, 
        document_data: Dict[str, Any], 
        file: UploadFile
    ) -> Dict[str, Any]:
        """
        Crear nuevo documento con archivo.
        
        Args:
            document_data: Datos del documento (proyecto_id_fk, subido_por_fk)
            file: Archivo a subir
            
        Returns:
            Dict con el documento creado
        """
        try:
            # Validar archivo
            self.validate_file(file)
            
            # Guardar archivo físico
            file_info = await self.file_service.save_file(file)
            
            # Determinar tipo de archivo
            file_ext = os.path.splitext(file.filename)[1].lower()
            
            # Combinar datos
            complete_data = {
                **document_data,
                'nombre_archivo': file_info['nombre_archivo'],
                'ruta_archivo': file_info['ruta_archivo'],
                'tipo_archivo': file_ext
            }
            
            # Validar y crear en BD
            validated_data = self.validate_data(complete_data)
            document = self.create(validated_data)
            
            return self._document_to_dict(document)
            
        except Exception as e:
            # Si falla, eliminar archivo subido
            if 'file_info' in locals():
                self.file_service.delete_file(file_info['ruta_archivo'])
            raise e
    
    def _document_to_dict(self, document) -> Dict[str, Any]:
        """Convertir objeto Documento a diccionario"""
        if document is None:
            return None
        
        return {
            'id_documento': document.id_documento,
            'nombre_archivo': document.nombre_archivo,
            'ruta_archivo': document.ruta_archivo,
            'tipo_archivo': document.tipo_archivo,
            'proyecto_id_fk': document.proyecto_id_fk,
            'subido_por_fk': document.subido_por_fk,
            'fecha_subida': document.fecha_subida.isoformat() if document.fecha_subida else None
        }
    
    def get_all_documents(
        self, 
        skip: int = 0, 
        limit: int = 100,
        proyecto_id: Optional[int] = None,
        tipo_archivo: Optional[str] = None,
        usuario_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtener todos los documentos con filtros opcionales"""
        try:
            query = self.repository.db.query(self.repository.model)
            
            # Aplicar filtros
            if proyecto_id:
                query = query.filter(self.repository.model.proyecto_id_fk == proyecto_id)
            
            if tipo_archivo:
                if not tipo_archivo.startswith('.'):
                    tipo_archivo = f'.{tipo_archivo}'
                query = query.filter(self.repository.model.tipo_archivo == tipo_archivo.lower())
            
            if usuario_id:
                query = query.filter(self.repository.model.subido_por_fk == usuario_id)
            
            # Ordenar por fecha (más recientes primero)
            query = query.order_by(self.repository.model.fecha_subida.desc())
            
            documents = query.offset(skip).limit(limit).all()
            return [self._document_to_dict(d) for d in documents]
            
        except Exception as e:
            print(f"Error en get_all_documents: {e}")
            return []
    
    def get_document_by_id(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Obtener documento por ID"""
        try:
            document = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_documento == document_id
            ).first()
            return self._document_to_dict(document)
        except Exception as e:
            print(f"Error en get_document_by_id: {e}")
            return None
    
    def get_by_project(self, proyecto_id: int) -> List[Dict[str, Any]]:
        """Obtener documentos de un proyecto específico"""
        try:
            documents = self.repository.db.query(self.repository.model).filter(
                self.repository.model.proyecto_id_fk == proyecto_id
            ).order_by(self.repository.model.fecha_subida.desc()).all()
            return [self._document_to_dict(d) for d in documents]
        except Exception as e:
            print(f"Error en get_by_project: {e}")
            return []
    
    def get_by_type(self, tipo_archivo: str) -> List[Dict[str, Any]]:
        """Obtener documentos por tipo de archivo"""
        try:
            if not tipo_archivo.startswith('.'):
                tipo_archivo = f'.{tipo_archivo}'
            
            documents = self.repository.db.query(self.repository.model).filter(
                self.repository.model.tipo_archivo == tipo_archivo.lower()
            ).order_by(self.repository.model.fecha_subida.desc()).all()
            return [self._document_to_dict(d) for d in documents]
        except Exception as e:
            print(f"Error en get_by_type: {e}")
            return []
    
    def update_document(
        self, 
        document_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Actualizar metadatos de documento (no el archivo)"""
        try:
            document = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_documento == document_id
            ).first()
            
            if not document:
                return None
            
            # Actualizar solo campos permitidos
            allowed_fields = ['nombre_archivo', 'tipo_archivo', 'proyecto_id_fk']
            for key, value in update_data.items():
                if key in allowed_fields and value is not None:
                    setattr(document, key, value)
            
            self.repository.db.commit()
            self.repository.db.refresh(document)
            
            return self._document_to_dict(document)
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en update_document: {e}")
            return None
    
    def delete_document(self, document_id: int, delete_file: bool = True) -> bool:
        """
        Eliminar documento permanentemente.
        
        Args:
            document_id: ID del documento
            delete_file: Si True, elimina también el archivo físico
        """
        try:
            document = self.repository.db.query(self.repository.model).filter(
                self.repository.model.id_documento == document_id
            ).first()
            
            if document:
                # Guardar ruta antes de eliminar
                file_path = document.ruta_archivo
                
                # Eliminar registro de BD
                self.repository.db.delete(document)
                self.repository.db.commit()
                
                # Eliminar archivo físico si se solicita
                if delete_file and os.path.exists(file_path):
                    os.remove(file_path)
                
                return True
            return False
        except Exception as e:
            self.repository.db.rollback()
            print(f"Error en delete_document: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de documentos"""
        try:
            total = self.repository.db.query(self.repository.model).count()
            
            # Contar por tipo de archivo
            tipos = self.repository.db.query(
                self.repository.model.tipo_archivo
            ).all()
            
            por_tipo = {}
            for (tipo,) in tipos:
                if tipo:
                    por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
            
            # Contar por proyecto
            proyectos = self.repository.db.query(
                self.repository.model.proyecto_id_fk
            ).filter(
                self.repository.model.proyecto_id_fk.isnot(None)
            ).all()
            
            documentos_con_proyecto = len(proyectos)
            documentos_sin_proyecto = total - documentos_con_proyecto
            
            return {
                'total': total,
                'con_proyecto': documentos_con_proyecto,
                'sin_proyecto': documentos_sin_proyecto,
                'por_tipo': por_tipo
            }
        except Exception as e:
            print(f"Error en get_statistics: {e}")
            return {
                'total': 0,
                'con_proyecto': 0,
                'sin_proyecto': 0,
                'por_tipo': {}
            }
    
    def search_documents(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar documentos por nombre de archivo"""
        try:
            documents = self.repository.db.query(self.repository.model).filter(
                self.repository.model.nombre_archivo.ilike(f'%{search_term}%')
            ).order_by(self.repository.model.fecha_subida.desc()).all()
            
            return [self._document_to_dict(d) for d in documents]
        except Exception as e:
            print(f"Error en search_documents: {e}")
            return []