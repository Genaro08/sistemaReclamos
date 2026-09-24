from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.reclamoModelo import Reclamo
    from app.models.usuarioModelo import Usuario


class HistorialReclamo(Base):
    """
    Modelo ORM que representa el registro de auditoría de todas las acciones
    y cambios de estado ocurridos sobre un reclamo.
    """
    __tablename__ = "historialReclamos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reclamoId: Mapped[int] = mapped_column(
        ForeignKey("reclamos.id", ondelete="CASCADE"),
        nullable=False
    )
    usuarioId: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )
    accion: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relaciones SQLAlchemy
    reclamo: Mapped["Reclamo"] = relationship("Reclamo")
    usuario: Mapped["Usuario"] = relationship("Usuario")

    # Timestamp
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
