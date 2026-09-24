######## Backend FastAPI - Guía Paso a Paso ########

1: Definir el problema conceptualmente (saber exactamente qué querés resolver).

2: Diseñar las tablas y el modelo relacional de la base de datos (relaciones, campos, claves).

3: Crear la carpeta `backend` e ingresar a ella.

4: Crear el Entorno Virtual Python dentro de la carpeta `backend`:
   Comando: python -m venv .venv

5: Crear a mano el archivo `requirements.txt` con las librerías necesarias (fastapi, uvicorn, sqlalchemy, alembic, psycopg2-binary, etc.) e instalarlas en el entorno virtual.
   Comando: .\.venv\Scripts\pip install -r requirements.txt

6: Inicializar Alembic para crear automáticamente la carpeta y archivos de migraciones.
   Comando: .\.venv\Scripts\alembic init alembic

7: Crear a mano la estructura de carpetas de la aplicación (`app/` y `tests/`).

--------------------------------------------------------------------------------
ESTRUCTURA DE CARPETAS Y ARCHIVOS (Identificando Origen: A Mano vs Vía Comando)
--------------------------------------------------------------------------------

 backend/
 ├── app/                                 (A MANO: Creada por nosotros)
 │   ├── api/                             (A MANO: Creada por nosotros)
 │   │   ├── v1/                          (A MANO: Creada por nosotros)
 │   │   │   ├── healthCheckRouter.py     (A MANO: Creado por nosotros)
 │   │   │   └── authRouter.py            (A MANO: Creado por nosotros)
 │   │   └── dependencias.py              (A MANO: Creado por nosotros)
 │   ├── core/                            (A MANO: Creada por nosotros)
 │   │   ├── configuracion.py             (A MANO: Creado por nosotros - Pydantic Settings)
 │   │   ├── excepciones.py               (A MANO: Creado por nosotros - Manejador global)
 │   │   └── seguridad.py                 (A MANO: Creado por nosotros - Bcrypt + JWT)
 │   ├── db/                              (A MANO: Creada por nosotros)
 │   │   ├── base.py                      (A MANO: Creado por nosotros - DeclarativeBase)
 │   │   └── sesion.py                    (A MANO: Creado por nosotros - Engine SQLAlchemy)
 │   ├── models/                          (A MANO: Creada por nosotros)
 │   │   └── usuario.py                   (A MANO: Creado por nosotros - Modelo ORM)
 │   ├── schemas/                         (A MANO: Creada por nosotros)
 │   │   └── usuarioSchema.py             (A MANO: Creado por nosotros - DTOs Pydantic)
 │   └── services/                        (A MANO: Creada por nosotros)
 │       └── authService.py               (A MANO: Creado por nosotros - Lógica de negocio)
 ├── alembic/                             (VÍA COMANDO: Creada por 'alembic init alembic')
 │   ├── env.py                           (VÍA COMANDO: Creado por 'alembic init' + Editado a mano)
 │   ├── script.py.mako                   (VÍA COMANDO: Creado por 'alembic init')
 │   └── versions/                        (VÍA COMANDO: Creada por 'alembic init')
 │       └── xxx_crear_tabla_usuarios.py  (VÍA COMANDO: Creado por 'alembic revision --autogenerate')
 ├── tests/                               (A MANO: Creada por nosotros)
 │   ├── conftest.py                      (A MANO: Creado por nosotros - Fixtures SQLite)
 │   └── test_auth.py                     (A MANO: Creado por nosotros - Pruebas Pytest)
 ├── .env                                 (A MANO: Creado por nosotros con credenciales Supabase)
 ├── .env.example                         (A MANO: Creado por nosotros como plantilla pública)
 ├── alembic.ini                          (VÍA COMANDO: Creado por 'alembic init alembic')
 ├── pytest.ini                           (A MANO: Creado por nosotros para Pytest)
 ├── requirements.txt                     (A MANO: Creado por nosotros)
 └── main.py                              (A MANO: Creado por nosotros - Entrypoint FastAPI)

--------------------------------------------------------------------------------
8: Flujo de trabajo para crear tablas y aplicar migraciones:
   - Paso A: Crear el archivo del modelo en `app/models/` (A MANO).
   - Paso B: Registrar el modelo importándolo en `alembic/env.py` (A MANO).
   - Paso C: Generar el archivo de migración en `alembic/versions/` (VÍA COMANDO).
     Comando: .\.venv\Scripts\alembic revision --autogenerate -m "nombre_migracion"
   - Paso D: Aplicar los cambios físicamente en la BD de Supabase (VÍA COMANDO).
     Comando: .\.venv\Scripts\alembic upgrade head