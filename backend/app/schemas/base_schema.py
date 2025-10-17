# Archivo 27/43: app/schemas/base_schema.py
# Descripción: Schema base Pydantic para herencia común
# Funcionalidad: Configuraciones base para todos los schemas de validación

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    """
    Schema base para todos los modelos Pydantic.
    Configuración común de serialización.
    """
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True
    )


class TimestampMixin(BaseSchema):
    """Mixin para campos de timestamp comunes"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None