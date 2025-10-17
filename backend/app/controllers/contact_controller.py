# Archivo 25/43: app/controllers/contact_controller.py
from typing import List, Dict, Any
from .base_controller import BaseController


class ContactController(BaseController):
    """Controlador para gestión de contactos"""
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validar datos específicos de contactos"""
        required_fields = ['nombre', 'tipo']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"El campo {field} es obligatorio")
        
        valid_types = ['persona', 'empresa']
        if data['tipo'] not in valid_types:
            raise ValueError(f"Tipo debe ser: {', '.join(valid_types)}")
        
        return data
    
    def _contact_to_dict(self, contact) -> Dict[str, Any]:
        """Convertir objeto Contact a diccionario para serialización"""
        if contact is None:
            return None
        
        return {
            'id_contacto': contact.id_contacto,
            'nombre': contact.nombre,
            'tipo': contact.tipo,
            'telefono': contact.telefono,
            'email': contact.email,
            'direccion': contact.direccion,
            'activo': contact.activo
        }
    
    def get_by_type(self, tipo: str) -> List[Dict[str, Any]]:
        """Obtener contactos por tipo"""
        try:
            contacts = self.repository.db.query(self.repository.model).filter(
                self.repository.model.tipo == tipo
            ).all()
            return [self._contact_to_dict(contact) for contact in contacts]
        except Exception as e:
            print(f"Error en get_by_type: {e}")
            return []
    
    def search_by_name(self, nombre: str) -> List[Dict[str, Any]]:
        """Buscar contactos por nombre"""
        try:
            all_contacts = self.repository.get_all()
            filtered = [c for c in all_contacts if nombre.lower() in c.nombre.lower()]
            return [self._contact_to_dict(contact) for contact in filtered]
        except Exception as e:
            print(f"Error en search_by_name: {e}")
            return []
    
    def get_contact_by_id(self, contact_id: int) -> Dict[str, Any]:
        """Obtener contacto por ID como diccionario"""
        try:
            contact = self.repository.get_by_id(contact_id)
            return self._contact_to_dict(contact)
        except Exception as e:
            print(f"Error en get_contact_by_id: {e}")
            return None
    
    def get_all_contacts(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener todos los contactos como diccionarios"""
        try:
            contacts = self.repository.get_all(skip=skip, limit=limit)
            return [self._contact_to_dict(contact) for contact in contacts]
        except Exception as e:
            print(f"Error en get_all_contacts: {e}")
            return []
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo contacto y retornar como diccionario"""
        try:
            validated_data = self.validate_data(data)
            contact = self.repository.create(validated_data)
            return self._contact_to_dict(contact)
        except Exception as e:
            print(f"Error en create contact: {e}")
            raise e
    
    def update_contact(self, contact_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar contacto y retornar como diccionario"""
        try:
            contact = self.repository.update(contact_id, data)
            return self._contact_to_dict(contact)
        except Exception as e:
            print(f"Error en update_contact: {e}")
            return None