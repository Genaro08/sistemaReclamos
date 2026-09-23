# Guía Maestra de Conceptos y Patrones Backend

Este documento es una guía genérica y reusable para inicializar proyectos con FastAPI, SQLAlchemy 2.0 y Alembic.

====================================================================
1. ESTRUCTURA COMPLETA DEL BACKEND
====================================================================

 backend/
 ├── app/
 │   ├── api/          : Controllers y rutas HTTP de FastAPI (reciben peticiones y devuelven JSON).
 │   ├── core/         : Configuración (.env), seguridad (JWT, Hashing) y excepciones globales.
 │   ├── db/           : Conexión a la base de datos (Motor SQLAlchemy y Sesiones).
 │   ├── models/       : Modelos ORM (Definición de tablas de la base de datos en Python).
 │   ├── schemas/      : Esquemas Pydantic (Validación de JSON de entrada y salida DTOs).
 │   └── services/     : Capa de Lógica de Negocio (Reglas de negocio y operaciones complejas).
 ├── alembic/          : Carpeta de versiones y migraciones de la base de datos.
 ├── tests/            : Pruebas automatizadas con Pytest (conftest.py y test_*.py).
 ├── .env              : Variables secretas (URL de Supabase y claves JWT) - Ignorado en Git.
 ├── .env.example      : Plantilla pública con los nombres de variables necesarios.
 ├── alembic.ini       : Archivo de configuración general de Alembic (en la raíz de backend/).
 ├── pytest.ini        : Archivo de configuración de la suite de pruebas Pytest.
 ├── requirements.txt  : Lista de librerías instaladas en el proyecto.
 └── main.py           : Archivo de entrada que arranca el servidor web de FastAPI.

--------------------------------------------------------------------
Diferencia entre archivos automáticos y creados a mano:
--------------------------------------------------------------------
- CREADOS AUTOMÁTICAMENTE:
  .venv/                      -> Al ejecutar 'python -m venv .venv'
  alembic/                    -> Al ejecutar 'alembic init alembic'
  alembic.ini                 -> Al ejecutar 'alembic init alembic'
  alembic/env.py              -> Al ejecutar 'alembic init alembic'
  alembic/script.py.mako      -> Al ejecutar 'alembic init alembic'
  alembic/versions/*.py       -> Al ejecutar 'alembic revision --autogenerate'

- CREADOS A MANO POR NOSOTROS:
  requirements.txt
  pytest.ini
  .env y .env.example
  app/main.py
  app/core/configuracion.py
  app/core/excepciones.py
  app/core/seguridad.py
  app/db/base.py
  app/db/sesion.py
  app/models/* (ejemplo: modelo.py)
  app/schemas/* (ejemplo: esquema.py)
  app/services/* (ejemplo: servicio.py)
  app/api/dependencias.py
  app/api/v1/* (ejemplo: router.py)
  tests/conftest.py
  tests/test_*.py

====================================================================
2. PASO A PASO Y COMANDOS EN ORDEN PARA CREAR EL PROYECTO
====================================================================

Paso 1: Crear la carpeta backend e ingresar a ella.

Paso 2: Crear el Entorno Virtual Python (.venv)
Ejecutar en la terminal:
python -m venv .venv

Paso 3: Crear el archivo requirements.txt e instalar dependencias
Crear el archivo backend/requirements.txt e instalar ejecutando en la terminal:
.\.venv\Scripts\pip install -r requirements.txt

Paso 4: Crear la estructura de carpetas de app/
Crear las subcarpetas: app/api, app/core, app/db, app/models, app/schemas, app/services, tests.

====================================================================
3. CÓMO CREAR UN MODELO ORM Y EJECUTAR SU MIGRACIÓN EN ORDEN
====================================================================

Paso A: Crear el archivo del modelo en app/models/ (ejemplo: app/models/miModelo.py)
--------------------------------------------------------------------
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class MiModelo(Base):
    __tablename__ = "mi_tabla"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
--------------------------------------------------------------------

Paso B: Registrar el modelo en backend/alembic/env.py
Agregar la importación del modelo en env.py para que Base.metadata lo registre:
from app.models.miModelo import MiModelo  # noqa: F401

Paso C: Generar el archivo de migración automática
Ejecutar en la terminal:
.\.venv\Scripts\alembic revision --autogenerate -m "crear_tabla_mi_tabla"

Paso D: Aplicar la migración físicamente en la base de datos de Supabase
Ejecutar en la terminal:
.\.venv\Scripts\alembic upgrade head

====================================================================
4. CÓMO CREAR ESQUEMAS DTO EN PYDANTIC (app/schemas/)
====================================================================

Los esquemas Pydantic validan el formato de los datos que entran por JSON en las peticiones HTTP y formatean las respuestas que recibe el cliente.

PATRÓN CÓDIGO GENÉRICO DTO (app/schemas/ejemploSchema.py):
--------------------------------------------------------------------
from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

class EsquemaBaseConfig(BaseModel):
    """Configuración que convierte atributos Python a camelCase en el JSON"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class EjemploCrear(EsquemaBaseConfig):
    """DTO para crear un registro (Petición HTTP POST)"""
    nombre: str
    email: EmailStr

class EjemploRespuesta(EsquemaBaseConfig):
    """DTO para responder datos al cliente (Respuesta HTTP)"""
    id: int
    nombre: str
    email: EmailStr
--------------------------------------------------------------------

====================================================================
5. CÓMO MANEJAR SEGURIDAD: HASHING BCRYPT Y TOKENS JWT (app/core/seguridad.py)
====================================================================

La seguridad en la API se basa en 2 componentes:
1. Hashing de Contraseñas (bcrypt nativo): Las claves nunca se guardan en texto plano en la BD.
2. Tokens de Acceso JWT (PyJWT): Se emiten al autenticarse exitosamente y contienen el ID y rol del usuario.

PATRÓN CÓDIGO MÓDULO SEGURIDAD (app/core/seguridad.py):
--------------------------------------------------------------------
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import jwt
import bcrypt
from app.core.configuracion import configuracion

def generarPasswordHash(passwordPlano: str) -> str:
    """Convierte la contraseña en un hash bcrypt seguro"""
    bytesPassword = passwordPlano.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytesPassword, salt).decode("utf-8")

def verificarPassword(passwordPlano: str, passwordHash: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash"""
    bytesPassword = passwordPlano.encode("utf-8")
    bytesHash = passwordHash.encode("utf-8")
    return bcrypt.checkpw(bytesPassword, bytesHash)

def crearTokenAcceso(datosPayload: dict[str, Any], deltaExpiracion: Optional[timedelta] = None) -> str:
    """Genera un token JWT firmado conteniendo el payload especificado"""
    copiaPayload = datosPayload.copy()
    if deltaExpiracion:
        expiracion = datetime.now(timezone.utc) + deltaExpiracion
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=configuracion.minutosExpiracionToken)
        
    copiaPayload.update({"exp": expiracion})
    return jwt.encode(copiaPayload, configuracion.secretKey, algorithm=configuracion.algoritmo)

def decodificarTokenAcceso(token: str) -> Optional[dict[str, Any]]:
    """Decodifica y valida la firma y vigencia del JWT"""
    try:
        return jwt.decode(token, configuracion.secretKey, algorithms=[configuracion.algoritmo])
    except jwt.PyJWTError:
        return None
--------------------------------------------------------------------

====================================================================
6. CÓMO CREAR CAPA DE SERVICIOS (app/services/)
====================================================================

La capa de servicios concentra las reglas de negocio, validaciones y consultas a la base de datos para mantener los controladores HTTP (routers) delgados y enfocados.

PATRÓN CÓDIGO SERVICIO (app/services/ejemploService.py):
--------------------------------------------------------------------
from sqlalchemy.orm import Session
from app.core.excepciones import ExcepcionDominio

class EjemploService:
    def __init__(self, sesionDb: Session):
        self.sesionDb = sesionDb

    def procesarReglaNegocio(self, datos):
        pass
--------------------------------------------------------------------

====================================================================
7. CÓMO INYECTAR DEPENDENCIAS Y AUTORIZACIÓN POR ROLES (app/api/dependencias.py)
====================================================================

FastAPI utiliza el sistema de Inyección de Dependencias ('Depends') para extraer el token JWT del encabezado 'Authorization: Bearer <token>', buscar al usuario en la BD y validar sus permisos según su rol (RBAC).

PATRÓN CÓDIGO DEPENDENCIAS (app/api/dependencias.py):
--------------------------------------------------------------------
from typing import Callable
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.sesion import obtenerSesionDb
from app.core.seguridad import decodificarTokenAcceso
from app.core.excepciones import ExcepcionDominio
from app.models.usuario import Usuario, RolUsuario

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def obtenerUsuarioActual(
    token: str = Depends(oauth2Scheme),
    sesionDb: Session = Depends(obtenerSesionDb)
) -> Usuario:
    payload = decodificarTokenAcceso(token)
    if not payload:
        raise ExcepcionDominio(mensaje="Token de autenticación inválido o expirado", codigoEstado=status.HTTP_401_UNAUTHORIZED)

    usuarioId = payload.get("id")
    consulta = select(Usuario).where(Usuario.id == usuarioId)
    usuario = sesionDb.execute(consulta).scalar_one_or_none()
    if not usuario or not usuario.activo:
        raise ExcepcionDominio(mensaje="Usuario no encontrado o inactivo", codigoEstado=status.HTTP_401_UNAUTHORIZED)

    return usuario

def requerirRoles(rolesPermitidos: list[RolUsuario]) -> Callable:
    def verificadorRol(usuarioActual: Usuario = Depends(obtenerUsuarioActual)) -> Usuario:
        if usuarioActual.rol not in rolesPermitidos:
            raise ExcepcionDominio(mensaje="Permisos insuficientes", codigoEstado=status.HTTP_403_FORBIDDEN)
        return usuarioActual
    return verificadorRol
--------------------------------------------------------------------

====================================================================
8. CÓMO CREAR Y REGISTRAR ROUTERS HTTP (app/api/v1/ & main.py)
====================================================================

Los routers de FastAPI exponen los endpoints HTTP (GET, POST, PUT, DELETE) e interactúan con la capa de servicio.

PATRÓN CÓDIGO ROUTER (app/api/v1/ejemploRouter.py):
--------------------------------------------------------------------
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.sesion import obtenerSesionDb

ejemploRouter = APIRouter(prefix="/ejemplo", tags=["Ejemplo"])

@ejemploRouter.get("", status_code=status.HTTP_200_OK)
def listarEjemplos(sesionDb: Session = Depends(obtenerSesionDb)):
    return {"mensaje": "Lista de ejemplos"}
--------------------------------------------------------------------

REGISTRO EN main.py:
--------------------------------------------------------------------
from app.api.v1.ejemploRouter import ejemploRouter

app.include_router(ejemploRouter, prefix=configuracion.apiV1Str)
--------------------------------------------------------------------

====================================================================
9. CÓMO PROBAR LA API CON PRUEBAS AUTOMATIZADAS (tests/ con Pytest)
====================================================================

Las pruebas automatizadas aseguran que los endpoints y la seguridad funcionen sin necesidad de probar a mano en el navegador.

Configuración de Pytest (backend/pytest.ini):
--------------------------------------------------------------------
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
--------------------------------------------------------------------

Fixture de BD SQLite en Memoria (backend/tests/conftest.py):
--------------------------------------------------------------------
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.base import Base
from app.db.sesion import obtenerSesionDb

MOTOR_TEST_DB = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
CreadorSesionesTest = sessionmaker(autocommit=False, autoflush=False, bind=MOTOR_TEST_DB)

@pytest.fixture(scope="function")
def sesionDbTest():
    Base.metadata.create_all(bind=MOTOR_TEST_DB)
    sesion = CreadorSesionesTest()
    try:
        yield sesion
    finally:
        sesion.close()
        Base.metadata.drop_all(bind=MOTOR_TEST_DB)

@pytest.fixture(scope="function")
def clienteTest(sesionDbTest):
    def overrideObtenerSesionDb():
        try:
            yield sesionDbTest
        finally:
            pass
    app.dependency_overrides[obtenerSesionDb] = overrideObtenerSesionDb
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()
--------------------------------------------------------------------

Comando para ejecutar las pruebas en la terminal:
.\.venv\Scripts\pytest

====================================================================
10. CÓDIGO DE ARCHIVOS BASE (COPIAR Y PEGAR)
====================================================================

A. Archivo app/core/configuracion.py:
--------------------------------------------------------------------
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Configuracion(BaseSettings):
    proyectoNombre: str = Field(default="Mi Proyecto", validation_alias="PROYECTO_NOMBRE")
    apiV1Str: str = Field(default="/api/v1", validation_alias="API_V1_STR")
    databaseUrl: str = Field(default="postgresql://localhost:5432/db", validation_alias="DATABASE_URL")
    secretKey: str = Field(default="secret_key", validation_alias="SECRET_KEY")
    algoritmo: str = Field(default="HS256", validation_alias="ALGORITMO")
    minutosExpiracionToken: int = Field(default=1440, validation_alias="MINUTOS_EXPIRACION_TOKEN")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

configuracion = Configuracion()
--------------------------------------------------------------------

B. Archivo app/db/base.py:
--------------------------------------------------------------------
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
--------------------------------------------------------------------

C. Archivo app/db/sesion.py:
--------------------------------------------------------------------
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.configuracion import configuracion

motorDb = create_engine(configuracion.databaseUrl, pool_pre_ping=True, pool_size=10, max_overflow=20)
CreadorSesionesDb = sessionmaker(autocommit=False, autoflush=False, bind=motorDb)

def obtenerSesionDb() -> Generator[Session, None, None]:
    sesion = CreadorSesionesDb()
    try:
        yield sesion
    finally:
        sesion.close()
--------------------------------------------------------------------

D. Archivo backend/alembic/env.py (Bloque a agregar):
--------------------------------------------------------------------
import sys
import os

# 1. Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importar configuración y la Base de los modelos
from app.core.configuracion import configuracion
from app.db.base import Base

# 3. Asignar la URL de la base de datos a Alembic
config.set_main_option("sqlalchemy.url", configuracion.databaseUrl)

# 4. Conectar los modelos de Python registrados en Base a Alembic
target_metadata = Base.metadata
--------------------------------------------------------------------
