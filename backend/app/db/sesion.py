from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.configuracion import configuracion

# Crear el motor de conexión SQLAlchemy
# pool_pre_ping ayuda a reconectar automáticamente si la conexión de Supabase expira
motorDb = create_engine(
    configuracion.databaseUrl,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Creador de sesiones reutilizables
CreadorSesionesDb = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motorDb
)


def obtenerSesionDb() -> Generator[Session, None, None]:
    """
    Inyector de dependencia para FastAPI.
    Proporciona una sesión de base de datos relacional y garantiza
    su cierre seguro al finalizar la petición HTTP.
    """
    sesion = CreadorSesionesDb()
    try:
        yield sesion
    finally:
        sesion.close()
