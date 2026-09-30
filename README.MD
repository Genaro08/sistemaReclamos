# Sistema de Gestión de Reclamos e Inteligencia Técnica

Plataforma Web Full-Stack diseñada para la centralización, seguimiento y resolución de solicitudes técnicas internas, integrando un motor de recomendación basado en base de conocimientos y control de acceso basado en roles (RBAC).

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Stack Tecnológico](#stack-tecnológico)
- [Arquitectura de Software](#arquitectura-de-software)
- [Funcionalidades Principales](#funcionalidades-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
  - [Requisitos Previos](#requisitos-previos)
  - [Configuración del Backend](#configuración-del-backend)
  - [Ejecución de Pruebas Unitarias](#ejecución-de-pruebas-unitarias)
  - [Configuración del Frontend](#configuración-del-frontend)
- [Documentación de la API](#documentación-de-la-api)

---

## Descripción del Proyecto

El sistema resuelve la dispersión de reclamos e incidencias operativas en organizaciones, proveyendo un flujo estructurado de atención. Combina el registro de tickets con una **Base de Conocimientos Técnica** y un **Algoritmo de Coincidencia Automática por Palabras Clave**, permitiendo a los operadores resolver incidencias rápidamente utilizando artículos técnicos y plantillas de respuesta predefinidas.

---

## Stack Tecnológico

### Backend
- **Lenguaje:** Python 3.12+
- **Framework Web:** FastAPI (API RESTful asíncrona)
- **ORM:** SQLAlchemy 2.0 (Mapeo Relacional Declarativo)
- **Migraciones de BD:** Alembic
- **Validación y DTOs:** Pydantic V2 (con generador de alias `to_camel` para interoperabilidad JSON)
- **Seguridad:** JWT (Tokens de Acceso y Renovación), Hashing Bcrypt
- **Testing:** Pytest (Suite automatizada con base de datos en memoria SQLite `StaticPool`)

### Base de Datos
- **Motor:** PostgreSQL (Desplegado en Supabase con Connection Pooling)

### Frontend
- **Librería UI:** React 18
- **Lenguaje:** TypeScript
- **Herramienta de Construcción:** Vite
- **Enrutamiento:** React Router DOM v6
- **Cliente HTTP:** Axios (con interceptores automáticos para Bearer Tokens y manejo de refresh token)
- **Estilos:** Vanilla CSS (Diseño responsivo, modo oscuro y variables CSS)

---

## Arquitectura de Software

La aplicación sigue el patrón de **Monolito Modular** articulado en capas claras de responsabilidad (*Feature Slice Architecture*):

```text
  [ Cliente React + TypeScript ]
               │
               │ HTTP / REST (JSON camelCase)
               ▼
   [ API Router (FastAPI) ]
               │
               ├─ Dependencias & RBAC (JWT Guard)
               ▼
  [ Capa de Servicios de Negocio ]
               │
               ├─ Reglas de Dominio & Algoritmo % Coincidencia
               ▼
  [ Modelos ORM (SQLAlchemy 2.0) ]
               │
               ▼
  [ PostgreSQL / Supabase DB ]
```

### Principios Arquitectónicos Clave
1. **Vertical Slice Workflow:** Cada módulo funcional (Categorías, Artículos, Reclamos) se desarrolla en 4 pasos: Schemas DTO -> Servicio -> Router -> Tests Pytest.
2. **Sub-recursos y Entidades Débiles:** Entidades como Plantillas, Comentarios e Historial de Auditoría comparten controladores y servicios con sus entidades padre para garantizar la cohesión del dominio y simplificar la jerarquía REST.
3. **Control de Acceso Basado en Roles (RBAC):**
   - `USER`: Creación y seguimiento de reclamos propios.
   - `OPERATOR`: Redacción de conocimiento técnico, gestión de tickets, notas privadas e interacciones.
   - `ADMIN`: Control total de usuarios, categorías y parámetros del sistema.

---

## Funcionalidades Principales

### 1. Autenticación y Usuarios
- Registro, inicio de sesión y renovación transparente de tokens JWT (Access & Refresh Tokens).
- Recuperación de contraseña mediante email (integración SMTP / Mock).
- Aislamiento de datos según el rol asignado (`USER`, `OPERATOR`, `ADMIN`).

### 2. Base de Conocimiento e Inteligencia Técnica
- Redacción de artículos técnicos profundos con categorización y etiquetas.
- Vinculación de artículos relacionados en esquema autorreferenciado (M:N).
- Plantillas de respuesta pública estandarizadas dirigidas al cliente final.
- **Motor de Búsqueda:** Cálculo automatizado del porcentaje de coincidencia entre las consultas ingresadas y las palabras clave/títulos del conocimiento.

### 3. Gestión de Reclamos y Auditoría
- Creación de reclamos con cálculo de coincidencia técnica automatizado desde el ingreso.
- Ciclo de vida de estados: `PENDING` -> `IN_PROGRESS` -> `WAITING_INFO` -> `RESOLVED` -> `CLOSED` -> `CANCELLED`.
- Asignación de técnicos responsables e incremento de contadores de uso de artículos aplicados.
- Hilo de conversación con soporte para **Comentarios Públicos** y **Notas Técnicas Privadas** (visibles exclusivamente para operadores).
- **Historial de Auditoría:** Registro cronológico de todas las acciones, asignaciones y cambios de estado efectuados sobre cada ticket.

---

## Estructura del Proyecto

```text
sistemaReclamos/
├── backend/
│   ├── alembic/                  # Scripts de migración de base de datos
│   ├── app/
│   │   ├── api/                  # Controladores REST HTTP (v1) y Dependencias
│   │   ├── core/                 # Configuración global, Seguridad JWT y Excepciones
│   │   ├── db/                   # Inicialización de SQLAlchemy y sesiones DB
│   │   ├── models/               # Modelos ORM SQLAlchemy (*Modelo.py)
│   │   ├── schemas/              # DTOs de validación Pydantic V2 (*Schema.py)
│   │   └── services/             # Servicios con Lógica de Negocio (*Service.py)
│   ├── tests/                    # Suite de pruebas Pytest (test_*.py)
│   ├── alembic.ini
│   ├── pytest.ini
│   ├── requirements.txt
│   └── main.py                   # Entrypoint FastAPI
├── docs/                         # Documentación técnica del proyecto
└── README.md                     # Documentación principal del repositorio
```

---

## Instalación y Configuración

### Requisitos Previos
- Python 3.12 o superior
- Node.js 18 o superior
- PostgreSQL (o cuenta en Supabase)

---

### Configuración del Backend

1. **Clonar el repositorio e ingresar a la carpeta del backend:**
   ```bash
   cd backend
   ```

2. **Crear y activar un entorno virtual:**
   - En Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - En Linux / macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno:**
   Crear un archivo `.env` en la raíz de `backend/` tomando como base `.env.example`:
   ```env
   PROYECTO_NOMBRE="Sistema de Gestión de Reclamos"
   API_V1_STR="/api/v1"
   SECRET_KEY="tu_clave_secreta_jwt"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7

   DATABASE_URL="postgresql://usuario:password@host:5432/nombre_bd"
   ```

5. **Aplicar las migraciones de Base de Datos:**
   ```bash
   alembic upgrade head
   ```

6. **Iniciar el servidor de desarrollo:**
   ```bash
   uvicorn app.main:app --reload
   ```
   El servidor estará disponible en: `http://localhost:8000`

---

### Ejecución de Pruebas Unitarias

La suite de pruebas ejecuta escenarios integrales sobre una base de datos aislada en memoria RAM (`SQLite StaticPool`):

```bash
pytest
```

---

### Configuración del Frontend

1. **Ingresar a la carpeta del frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar las dependencias de Node:**
   ```bash
   npm install
   ```

3. **Ejecutar el servidor de desarrollo Vite:**
   ```bash
   npm run dev
   ```
   El cliente web estará disponible en: `http://localhost:5173`

---

## Documentación de la API

Una vez iniciado el servidor backend, la documentación interactiva OpenAPI autogenerada se encuentra disponible en:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
