import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.base import Base
from app.db.sesion import obtenerSesionDb
from app.models.usuario import Usuario  # noqa: F401

# Base de datos SQLite en memoria con StaticPool para mantener viva la BD durante el test
MOTOR_TEST_DB = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
CreadorSesionesTest = sessionmaker(autocommit=False, autoflush=False, bind=MOTOR_TEST_DB)


@pytest.fixture(scope="function")
def sesionDbTest():
    """
    Fixture que crea las tablas en la BD SQLite en memoria
    y provee una sesión limpia para cada test.
    """
    Base.metadata.create_all(bind=MOTOR_TEST_DB)
    sesion = CreadorSesionesTest()
    try:
        yield sesion
    finally:
        sesion.close()
        Base.metadata.drop_all(bind=MOTOR_TEST_DB)


@pytest.fixture(scope="function")
def clienteTest(sesionDbTest):
    """
    Fixture de TestClient de FastAPI inyectando la sesión de BD de prueba.
    """
    def overrideObtenerSesionDb():
        try:
            yield sesionDbTest
        finally:
            pass

    app.dependency_overrides[obtenerSesionDb] = overrideObtenerSesionDb
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()
