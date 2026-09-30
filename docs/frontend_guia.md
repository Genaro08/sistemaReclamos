######## Frontend React + TypeScript + Vite - Guía Paso a Paso ########

1: OBJETIVO DEL FRONTEND
--------------------------------------------------------------------------------
Construir una interfaz SPA (Single Page Application) moderna, reactiva y elegante para el "Sistema de Gestión de Reclamos e Inteligencia Técnica", conectada al backend FastAPI.

--------------------------------------------------------------------------------
2: COMANDOS DE INICIALIZACIÓN E INSTALACIÓN DE LIBRERÍAS
--------------------------------------------------------------------------------

A. Crear el proyecto React con TypeScript vía Vite:
   Comando: npm create vite@latest frontend -- --template react-ts

B. Ingresar a la carpeta e instalar dependencias principales:
   Comando: cd frontend
   Comando: npm install react-router-dom axios lucide-react

C. Ejecutar el servidor de desarrollo local:
   Comando: npm run dev (Disponible por defecto en http://localhost:5173)

--------------------------------------------------------------------------------
3: ESTRUCTURA DE CARPETAS Y ARCHIVOS DEL FRONTEND
--------------------------------------------------------------------------------

 frontend/
 ├── public/                      (Assets estáticos públicos: favicon, imágenes)
 ├── src/
 │   ├── api/                     (Configuración de Axios e interceptores JWT)
 │   │   ├── clienteAxios.ts      (Instancia Axios con baseURL y Bearer Token)
 │   │   ├── authApi.ts           (Peticiones login, registro, refresh token)
 │   │   ├── categoriaApi.ts      (Peticiones CRUD de categorías)
 │   │   ├── articuloApi.ts       (Peticiones artículos, plantillas y % búsqueda)
 │   │   └── reclamoApi.ts        (Peticiones reclamos, asignación, comentarios)
 │   │
 │   ├── components/              (Componentes UI reutilizables)
 │   │   ├── common/              (Botones, Inputs, Modales, Spinner, Badges)
 │   │   │   ├── InsigniaEstado.tsx (Badge de color para PENDING, RESOLVED, etc.)
 │   │   │   ├── InsigniaPrioridad.tsx (Badge para LOW, HIGH, CRITICAL)
 │   │   │   ├── Modal.tsx        (Modal reutilizable)
 │   │   │   └── Cargando.tsx     (Spinner loader)
 │   │   └── layout/              (Estructura general)
 │   │       ├── Navbar.tsx       (Barra superior con perfil y botón Logout)
 │   │       ├── Sidebar.tsx      (Menú lateral desplegable según rol)
 │   │       └── LayoutPrincipal.tsx (Contenedor común de las páginas)
 │   │
 │   ├── context/                 (Gestión de Estado Global de Autenticación)
 │   │   └── AuthContext.tsx      (Provee usuario, token, login, logout, rol)
 │   │
 │   ├── hooks/                   (Hooks personalizados React)
 │   │   └── useAuth.ts           (Shortcut para consumir AuthContext)
 │   │
 │   ├── pages/                   (Vistas/Páginas completas de la aplicación)
 │   │   ├── auth/
 │   │   │   ├── LoginPage.tsx    (Inicio de sesión)
 │   │   │   ├── RegistroPage.tsx (Registro de nuevos usuarios)
 │   │   │   └── RecuperarPasswordPage.tsx (Recuperación por email)
 │   │   ├── dashboard/
 │   │   │   └── DashboardPage.tsx (Métricas y resumen según rol)
 │   │   ├── categorias/
 │   │   │   └── CategoriasPage.tsx (Gestión CRUD de categorías/conceptos)
 │   │   ├── conocimiento/
 │   │   │   ├── BaseConocimientoPage.tsx (Buscador por % coincidencia y listado)
 │   │   │   ├── CrearArticuloPage.tsx (Redacción técnica y plantillas)
 │   │   │   └── DetalleArticuloPage.tsx (Ver guía técnica completa)
 │   │   └── reclamos/
 │   │       ├── ReclamosPage.tsx (Listado de tickets con filtros)
 │   │       ├── NuevoReclamoPage.tsx (Creación de ticket con auto % coincidencia)
 │   │       └── DetalleReclamoPage.tsx (Asignación, estados, chat y notas privadas)
 │   │
 │   ├── routes/                  (Enrutamiento con React Router)
 │   │   ├── RutaProtegida.tsx    (Guardián que valida JWT y roles RBAC)
 │   │   └── RutasApp.tsx         (Definición de <Routes> y <Route>)
 │   │
 │   ├── types/                   (Interfaces TypeScript alineadas con Backend DTOs)
 │   │   ├── usuario.ts           (Interface Usuario, RolUsuario)
 │   │   ├── categoria.ts         (Interface Categoria)
 │   │   ├── articulo.ts          (Interface Articulo, Plantilla)
 │   │   └── reclamo.ts           (Interface Reclamo, Comentario, Historial)
 │   │
 │   ├── index.css                (Diseño Vanilla CSS moderno con variables CSS)
 │   ├── App.tsx                  (Proveedor de Contexto y Rutas)
 │   └── main.tsx                 (Punto de entrada de React DOM)
 ├── index.html                   (Plantilla HTML5 principal)
 ├── package.json                 (Dependencias del proyecto)
 └── vite.config.ts               (Configuración de Vite y Server Proxy)

--------------------------------------------------------------------------------
4: CONEXIÓN Y COMUNICACIÓN CON EL BACKEND FASTAPI
--------------------------------------------------------------------------------

A. Configuración de BaseURL y CORS:
   - El cliente Axios apunta a `http://localhost:8000/api/v1`.
   - FastAPI ya tiene habilitado el middleware CORSMiddleware.

B. Interceptor de Peticiones (JWT Bearer Token):
   - Cada petición saliente adjunta en las cabeceras: `Authorization: Bearer <tokenAcceso>`.
   - El token se almacena de forma segura en `localStorage` o memoria de AuthContext.

C. Interceptor de Respuestas (Manejo de Errores y ExcepcionDominio):
   - Si el backend retorna 401 (Token expirado), el interceptor intenta la renovación automática vía `/auth/refresh` o redirige al Login.
   - Si retorna 400, 403 o 404 con `{"exito": false, "error": "mensaje"}`, Axios extrae el mensaje de error de dominio para mostrar alertas al usuario.

--------------------------------------------------------------------------------
5: METODOLOGÍA DE DESARROLLO VERTICAL EN EL FRONTEND
--------------------------------------------------------------------------------
Para construir el frontend de forma ordenada, avanzaremos módulo por módulo siguiendo 4 pasos:

PASO 1: TIPOS TYPESCRIPT (`src/types/*.ts`)
--------------------------------------------
- Definición de las interfaces TS mapeando los DTOs en `camelCase` enviados por la API.

PASO 2: SERVICIO API (`src/api/*.ts`)
--------------------------------------
- Creación de funciones asíncronas para llamar a los endpoints de FastAPI con Axios.

PASO 3: COMPONENTES UI Y PÁGINAS (`src/pages/*`)
-------------------------------------------------
- Maquetación estética con Vanilla CSS (colores modernos, modo oscuro pulido, micro-animaciones).
- Manejo de estados de carga (`loading`), errores y estados de formularios.

PASO 4: RUTAS Y SEGURIDAD (`src/routes/*`)
-------------------------------------------
- Registro de las vistas en `RutasApp.tsx` y protección con `RutaProtegida.tsx` verificando el rol del usuario (`USER`, `OPERATOR`, `ADMIN`).

--------------------------------------------------------------------------------
6: EXPLICACIÓN DETALLADA DE ARCHIVOS Y ARQUITECTURA DE CSS
--------------------------------------------------------------------------------

A. EXPLICACIÓN FÁCIL Y ENTENDIBLE DE CADA ARCHIVO:

1. `App.tsx`:
   Es el componente raíz principal de React. Su única responsabilidad es envolver a toda la aplicación con los proveedores globales (`BrowserRouter` para la navegación y `AuthProvider` para el estado del usuario) e instanciar `RutasApp`.

2. `AuthContext.tsx`:
   Es el "cerebro" central de la sesión. Mantiene en la memoria viva de React al `usuario` logueado, gestiona el almacenamiento persistente de los JWT tokens en `localStorage` y expone las funciones `login()`, `registro()` y `logout()`.

3. `useAuth.ts` (Hook personalizado):
   Es un "acceso directo" para consumir el `AuthContext` en cualquier componente.
   - ¿Por qué existe en vez de usar `useContext(AuthContext)` directamente?
     Sin este hook, en cada archivo tendrías que escribir 2 imports (`useContext` y `AuthContext`) y validar si el contexto no es `undefined`. Con `useAuth()`, simplificás la llamada a 1 sola línea: `const { usuario, logout } = useAuth();` y prevenís errores si alguien intenta usarlo fuera del `<AuthProvider>`.

4. `index.css` (Diseño Global / Design System):
   Almacena las variables CSS globales (`--primary`, `--bg-primary`, etc.), el reset básico de HTML y tipografía.

5. `LoginPage.tsx` / `RegistroPage.tsx`:
   Son las vistas/pantallas de interfaz. Contienen el formulario (JSX/HTML), capturan los inputs del usuario, invocan a `useAuth()` para mandar los datos a la API y manejan los estados visuales (spinners de carga y alertas de error).

6. `DashboardPage.tsx`:
   Es la pantalla inicial de bienvenida protegida a la que se redirige al usuario apenas inicia sesión con éxito.

7. `RutaProtegida.tsx` (Guardián de Seguridad):
   Componente envoltorio que verifica en tiempo real si el usuario tiene sesión activa y si su rol (`USER`, `OPERATOR`, `ADMIN`) tiene permiso para ver la página. Si no está logueado, lo redirige automáticamente a `/login`.

8. `RutasApp.tsx`:
   Mapa central de rutas con React Router (`<Routes>` y `<Route>`) que define a qué componente corresponde cada URL (`/login`, `/registro`, `/dashboard`).

--------------------------------------------------------------------------------
B. ARQUITECTURA DE CSS: ¿CÓMO EVITAR QUE `index.css` CREZCA DESMESURADAMENTE?
--------------------------------------------------------------------------------
En aplicaciones profesionales se evita colocar todo el CSS en un solo archivo `index.css`. La mejor práctica recomendada es:

1. `index.css` (Ligero): Mantiene únicamente variables CSS globales (`--primary`, `--bg-card`), resets de margen/padding y fuentes.
2. CSS por Módulo / Componente (ej: `AuthPages.css` o CSS Modules `LoginPage.module.css`):
   Cada pantalla o módulo funcional importa su propio archivo de estilos.
   - Vite soporta **CSS Modules** de forma nativa (`.module.css`), lo que genera nombres de clases únicos y evita colisiones de estilos entre páginas distintas.

