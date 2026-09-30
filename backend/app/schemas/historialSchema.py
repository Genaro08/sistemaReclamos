from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from app.schemas.usuarioSchema import UsuarioRespuesta


class EsquemaBaseConfig(BaseModel):
    """
    Configuración base que convierte automáticamente atributos de Python a camelCase en el JSON.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class HistorialRespuestaSchema(EsquemaBaseConfig):
    """
    DTO de respuesta para los registros de auditoría de un reclamo.
    """
    id: int
    reclamoId: int
    usuarioId: int
    accion: str
    usuario: Optional[UsuarioRespuesta] = None
    fecha: datetime
