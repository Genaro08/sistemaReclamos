from typing import Generic, List, TypeVar
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar('T')


class RespuestaPaginada(BaseModel, Generic[T]):
    """
    Esquema genérico para respuestas con listas paginadas.
    Soporta cualquier tipo de modelo DTO de Pydantic.
    """
    elementos: List[T]
    total: int
    pagina: int
    tamanoPagina: int
    totalPaginas: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
