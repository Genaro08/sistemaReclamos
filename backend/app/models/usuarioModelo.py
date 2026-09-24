import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class RolUsuario(str, enum.Enum):
    """
    Enum de roles de usuario para el control de acceso (RBAC).
    """
    USER = "USER"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"


class Usuario(Base):
    """
    Modelo ORM SQLAlchemy que representa la tabla 'usuarios' en PostgreSQL.
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(75), nullable=False)
    apellido: Mapped[str] = mapped_column(String(75), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    passwordHash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(
        SQLEnum(RolUsuario, name="rol_usuario_enum"),
        default=RolUsuario.USER,
        nullable=False
    )
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)
    refreshToken: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
