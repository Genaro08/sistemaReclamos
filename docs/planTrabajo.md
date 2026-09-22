# Plan de Trabajo Incremental - Sistema de Gestión de Reclamos

Este documento sirve como registro continuo y trazable de la arquitectura, las decisiones técnicas y el progreso incremental del proyecto.

---

## 📌 Información General

* **Proyecto**: Sistema de Gestión de Reclamos e Historial Interno
* **Arquitectura**: Monolito Modular Backend (FastAPI) + SPA Frontend (React + TS + Vite)
* **Base de Datos**: PostgreSQL (Supabase / Local) desacoplada mediante SQLAlchemy 2.0 y Alembic
* **Despliegue**: Frontend y Backend en Vercel (Serverless)

---

## 🛠️ Convenciones del Proyecto

1. **Idioma**: Dominio y comentarios en **Español**.
2. **Nomenclatura**:
   * Archivos y variables/funciones backend: `camelCase` en español (ej: `usuarioService.py`, `reclamoRouter.py`, `obtenerReclamos`).
   * Clases e Interfaces: `PascalCase` (ej: `Usuario`, `ReclamoService`).
   * Base de datos: Tablas y columnas relacionales en español (ej: `usuarios`, `reclamos`, `historialReclamos`).
   * API REST: JSON en `camelCase` mediante configuraciones Pydantic.
3. **Comentarios**: Informativos, concisos y sin elementos decorativos.

---

## 🚀 Estado de Avance por Etapas

### [x] Etapa 1: Inicialización y Configuración Base
* **Backend**:
  * Entorno `.venv` creado con `fastapi`, `sqlalchemy`, `alembic`, `pydantic-settings`, `psycopg2-binary`.
  * Archivo `backend/app/core/configuracion.py` desacoplado leyendo variables del archivo `.env`.
  * Inyección de sesión SQLAlchemy con `pool_pre_ping=True` en `backend/app/db/sesion.py`.
  * Manejo global de excepciones en `backend/app/core/excepciones.py`.
  * Endpoint `/api/v1/health` para verificación de estado del servidor y la BD relacional.
  * Alembic configurado y sincronizado dinámicamente con la base de datos.
* **Frontend**:
  * Aplicación React + TypeScript + Vite inicializada en `frontend/` con dependencias instaladas.

---

### [ ] Etapa 2: Usuarios, Autenticación JWT y Roles (En Proceso)
* Modelo SQLAlchemy `Usuario` (roles: `USER`, `OPERATOR`, `ADMIN`).
* Esquemas Pydantic `usuarioSchema.py`.
* Hashing `bcrypt` y Tokens JWT (`seguridad.py` y `authService.py`).
* Endpoints `/api/v1/auth/registro`, `/login`, `/me`.
* Inyector de dependencias RBAC (control de acceso por roles).
* Primera migración de tabla `usuarios` en la BD.

---

### [ ] Etapa 3: Módulo Principal de Reclamos
* Modelos `Reclamo`, `Prioridad`, `Estado`, `Categoria`.
* Repositorio, Servicio y Router REST con asignaciones, cambios de estado y paginación.

---

### [ ] Etapa 4: Historial de Cambios y Trazabilidad (Auditoría)
* Modelo `HistorialReclamo`.
* Registro automático de eventos en `ReclamoService`.

---

### [ ] Etapa 5: Comentarios y Adjuntos Seguros
* Modelo `Comentario` y subida/descarga protegida de adjuntos (validación MIME y límite 5MB).

---

### [ ] Etapa 6: Lógica de SLA & Dashboard Backend
* Cálculo dinámico de SLA y endpoints de métricas agregadas SQL.

---

### [ ] Etapa 7: Setup Frontend & Autenticación UI
* React Router, `AuthContext` y Rutas Protegidas en React TS.

---

### [ ] Etapa 8: UI Reclamos: Listado, Filtros y Detalle
* Tabla paginada, formulario y vista con historial y comentarios.

---

### [ ] Etapa 9: UI Dashboard & SLA Semáforo
* Tarjetas de resumen, gráficos e indicadores de plazo.

---

### [ ] Etapa 10: Testing (Pytest & Frontend)
* Pruebas automatizadas backend y componentes frontend.

---

### [ ] Etapa 11: Infraestructura Docker
* `Dockerfile` y `docker-compose.yml` para orquestación local.

---

### [ ] Etapa 12: Despliegue en Vercel & README Final
* `vercel.json` para Backend Serverless y Frontend React SPA.
