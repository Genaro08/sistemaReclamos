from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class EsquemaBaseConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class PlantillaBase(EsquemaBaseConfig):
    """
    Campos base para una plantilla de respuesta pública dirigida al usuario.
    """
    titulo: str = Field(..., min_length=2, max_length=150, description="Título corto identificador de la plantilla")
    contenidoUsuario: str = Field(..., min_length=5, description="Texto amigable listo para enviar al usuario")


class PlantillaCrear(PlantillaBase):
    """
    DTO para la creación de una plantilla asociada a un artículo de conocimiento.
    """
    articuloId: Optional[int] = Field(None, description="ID del artículo de conocimiento al que pertenece")


class PlantillaActualizar(EsquemaBaseConfig):
    """
    DTO para la actualización de una plantilla de respuesta.
    """
    titulo: Optional[str] = Field(None, min_length=2, max_length=150)
    contenidoUsuario: Optional[str] = Field(None, min_length=5)


class PlantillaRespuestaSchema(PlantillaBase):
    """
    DTO de respuesta pública de una plantilla.
    """
    id: int
    articuloId: int
    fechaCreacion: datetime
    fechaActualizacion: datetime
