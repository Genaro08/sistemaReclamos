from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from app.models.reclamoModelo import EstadoReclamo, PrioridadReclamo
from app.schemas.articuloSchema import ArticuloResumenSchema
from app.schemas.categoriaSchema import CategoriaRespuesta
from app.schemas.plantillaSchema import PlantillaRespuestaSchema
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


class ReclamoBase(EsquemaBaseConfig):
    """
    Campos base comunes para un ticket o reclamo del sistema.
    """
    titulo: str = Field(..., min_length=3, max_length=200, description="Título descriptivo del problema o solicitud")
    descripcion: str = Field(..., min_length=5, description="Detalle o cuerpo completo del reclamo")
    prioridad: PrioridadReclamo = Field(default=PrioridadReclamo.MEDIUM, description="Nivel de prioridad (LOW, MEDIUM, HIGH, CRITICAL)")
    categoriaId: int = Field(..., description="ID de la categoría a la que pertenece el reclamo")


class ReclamoCrear(ReclamoBase):
    """
    DTO para la creación de un nuevo reclamo por parte de un usuario.
    """
    pass


class ReclamoCambiarEstado(EsquemaBaseConfig):
    """
    DTO para que un operador/administrador actualice el estado del reclamo
    y opcionalmente vincule la solución aplicada de la Base de Conocimiento.
    """
    estado: EstadoReclamo = Field(..., description="Nuevo estado del ticket (ej: IN_PROGRESS, RESOLVED, CLOSED)")
    articuloAplicadoId: Optional[int] = Field(None, description="ID del artículo técnico utilizado para solucionar el ticket")
    plantillaAplicadaId: Optional[int] = Field(None, description="ID de la plantilla de respuesta enviada al usuario")


class ReclamoAsignarResponsable(EsquemaBaseConfig):
    """
    DTO para asignar o reasignar un técnico u operador responsable del reclamo.
    """
    responsableId: int = Field(..., description="ID del usuario técnico asignado")


class ReclamoRespuestaSchema(ReclamoBase):
    """
    DTO de respuesta pública completa de un reclamo/ticket con relaciones anidadas y timestamps.
    """
    id: int
    estado: EstadoReclamo
    creadorId: int
    responsableId: Optional[int] = None
    articuloAplicadoId: Optional[int] = None
    plantillaAplicadaId: Optional[int] = None
    porcentajeCoincidenciaAuto: Optional[float] = None

    categoria: Optional[CategoriaRespuesta] = None
    creador: Optional[UsuarioRespuesta] = None
    responsable: Optional[UsuarioRespuesta] = None
    articuloAplicado: Optional[ArticuloResumenSchema] = None
    plantillaAplicada: Optional[PlantillaRespuestaSchema] = None

    fechaCreacion: datetime
    fechaActualizacion: datetime
    fechaResolucion: Optional[datetime] = None
    fechaCierre: Optional[datetime] = None
