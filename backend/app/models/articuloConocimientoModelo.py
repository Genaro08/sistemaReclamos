from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.articuloRelacionadoModelo import articulos_relacionados

if TYPE_CHECKING:
    from app.models.categoriaModelo import Categoria
    from app.models.usuarioModelo import Usuario


class ArticuloConocimiento(Base):
    """
    Modelo ORM que representa los desarrollos técnicos de conocimiento
    asociados a un concepto/categoría.
    """
    __tablename__ = "articulosConocimiento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    resumen: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contenidoTecnico: Mapped[str] = mapped_column(Text, nullable=False)  # HTML/Markdown técnico
    etiquetas: Mapped[str] = mapped_column(String(255), nullable=False)  # Keywords para % de coincidencia
    vecesUtilizado: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Claves Foráneas
    categoriaId: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    autorId: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # Relaciones SQLAlchemy
    categoria: Mapped["Categoria"] = relationship("Categoria")
    autor: Mapped["Usuario"] = relationship("Usuario")

    # Relación Muchos a Muchos (M:N) cruzada entre artículos de conocimiento
    articulosRelacionados: Mapped[list["ArticuloConocimiento"]] = relationship(
        "ArticuloConocimiento",
        secondary=articulos_relacionados,
        primaryjoin=id == articulos_relacionados.c.articulo_origen_id,
        secondaryjoin=id == articulos_relacionados.c.articulo_destino_id,
    )

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
