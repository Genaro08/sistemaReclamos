from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.reclamoModelo import Reclamo
    from app.models.usuarioModelo import Usuario


class Comentario(Base):
    """
    Modelo ORM que representa los mensajes e interacciones dentro de un reclamo/ticket.
    Soporta mensajes públicos (usuario/técnico) y notas internas privadas (solo técnicos).
    """
    __tablename__ = "comentarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reclamoId: Mapped[int] = mapped_column(
        ForeignKey("reclamos.id", ondelete="CASCADE"),
        nullable=False
    )
    usuarioId: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    esInternoTecnico: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relaciones SQLAlchemy
    reclamo: Mapped["Reclamo"] = relationship("Reclamo")
    usuario: Mapped["Usuario"] = relationship("Usuario")

    # Timestamps
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
