# Plan de Trabajo Incremental - Sistema de Gestión de Reclamos y Base de Conocimientos

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

## 🗄️ 2. Modelo Relacional Definitivo de Base de Datos (8 Tablas)

### 1. `usuarios` (Autenticación y Control de Accesos RBAC)
* `id`: INT (Primary Key, Autoincremental)
* `nombre`: VARCHAR(75)
* `apellido`: VARCHAR(75)
* `email`: VARCHAR(255) (Único, Indexado)
* `passwordHash`: VARCHAR(255)
* `rol`: ENUM ('USER', 'OPERATOR', 'ADMIN') Default 'USER'
* `activo`: BOOLEAN Default True
* `refreshToken`: VARCHAR(500) (Nullable)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 2. `categorias` (Conceptos y Áreas Técnicas de Conocimiento)
* `id`: INT (Primary Key, Autoincremental)
* `nombre`: VARCHAR(100) (Único, Indexado - ej: "Outlook", "VPN", "Credenciales", "Redes")
* `descripcion`: TEXT (Nullable)
* `activa`: BOOLEAN Default True

### 3. `articulosConocimiento` (Desarrollos Técnicos Específicos para Técnicos)
* `id`: INT (Primary Key, Autoincremental)
* `titulo`: VARCHAR(200) (ej: "Configurar firma institucional HTML en Outlook")
* `resumen`: VARCHAR(500) (Nullable - Breve resumen ejecutivo de 2 líneas)
* `contenidoTecnico`: TEXT (Desarrollo profundo en HTML / Markdown con comandos y diagnóstico)
* `etiquetas`: VARCHAR(255) (Keywords para cálculo automático de % de coincidencia)
* `vecesUtilizado`: INT Default 0 (Contador de éxito de tickets resueltos)
* `categoriaId`: INT (Foreign Key -> `categorias.id`)
* `autorId`: INT (Foreign Key -> `usuarios.id`)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaActualizacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 4. `articulos_relacionados` (Vinculación Cruzada M:N entre Artículos)
* `articuloOrigenId`: INT (Foreign Key -> `articulosConocimiento.id` ON DELETE CASCADE, PK)
* `articuloDestinoId`: INT (Foreign Key -> `articulosConocimiento.id` ON DELETE CASCADE, PK)

### 5. `plantillasRespuesta` (Respuestas Amigables para Usuarios)
* `id`: INT (Primary Key, Autoincremental)
* `articuloId`: INT (Foreign Key -> `articulosConocimiento.id` ON DELETE CASCADE)
* `titulo`: VARCHAR(150) (ej: "Pasos amigables para colocar la firma en Outlook")
* `contenidoUsuario`: TEXT (Texto instruccional limpio para enviar al usuario)

### 6. `reclamos` (Módulo de Reclamos / Tickets)
* `id`: INT (Primary Key, Autoincremental)
* `titulo`: VARCHAR(200)
* `descripcion`: TEXT
* `categoriaId`: INT (Foreign Key -> `categorias.id`)
* `prioridad`: ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') Default 'MEDIUM'
* `estado`: ENUM ('PENDING', 'IN_PROGRESS', 'WAITING_INFO', 'RESOLVED', 'CLOSED', 'CANCELLED') Default 'PENDING'
* `creadorId`: INT (Foreign Key -> `usuarios.id` - Usuario común)
* `responsableId`: INT (Foreign Key -> `usuarios.id`, Nullable - Técnico asignado)
* `articuloAplicadoId`: INT (Foreign Key -> `articulosConocimiento.id`, Nullable)
* `plantillaAplicadaId`: INT (Foreign Key -> `plantillasRespuesta.id`, Nullable)
* `porcentajeCoincidenciaAuto`: FLOAT (Nullable - % de coincidencia calculado)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaActualizacion`: TIMESTAMP WITH TIMEZONE Default NOW()
* `fechaResolucion`: TIMESTAMP WITH TIMEZONE (Nullable)
* `fechaCierre`: TIMESTAMP WITH TIMEZONE (Nullable)

### 7. `comentarios` (Hilo de Seguimiento de Reclamos)
* `id`: INT (Primary Key, Autoincremental)
* `reclamoId`: INT (Foreign Key -> `reclamos.id` ON DELETE CASCADE)
* `usuarioId`: INT (Foreign Key -> `usuarios.id`)
* `contenido`: TEXT
* `esInternoTecnico`: BOOLEAN Default False (Si es True, nota privada de técnicos)
* `fechaCreacion`: TIMESTAMP WITH TIMEZONE Default NOW()

### 8. `historialReclamos` (Auditoría)
* `id`: INT (Primary Key, Autoincremental)
* `reclamoId`: INT (Foreign Key -> `reclamos.id` ON DELETE CASCADE)
* `usuarioId`: INT (Foreign Key -> `usuarios.id`)
* `accion`: VARCHAR(255) (ej: "Aplicó plantilla #4 con 92% de coincidencia")
* `fecha`: TIMESTAMP WITH TIMEZONE Default NOW()

---

## 🚀 3. Estado de Avance por Etapas

### [x] Etapa 1: Inicialización y Estructura Base Limpia
* Proyecto base con FastAPI, SQLAlchemy 2.0, PostgreSQL (Supabase) y Alembic.
* `.gitignore` configurado para seguridad.

### [x] Etapa 2: Módulo de Usuarios y Autenticación JWT (FINALIZADA)
* Modelo `models/usuario.py` creado con `refreshToken` y roles RBAC (`USER`, `OPERATOR`, `ADMIN`).
* Migraciones Alembic impactadas exitosamente en Supabase PostgreSQL.
* Validadores DTO `schemas/usuarioSchema.py`.
* Módulo de seguridad `core/seguridad.py` (bcrypt nativo + PyJWT access & refresh).
* Servicio `services/authService.py` con registro, login, refresh y recupero por email.
* Middleware / Inyección de dependencias `api/dependencias.py`.
* Controladores HTTP en `api/v1/authRouter.py`.
* Pruebas automatizadas con Pytest (100% de éxito).

### [ ] Etapa 3: Definición Incremental de Modelos ORM (EN PROGRESO)
* [ ] Modelo 1: `Categoria` (`app/models/categoria.py`)
* [ ] Modelo 2: `ArticuloConocimiento` y `articulos_relacionados` (`app/models/articuloConocimiento.py`)
* [ ] Modelo 3: `PlantillaRespuesta` (`app/models/plantillaRespuesta.py`)
* [ ] Modelo 4: `Reclamo` y Enums `EstadoReclamo`, `PrioridadReclamo` (`app/models/reclamo.py`)
* [ ] Modelo 5: `Comentario` (`app/models/comentario.py`)
* [ ] Modelo 6: `HistorialReclamo` (`app/models/historialReclamo.py`)
* [ ] Generar migración Alembic global e impactar en Supabase PostgreSQL.

### [ ] Etapa 4: Servicios, Schemas, Routers y Pruebas Automatizadas
* Schemas DTOs, Servicios y Routers REST para Categorías, Base de Conocimiento y Reclamos con cálculo de % de coincidencia.
