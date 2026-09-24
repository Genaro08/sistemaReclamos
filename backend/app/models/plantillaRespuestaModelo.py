from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.articuloConocimientoModelo import ArticuloConocimiento


class PlantillaRespuesta(Base):
    """
    Modelo ORM que representa las plantillas de respuesta pública
    dirigidas a los usuarios finales, asociadas a un desarrollo de conocimiento técnico.
    """
    __tablename__ = "plantillasRespuesta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    articuloId: Mapped[int] = mapped_column(
        ForeignKey("articulosConocimiento.id", ondelete="CASCADE"),
        nullable=False
    )
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    contenidoUsuario: Mapped[str] = mapped_column(Text, nullable=False)

    # Relación SQLAlchemy con el artículo de conocimiento
    articulo: Mapped["ArticuloConocimiento"] = relationship("ArticuloConocimiento")

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
