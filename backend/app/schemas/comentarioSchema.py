from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
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


class ComentarioCrear(EsquemaBaseConfig):
    """
    DTO para agregar un comentario público o una nota técnica privada a un reclamo.
    """
    contenido: str = Field(..., min_length=1, description="Texto del comentario o nota de soporte")
    esInternoTecnico: bool = Field(default=False, description="True si es una nota privada exclusiva para operadores/administradores")


class ComentarioRespuestaSchema(EsquemaBaseConfig):
    """
    DTO de respuesta pública para un comentario/nota.
    """
    id: int
    reclamoId: int
    usuarioId: int
    contenido: str
    esInternoTecnico: bool
    usuario: Optional[UsuarioRespuesta] = None
    fechaCreacion: datetime
