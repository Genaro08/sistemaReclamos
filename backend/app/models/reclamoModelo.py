from datetime import datetime, timezone
import enum
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.articuloConocimientoModelo import ArticuloConocimiento
    from app.models.categoriaModelo import Categoria
    from app.models.plantillaRespuestaModelo import PlantillaRespuesta
    from app.models.usuarioModelo import Usuario


class PrioridadReclamo(str, enum.Enum):
    """
    Enum de prioridades de un reclamo/ticket.
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EstadoReclamo(str, enum.Enum):
    """
    Enum de estados posibles del ciclo de vida de un reclamo/ticket.
    """
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_INFO = "WAITING_INFO"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class Reclamo(Base):
    """
    Modelo ORM que representa los tickets o reclamos generados por los usuarios.
    """
    __tablename__ = "reclamos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    prioridad: Mapped[PrioridadReclamo] = mapped_column(
        SQLEnum(PrioridadReclamo, name="prioridad_reclamo_enum"),
        default=PrioridadReclamo.MEDIUM,
        nullable=False
    )
    estado: Mapped[EstadoReclamo] = mapped_column(
        SQLEnum(EstadoReclamo, name="estado_reclamo_enum"),
        default=EstadoReclamo.PENDING,
        nullable=False
    )

    # Claves Foráneas
    categoriaId: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    creadorId: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    responsableId: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    articuloAplicadoId: Mapped[int | None] = mapped_column(ForeignKey("articulosConocimiento.id"), nullable=True)
    plantillaAplicadaId: Mapped[int | None] = mapped_column(ForeignKey("plantillasRespuesta.id"), nullable=True)

    # Porcentaje de Coincidencia automática calculada por el backend
    porcentajeCoincidenciaAuto: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Relaciones SQLAlchemy
    categoria: Mapped["Categoria"] = relationship("Categoria")
    creador: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[creadorId])
    responsable: Mapped["Usuario | None"] = relationship("Usuario", foreign_keys=[responsableId])
    articuloAplicado: Mapped["ArticuloConocimiento | None"] = relationship("ArticuloConocimiento")
    plantillaAplicada: Mapped["PlantillaRespuesta | None"] = relationship("PlantillaRespuesta")

    # Timestamps
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    fechaResolucion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fechaCierre: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
