from sqlalchemy import Column, ForeignKey, Integer, Table
from app.db.base import Base

# Tabla intermedia M:N separada para vincular artículos de conocimiento entre sí
articulos_relacionados = Table(
    "articulos_relacionados",
    Base.metadata,
    Column("articulo_origen_id", Integer, ForeignKey("articulosConocimiento.id", ondelete="CASCADE"), primary_key=True),
    Column("articulo_destino_id", Integer, ForeignKey("articulosConocimiento.id", ondelete="CASCADE"), primary_key=True),
)
