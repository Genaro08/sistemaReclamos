from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class EsquemaBaseConfig(BaseModel):
    """
    Configuración base que convierte automáticamente atributos de Python a camelCase en el JSON.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class CategoriaBase(EsquemaBaseConfig):
    """
    Campos base comunes para una categoría o concepto.
    """
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre único del concepto o categoría")
    descripcion: str | None = Field(None, max_length=500, description="Descripción corta del área de conocimiento")


class CategoriaCrear(CategoriaBase):
    """
    DTO para la solicitud de creación de una nueva categoría.
    """
    pass


class CategoriaActualizar(EsquemaBaseConfig):
    """
    DTO para la solicitud de actualización parcial de una categoría existente.
    """
    nombre: str | None = Field(None, min_length=2, max_length=100)
    descripcion: str | None = Field(None, max_length=500)
    activa: bool | None = None


class CategoriaRespuesta(CategoriaBase):
    """
    DTO de respuesta pública de una categoría.
    """
    id: int
    activa: bool
