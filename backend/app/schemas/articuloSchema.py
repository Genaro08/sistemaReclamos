from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from app.schemas.categoriaSchema import CategoriaRespuesta
from app.schemas.plantillaSchema import PlantillaRespuestaSchema


class EsquemaBaseConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class ArticuloResumenSchema(EsquemaBaseConfig):
    """
    DTO resumido de un artículo de conocimiento (utilizado para listas de artículos relacionados).
    """
    id: int
    titulo: str
    resumen: Optional[str] = None
    etiquetas: str


class ArticuloBase(EsquemaBaseConfig):
    """
    Campos base comunes para un desarrollo de conocimiento técnico.
    """
    titulo: str = Field(..., min_length=2, max_length=200, description="Título del artículo de conocimiento")
    resumen: Optional[str] = Field(None, max_length=500, description="Breve resumen ejecutivo del tema")
    contenidoTecnico: str = Field(..., min_length=5, description="Desarrollo técnico profundo en HTML/Markdown")
    etiquetas: str = Field(..., min_length=2, max_length=255, description="Keywords separadas por coma para el % de coincidencia")
    categoriaId: int = Field(..., description="ID de la categoría/concepto al que pertenece")


class ArticuloCrear(ArticuloBase):
    """
    DTO para crear un nuevo artículo de conocimiento con IDs de artículos relacionados opcionales.
    """
    articulosRelacionadosIds: Optional[List[int]] = Field(default=[], description="Lista de IDs de otros artículos vinculados")


class ArticuloActualizar(EsquemaBaseConfig):
    """
    DTO para la actualización parcial de un artículo de conocimiento.
    """
    titulo: Optional[str] = Field(None, min_length=2, max_length=200)
    resumen: Optional[str] = Field(None, max_length=500)
    contenidoTecnico: Optional[str] = Field(None, min_length=5)
    etiquetas: Optional[str] = Field(None, min_length=2, max_length=255)
    categoriaId: Optional[int] = None
    articulosRelacionadosIds: Optional[List[int]] = None


class ArticuloRespuestaSchema(ArticuloBase):
    """
    DTO de respuesta pública completa de un artículo de conocimiento,
    incluyendo datos de categoría, plantillas asociadas y artículos relacionados.
    """
    id: int
    vecesUtilizado: int
    autorId: int
    fechaCreacion: datetime
    fechaActualizacion: datetime
    categoria: Optional[CategoriaRespuesta] = None
    plantillas: Optional[List[PlantillaRespuestaSchema]] = []
    articulosRelacionados: Optional[List[ArticuloResumenSchema]] = []


class ArticuloBusquedaRespuesta(ArticuloRespuestaSchema):
    """
    DTO de respuesta para búsquedas por coincidencia, incluyendo el % de similitud calculado.
    """
    porcentajeCoincidencia: float = 0.0

