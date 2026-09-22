from fastapi import Request, status
from fastapi.responses import JSONResponse


class ExcepcionDominio(Exception):
    """
    Excepción base para errores de lógica de negocio o dominio.
    """
    def __init__(self, mensaje: str, codigoEstado: int = status.HTTP_400_BAD_REQUEST):
        self.mensaje = mensaje
        self.codigoEstado = codigoEstado
        super().__init__(mensaje)


async def manejadorExcepcionDominio(request: Request, exc: ExcepcionDominio) -> JSONResponse:
    """
    Manejador global de FastAPI para capturar excepciones de dominio
    y retornar respuestas JSON estandarizadas en camelCase.
    """
    return JSONResponse(
        status_code=exc.codigoEstado,
        content={
            "exito": False,
            "error": exc.mensaje
        }
    )
