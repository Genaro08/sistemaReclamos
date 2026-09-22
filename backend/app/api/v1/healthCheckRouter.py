from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.sesion import obtenerSesionDb

healthCheckRouter = APIRouter(prefix="/health", tags=["Salud del Sistema"])


@healthCheckRouter.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Verificar la salud de la API y la conexión a la base de datos"
)
def verificarSaludSistema(sesionDb: Session = Depends(obtenerSesionDb)):
    """
    Comprueba que el servicio FastAPI y la conexión relacional a PostgreSQL
    (Supabase o Local) respondan correctamente.
    """
    estadoDb = False
    mensajeDb = "Sin conexión"

    try:
        # Consulta rápida de prueba a PostgreSQL
        resultado = sesionDb.execute(text("SELECT 1")).scalar()
        if resultado == 1:
            estadoDb = True
            mensajeDb = "Conexión a PostgreSQL exitosa"
    except Exception as error:
        mensajeDb = f"Error al conectar con la base de datos: {str(error)}"

    return {
        "estado": "ok",
        "baseDeDatos": {
            "conectado": estadoDb,
            "mensaje": mensajeDb
        }
    }
