from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.configuracion import configuracion
from app.core.excepciones import ExcepcionDominio, manejadorExcepcionDominio
from app.api.v1.healthCheckRouter import healthCheckRouter
from app.api.v1.authRouter import authRouter

# Instancia principal de FastAPI
app = FastAPI(
    title=configuracion.proyectoNombre,
    openapi_url=f"{configuracion.apiV1Str}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejador global de excepciones de dominio
app.add_exception_handler(ExcepcionDominio, manejadorExcepcionDominio)

# Registrar routers de la API v1
app.include_router(healthCheckRouter, prefix=configuracion.apiV1Str)
app.include_router(authRouter, prefix=configuracion.apiV1Str)


@app.get("/", summary="Ruta raíz de la API")
def rutaRaiz():
    return {
        "mensaje": f"Bienvenido a la API del {configuracion.proyectoNombre}",
        "documentacion": "/docs",
        "salud": f"{configuracion.apiV1Str}/health"
    }
