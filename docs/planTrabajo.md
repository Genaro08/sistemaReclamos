# Plan de Trabajo Incremental - Sistema de Gestión de Reclamos

Este documento es la guía de diseño, arquitectura y roadmap específico de este proyecto.

---

## 📌 1. Estructura Backend Completa

```text
backend/
├── app/
│   ├── api/          # Rutas REST (Endpoints de FastAPI que reciben peticiones HTTP)
│   ├── core/         # Configuración central (Pydantic Settings para .env), seguridad y errores
│   ├── db/           # Conexión a PostgreSQL mediante SQLAlchemy (Motor y Sesiones)
│   ├── models/       # Modelos ORM (Clases Python que definen las tablas de la BD)
│   ├── schemas/      # Esquemas Pydantic (Validadores de los datos JSON de la API)
│   └── services/     # Capa de Lógica de Negocio (Servicios para mantener routers delgados)
├── alembic/          # Control de versiones de la base de datos (Migraciones SQL)
├── tests/            # Pruebas automatizadas con Pytest
├── .env              # Variables secretas (URL de Supabase, JWT Secret) - Ignorado en Git
├── .env.example      # Plantilla con los nombres de variables necesarios
├── alembic.ini       # Archivo de configuración general de Alembic
├── pytest.ini        # Configuración de ejecutor de pruebas Pytest
└── main.py           # Punto de entrada de la aplicación FastAPI
```

---

## 🗄️ 2. Modelo Relacional Definitivo de Base de Datos (6 Tablas)

### 1. `usuarios`
* `id`: INT (Primary Key, Autoincremental)
* `nombre`: VARCHAR(75)
* `apellido`: VARCHAR(75)
* `email`: VARCHAR(255) (Único, Indexado)
* `passwordHash`: VARCHAR(255)
* `rol`: ENUM ('USER', 'OPERATOR', 'ADMIN') Default 'USER'
* `activo`: BOOLEAN Default True
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 2. `categorias` (Catálogo de Clasificación)
* `id`: INT (Primary Key, Autoincremental)
* `nombre`: VARCHAR(100) (Único - ej: "Hardware", "Software", "Redes")
* `descripcion`: TEXT (Nullable)
* `activa`: BOOLEAN Default True

### 3. `articulosConocimiento` (Módulo Documental / KCS)
* `id`: INT (Primary Key, Autoincremental)
* `titulo`: VARCHAR(200) (ej: "Procedimiento de reconfiguración VPN")
* `contenido`: TEXT (Manual técnico profundo / Diagnóstico interno)
* `respuestaPredeterminada`: TEXT (Nullable - Plantilla de respuesta corta para usuario)
* `modoRespuesta`: ENUM ('SOLO_LECTURA', 'USAR_CONTENIDO', 'USAR_PLANTILLA_CORTA') Default 'SOLO_LECTURA'
* `categoriaId`: INT (Foreign Key -> `categorias.id`)
* `autorId`: INT (Foreign Key -> `usuarios.id`)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaActualizacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 4. `reclamos` (Módulo Reclamos)
* `id`: INT (Primary Key, Autoincremental)
* `titulo`: VARCHAR(200)
* `descripcion`: TEXT
* `categoriaId`: INT (Foreign Key -> `categorias.id`)
* `prioridad`: ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') Default 'MEDIUM'
* `estado`: ENUM ('PENDING', 'IN_PROGRESS', 'WAITING_INFO', 'RESOLVED', 'CLOSED', 'CANCELLED') Default 'PENDING'
* `creadorId`: INT (Foreign Key -> `usuarios.id`)
* `responsableId`: INT (Foreign Key -> `usuarios.id`, Nullable)
* `reclamoRelacionadoId`: INT (Foreign Key -> `reclamos.id`, Nullable - Autoreferenciado)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaActualizacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaResolucion`: TIMESTAMP WITH TIMEZONE (Nullable)
* `fechaCierre`: TIMESTAMP WITH TIMEZONE (Nullable)

### 5. `comentarios`
* `id`: INT (Primary Key, Autoincremental)
* `reclamoId`: INT (Foreign Key -> `reclamos.id` ON DELETE CASCADE)
* `usuarioId`: INT (Foreign Key -> `usuarios.id`)
* `contenido`: TEXT
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 6. `historialReclamos` (Auditoría)
* `id`: INT (Primary Key, Autoincremental)
* `reclamoId`: INT (Foreign Key -> `reclamos.id` ON DELETE CASCADE)
* `usuarioId`: INT (Foreign Key -> `usuarios.id`)
* `accion`: VARCHAR(255) (Ej: "Creó el reclamo", "Cambió el estado a En Progreso")
* `fecha`: TIMESTAMP WITH TIMEZONE Default NOW()

---

## 🚀 3. Estado de Avance por Etapas

### [x] Etapa 1: Inicialización y Estructura Base Limpia
* Proyecto base con FastAPI, SQLAlchemy 2.0, PostgreSQL (Supabase) y Alembic.
* `.gitignore` configurado para seguridad.

### [x] Etapa 2: Módulo de Usuarios y Autenticación JWT (FINALIZADA)
* Modelo `models/usuario.py` creado con `nombre` y `apellido`.
* Migración Alembic generada e impactada en Supabase PostgreSQL.
* Validadores DTO `schemas/usuarioSchema.py`.
* Módulo de seguridad `core/seguridad.py` (bcrypt nativo + PyJWT).
* Servicio `services/authService.py` con registro y login.
* Middleware / Inyección de dependencias `api/dependencias.py` (RBAC `USER`, `OPERATOR`, `ADMIN`).
* Controladores HTTP en `api/v1/authRouter.py` (`POST /auth/registro`, `POST /auth/login`, `GET /auth/me`).
* Pruebas automatizadas ejecutadas exitosamente con Pytest en `tests/test_auth.py` (100% de éxito).

### [ ] Etapa 3: Módulo de Categorías y Documentación / Base de Conocimiento (Próximo paso)
* Modelos `Categoria` y `ArticuloConocimiento`.
* Migración Alembic.
* Schemas DTOs, Servicios y Routers REST.
