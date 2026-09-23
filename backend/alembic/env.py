import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Agregar el directorio raíz del backend al path para poder importar 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importar configuración y la Base de los modelos
from app.core.configuracion import configuracion
from app.db.base import Base

# 3. Importar modelos ORM creados para registrar en Base.metadata
from app.models.usuario import Usuario  # noqa: F401

config = context.config

# 4. Asignar la URL de Supabase desde configuracion.py a Alembic
config.set_main_option("sqlalchemy.url", configuracion.databaseUrl)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 5. Conectar los modelos de Python registrados en Base a Alembic
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online conectándose a PostgreSQL."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
