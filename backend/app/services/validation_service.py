# Archivo 35/40: app/services/validation_service.py
# Descripción: Servicio de validaciones personalizadas
# Funcionalidad: Validaciones de negocio específicas del dominio jurídico

import re
from typing import Dict, Any, List
from datetime import datetime, date


class ValidationService:
    """
    Servicio de validaciones de negocio.
    Validaciones específicas para el dominio jurídico.
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validar formato de teléfono"""
        if not phone:
            return True  # Teléfono es opcional
        
        # Permitir formatos comunes de Guatemala
        pattern = r'^[\+]?[0-9\-\(\)\s]{8,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validar fortaleza de contraseña"""
        validations = {
            "min_length": len(password) >= 6,
            "has_upper": bool(re.search(r'[A-Z]', password)),
            "has_lower": bool(re.search(r'[a-z]', password)),
            "has_number": bool(re.search(r'\d', password)),
            "is_strong": False
        }
        
        # Contraseña fuerte si cumple al menos 3 de 4 criterios
        criteria_met = sum([
            validations["min_length"],
            validations["has_upper"], 
            validations["has_lower"],
            validations["has_number"]
        ])
        
        validations["is_strong"] = criteria_met >= 3
        return validations
    
    @staticmethod
    def validate_date_range(fecha_inicio: date, fecha_fin: date = None) -> bool:
        """Validar rango de fechas"""
        if fecha_fin and fecha_inicio > fecha_fin:
            return False
        return True
    
    @staticmethod
    def validate_project_data(data: Dict[str, Any]) -> List[str]:
        """Validaciones específicas para proyectos jurídicos"""
        errors = []
        
        # Validar fechas
        if 'fecha_inicio' in data and 'fecha_fin' in data:
            if data['fecha_fin'] and data['fecha_inicio'] > data['fecha_fin']:
                errors.append("La fecha de fin no puede ser anterior a la fecha de inicio")
        
        # Validar nombre del proyecto
        if 'nombre' in data and len(data['nombre'].strip()) < 3:
            errors.append("El nombre del proyecto debe tener al menos 3 caracteres")
        
        return errors
    
    @staticmethod
    def validate_task_data(data: Dict[str, Any]) -> List[str]:
        """Validaciones específicas para tareas"""
        errors = []
        
        # Validar fecha de vencimiento
        if 'fecha_vencimiento' in data and data['fecha_vencimiento']:
            if data['fecha_vencimiento'] < date.today():
                errors.append("La fecha de vencimiento no puede ser anterior a hoy")
        
        return errors