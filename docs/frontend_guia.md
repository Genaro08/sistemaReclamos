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
--------------------------------------------------------------------------------
7: PLAN MASTER DE ARQUITECTURA FRONTEND EN 4 FASES
--------------------------------------------------------------------------------
Para garantizar un desarrollo escalable y profesional, el frontend se construye siguiendo una arquitectura Bottom-Up (De los cimientos a las páginas):

FASE 1: CONTRATOS DE DATOS Y SERVICIOS API
-------------------------------------------
- 1.1 Interfaces TypeScript (`src/types/`): `usuario.ts`, `categoria.ts`, `articulo.ts`, `reclamo.ts`.
- 1.2 Servicios de Red (`src/api/`): `authApi.ts`, `categoriaApi.ts`, `articuloApi.ts`, `reclamoApi.ts`.

FASE 2: COMPONENTES ATÓMICOS Y LAYOUT ESTRUCTURAL
--------------------------------------------------
- 2.1 Componentes UI Atómicos Reutilizables (`src/components/common/`): `InsigniaEstado.tsx`, `InsigniaPrioridad.tsx`, `Modal.tsx`, `Cargando.tsx`.
- 2.2 Layout Estructural (`src/components/layout/`): `Navbar.tsx`, `Sidebar.tsx`, `LayoutPrincipal.tsx`.

FASE 3: HOOKS PERSONALIZADOS DE ESTADO DE DATOS
-------------------------------------------------
- Encapsulamiento de lógica de consulta, filtrado y mutación con reactividad (`useReclamos`, `useArticulos`).

FASE 4: ENSAMBLADO DE PÁGINAS Y RUTAS
--------------------------------------
- Vistas completas por módulo (`CategoriasPage.tsx`, `BaseConocimientoPage.tsx`, `ReclamosPage.tsx`) integradas en `RutasApp.tsx` con `RutaProtegida.tsx`.

--------------------------------------------------------------------------------
8: CRITERIO DE DISEÑO: SCHEMAS (BACKEND) VS TYPES (FRONTEND)
--------------------------------------------------------------------------------

A. ¿A PARTIR DE QUÉ IDEA SE CREAN LOS SCHEMAS Y TYPES?
-------------------------------------------------------
No se crea 1 sola interfaz por Tabla o Modelo ORM de Base de Datos.
Tanto en el Backend (Pydantic DTOs) como en el Frontend (TypeScript Interfaces), se crean interfaces separadas según el TIPO DE OPERACIÓN HTTP (Caso de Uso):

1. DTO de Lectura / Respuesta (`GET`):
   - Contiene la información completa del recurso retornada por la API: `id` autoincremental, `fechaCreacion`, `vecesUtilizado` y las relaciones anidadas pobladas (ej: `categoria: Categoria`).
   - Backend Python: `ArticuloRespuestaSchema`
   - Frontend TypeScript: `interface Articulo`

2. DTO de Creación (`POST`):
   - Exige únicamente los campos requeridos para insertar un nuevo registro. NO incluye `id`, `fechaCreacion` ni objetos anidados completos (usa sólo claves foráneas como `categoriaId` o listas de IDs `articulosRelacionadosIds`).
   - Backend Python: `ArticuloCrear`
   - Frontend TypeScript: `interface SolicitudCrearArticulo`

3. DTO de Edición / Actualización Parcial (`PUT` / `PATCH`):
   - Posee todos los campos opcionales (`?` en TS, `Optional` en Python) para permitir editar propiedades individuales sin obligar a reenviar todo el cuerpo técnico.
   - Backend Python: `ArticuloActualizar`
   - Frontend TypeScript: `interface SolicitudActualizarArticulo`

B. BENEFICIO EN EL DESARROLLO FRONTEND:
----------------------------------------
Tipar las solicitudes (`SolicitudCrear*`, `SolicitudActualizar*`) garantiza autocompletado perfecto y validación en tiempo de compilación. Si el desarrollador olvida un campo obligatorio antes de un `POST` o intenta enviar una propiedad no permitida, TypeScript marca el error inmediatamente en el editor antes de realizar la petición HTTP.

--------------------------------------------------------------------------------
9: ANATOMÍA Y ESTRUCTURA DE LA CAPA DE SERVICIOS API (`src/api/*.ts`)
--------------------------------------------------------------------------------

A. ESTRUCTURA INTERNA DE UN SERVICIO API:
------------------------------------------
Cada módulo de la aplicación posee su propio archivo de servicio (`authApi.ts`, `categoriaApi.ts`, `articuloApi.ts`, `reclamoApi.ts`). Todos consumen la misma instancia centralizada de `clienteAxios`.

Ejemplo de desglose línea por línea (`categoriaApi.ts`):

```typescript
import { clienteAxios } from './clienteAxios';
import type { Categoria, SolicitudCrearCategoria } from '../types/categoria';

export const categoriaApi = {
  // Petición GET con Query Parameter opcional (?soloActivas=true)
  async obtenerCategorias(soloActivas: boolean = false): Promise<Categoria[]> {
    const respuesta = await clienteAxios.get<Categoria[]>('/categorias', {
      params: { soloActivas }
    });
    return respuesta.data; // Retorna únicamente el cuerpo JSON de la respuesta
  },

  // Petición POST enviando cuerpo JSON tipado
  async crearCategoria(datos: SolicitudCrearCategoria): Promise<Categoria> {
    const respuesta = await clienteAxios.post<Categoria>('/categorias', datos);
    return respuesta.data;
  },

  // Petición PUT inyectando Path Parameter dinámico (/categorias/5)
  async actualizarCategoria(categoriaId: number, datos: SolicitudActualizarCategoria): Promise<Categoria> {
    const respuesta = await clienteAxios.put<Categoria>(`/categorias/${categoriaId}`, datos);
    return respuesta.data;
  }
};
```

B. SEGURIDAD RBAC: FRONTEND VS BACKEND
---------------------------------------
1. En el Backend (Seguridad Estricta / Garantía de Acceso):
   FastAPI intercepta el JWT Bearer Token y verifica mediante `Depends(requerirRoles([RolUsuario.ADMIN]))` si el usuario posee el rol requerido. Si no lo posee, la petición rebota con status HTTP 403 Forbidden.
2. En el Frontend (Experiencia de Usuario / UX):
   Los roles guardados en `usuario.rol` se utilizan en React únicamente para personalizar la interfaz visual (mostrar u ocultar botones de edición/creación). Aunque un usuario intente invocar la función de la API desde la consola del navegador, la seguridad del backend impedirá la operación.




