\# Sistema de gestión de reclamos internos



Aplicación web full stack para gestionar solicitudes y reclamos internos de una organización, desde su creación hasta su resolución y cierre.



\## Objetivo



El proyecto busca resolver un problema habitual en organizaciones donde las solicitudes se reciben por distintos medios (correo, mensajería o comunicación directa) y resulta difícil realizar su seguimiento.



El sistema permite registrar cada solicitud, asignarla a un responsable, establecer prioridades, realizar seguimiento de su estado y conservar un historial de las acciones realizadas.



El objetivo del proyecto es desarrollar una solución completa, mantenible y cercana a un escenario de trabajo real.



\## Stack tecnológico



\### Frontend



\* React

\* TypeScript

\* Vite



\### Backend



\* Python

\* FastAPI

\* Pydantic

\* SQLAlchemy

\* Alembic



\### Base de datos



\* PostgreSQL



\### API y seguridad



\* REST API

\* OpenAPI / Swagger

\* JWT

\* Control de acceso por roles



\### Testing



\* Pytest

\* Tests de frontend



\### Infraestructura



\* Docker

\* Docker Compose



\## Funcionalidades



\### Usuarios y autenticación



\* Registro e inicio de sesión

\* Autenticación mediante JWT

\* Roles y permisos

\* Gestión de usuarios



\### Reclamos



\* Crear reclamos

\* Consultar reclamos

\* Editar información

\* Asignar responsables

\* Cambiar estado

\* Definir prioridad

\* Clasificar por categoría

\* Agregar comentarios

\* Adjuntar archivos

\* Consultar historial



\### Seguimiento



\* Historial de cambios

\* Fechas de creación, asignación y resolución

\* Identificación del responsable

\* Control de solicitudes pendientes y vencidas



\### Dashboard



\* Cantidad de reclamos por estado

\* Cantidad por prioridad

\* Cantidad por categoría

\* Reclamos pendientes

\* Reclamos vencidos

\* Tiempo promedio de resolución



\### Búsqueda y filtros



\* Búsqueda por texto

\* Filtro por estado

\* Filtro por prioridad

\* Filtro por categoría

\* Filtro por responsable

\* Paginación



\## Arquitectura



La aplicación estará dividida en dos componentes principales:



```text

React

&#x20; │

&#x20; │ HTTP / REST

&#x20; ▼

FastAPI

&#x20; │

&#x20; ├── Lógica de negocio

&#x20; ├── Autenticación y autorización

&#x20; ├── Validaciones

&#x20; └── Acceso a datos

&#x20;      │

&#x20;      ▼

&#x20;  PostgreSQL

```



El backend seguirá una estructura modular, separando responsabilidades entre API, lógica de negocio, acceso a datos, modelos, esquemas, seguridad y manejo de errores.



\## Estado del proyecto



\* [x] Definición inicial



\* [x] Configuración del backend



\* [x] Configuración de PostgreSQL (Supabase / Local)



\* \[ ] Modelado de datos



\* \[ ] Autenticación y autorización



\* \[ ] Gestión de usuarios

\* \[ ] Gestión de reclamos

\* \[ ] Comentarios e historial

\* \[ ] Adjuntos

\* \[ ] Búsqueda y filtros

\* \[ ] Dashboard

\* \[ ] Frontend

\* \[ ] Testing

\* \[ ] Dockerización

\* \[ ] Deploy

\* \[ ] Documentación final



\## Objetivo del portfolio



El proyecto busca demostrar experiencia práctica en:



\* Desarrollo full stack

\* Diseño y desarrollo de APIs REST

\* Desarrollo backend con Python

\* Desarrollo frontend con React

\* Diseño de bases de datos relacionales

\* Autenticación y autorización

\* Validación y manejo de errores

\* Testing

\* Git y buenas prácticas de desarrollo

\* Despliegue de aplicaciones

\* Resolución de problemas y diseño de soluciones



\## Estado



Proyecto en desarrollo.



