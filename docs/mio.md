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
 │   │   │   ├── authRouter.py            (A MANO: Creado por nosotros)
 │   │   │   └── categoriaRouter.py       (A MANO: En proceso)
 │   │   └── dependencias.py              (A MANO: Creado por nosotros)
 │   ├── core/                            (A MANO: Creada por nosotros)
 │   │   ├── configuracion.py             (A MANO: Creado por nosotros - Pydantic Settings)
 │   │   ├── email.py                     (A MANO: Creado por nosotros - Enviador SMTP/Mock)
 │   │   ├── excepciones.py               (A MANO: Creado por nosotros - Manejador global)
 │   │   └── seguridad.py                 (A MANO: Creado por nosotros - Bcrypt + JWT)
 │   ├── db/                              (A MANO: Creada por nosotros)
 │   │   ├── base.py                      (A MANO: Creado por nosotros - DeclarativeBase)
 │   │   └── sesion.py                    (A MANO: Creado por nosotros - Engine SQLAlchemy)
 │   ├── models/                          (A MANO: Creada por nosotros)
 │   │   ├── usuarioModelo.py             (A MANO: Creado por nosotros - Tabla usuarios)
 │   │   ├── categoriaModelo.py           (A MANO: Creado por nosotros - Tabla categorias)
 │   │   ├── articuloConocimientoModelo.py(A MANO: Creado por nosotros - Tabla articulosConocimiento)
 │   │   ├── articuloRelacionadoModelo.py (A MANO: Creado por nosotros - Tabla M:N articulos_relacionados)
 │   │   ├── plantillaRespuestaModelo.py  (A MANO: Creado por nosotros - Tabla plantillasRespuesta)
 │   │   ├── reclamoModelo.py             (A MANO: Creado por nosotros - Tabla reclamos)
 │   │   ├── comentarioModelo.py          (A MANO: Creado por nosotros - Tabla comentarios)
 │   │   └── historialReclamoModelo.py    (A MANO: Creado por nosotros - Tabla historialReclamos)
 │   ├── schemas/                         (A MANO: Creada por nosotros)
 │   │   ├── paginacionSchema.py          (A MANO: Creado por nosotros - DTO Genérico Paginado)
 │   │   ├── usuarioSchema.py             (A MANO: Creado por nosotros - DTOs Pydantic)
 │   │   └── categoriaSchema.py           (A MANO: En proceso)
 │   └── services/                        (A MANO: Creada por nosotros)
 │       ├── authService.py               (A MANO: Creado por nosotros - Lógica Auth)
 │       └── categoriaService.py          (A MANO: En proceso)
 ├── alembic/                             (VÍA COMANDO: Creada por 'alembic init alembic')
 │   ├── env.py                           (VÍA COMANDO: Creado por 'alembic init' + Editado a mano)
 │   ├── script.py.mako                   (VÍA COMANDO: Creado por 'alembic init')
 │   └── versions/                        (VÍA COMANDO: Creada por 'alembic init')
 │       ├── 1fcb98e5fe26_crear_tabla_usuarios.py (VÍA COMANDO)
 │       ├── 72a5ca48158b_agregar_refresh_token_a_usuarios.py (VÍA COMANDO)
 │       └── df44491c5c14_crear_tablas_conocimiento_reclamos_.py (VÍA COMANDO)
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
--------------------------------------------------------------------------------
   - Paso A: Crear el archivo del modelo en `app/models/` con nomenclatura `*Modelo.py` (A MANO).
   - Paso B: Registrar el modelo importándolo en `alembic/env.py` (A MANO).
   - Paso C: Generar el archivo de migración en `alembic/versions/` (VÍA COMANDO).
     Comando: .\.venv\Scripts\alembic revision --autogenerate -m "nombre_descriptivo_migracion"
   - Paso D: Aplicar los cambios físicamente en la BD de Supabase (VÍA COMANDO).
     Comando: .\.venv\Scripts\alembic upgrade head

--------------------------------------------------------------------------------
9: ¿Cuándo hay que volver a ejecutar comandos de Alembic en el futuro?
--------------------------------------------------------------------------------
Se deben ejecutar comandos de Alembic únicamente cuando la estructura en Python difiera de la BD:

1. Al AGREGAR UNA NUEVA TABLA o MODELO en `app/models/`:
   - Se crea el modelo, se importa en `alembic/env.py`, se ejecuta `alembic revision --autogenerate` y luego `alembic upgrade head`.

2. Al MODIFICAR UNA TABLA EXISTENTE:
   - Si agregás una columna nueva (ej: `telefono` a `usuarioModelo.py`).
   - Si borrás o renombrás una columna.
   - Si cambiás un tipo de dato, una clave foránea (FK) o un índice.
   - Flujo: Editar modelo -> `alembic revision --autogenerate -m "modificacion"` -> `alembic upgrade head`.

3. Al DESPLEGAR O INSTALAR EL PROYECTO EN UNA COMPUTADORA NUEVA:
   - Solo se ejecuta: `alembic upgrade head` (Esto lee el historial de la carpeta `alembic/versions/` y crea de un tiro todas las tablas en la BD vacía, sin necesidad de generar una nueva revisión).

--------------------------------------------------------------------------------
10: METODOLOGÍA DE DESARROLLO VERTICAL POR MÓDULO (Feature Slice Workflow)
--------------------------------------------------------------------------------
Una vez definidos los modelos ORM en `app/models/` y aplicadas las migraciones de Alembic, cada funcionalidad o módulo del sistema (ej: Categorías, Artículos de Conocimiento, Reclamos) se desarrolla completando 4 pasos verticales consecutivos:

PASO 1: SCHEMAS DTO (`app/schemas/*Schema.py`)
------------------------------------------------
- Definición de los contratos de entrada y salida con Pydantic V2.
- Separación de responsabilidades entre DTO de creación/edición (ej: `CategoriaCrear`) y DTO de respuesta pública (ej: `CategoriaRespuesta`).
- Configuración de `to_camel` en la clase base (`model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)`) para convertir automáticamente de `snake_case` (Python) a `camelCase` (JSON/React).

PASO 2: SERVICIO DE NEGOCIO (`app/services/*Service.py`)
---------------------------------------------------------
- Implementación de la lógica de negocio pura y consultas ORM con SQLAlchemy 2.0 (`select`, `add`, `commit`, `refresh`).
- Validación de reglas de dominio (ej: verificar que el nombre no esté duplicado, que el registro exista y esté activo).
- Lanzamiento de excepciones personalizadas (`ExcepcionDominio(mensaje, codigoEstado)`).
- Mantiene a los controladores (routers) limpios de lógica SQL.

PASO 3: ROUTER / CONTROLADOR HTTP (`app/api/v1/*Router.py` y `app/main.py`)
---------------------------------------------------------------------------
- Definición de las rutas REST con decoradores de FastAPI (`@router.get`, `@router.post`, `@router.put`, `@router.delete`).
- Inyección de dependencias para sesión de BD (`db: Session = Depends(obtenerSesionDb)`) y seguridad por roles RBAC (`usuarioActual = Depends(requerirRoles([RolUsuario.ADMIN]))`).
- Especificación del modelo de respuesta `response_model` y status codes HTTP (ej: `201 CREATED`, `200 OK`, `404 NOT FOUND`).
- Registro del router en la aplicación principal en `app/main.py` mediante `app.include_router(...)`.

PASO 4: PRUEBAS AUTOMATIZADAS (`tests/test_*.py`)
-------------------------------------------------
- Creación del archivo de prueba específico del módulo.
- Escenarios de éxito: Peticiones legítimas con status `200` o `201`.
- Escenarios de error: Peticiones duplicadas, datos inválidos o acceso sin permisos retornando `400`, `401` o `403`.
- Ejecución rápida en la base de datos aislada en memoria RAM (`sqlite:///:memory:`) con el comando: `.\.venv\Scripts\pytest`.