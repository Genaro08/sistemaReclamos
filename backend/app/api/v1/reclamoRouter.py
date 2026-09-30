from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.dependencias import obtenerSesionDb, obtenerUsuarioActual, requerirRoles
from app.models.reclamoModelo import EstadoReclamo, PrioridadReclamo
from app.models.usuarioModelo import RolUsuario, Usuario
from app.schemas.comentarioSchema import ComentarioCrear, ComentarioRespuestaSchema
from app.schemas.historialSchema import HistorialRespuestaSchema
from app.schemas.reclamoSchema import (
    ReclamoAsignarResponsable,
    ReclamoCambiarEstado,
    ReclamoCrear,
    ReclamoRespuestaSchema,
)
from app.services.reclamoService import ReclamoService

reclamoRouter = APIRouter(prefix="/reclamos", tags=["Reclamos, Interacciones y Auditoría"])


@reclamoRouter.post(
    "",
    response_model=ReclamoRespuestaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo reclamo/ticket"
)
def crearReclamo(
    datos: ReclamoCrear,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Permite a cualquier usuario autenticado registrar un nuevo ticket de reclamo.
    Calcula de forma automática el % de coincidencia con la Base de Conocimiento.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.crearReclamo(datos, creadorId=usuarioActual.id)


@reclamoRouter.get(
    "",
    response_model=List[ReclamoRespuestaSchema],
    status_code=status.HTTP_200_OK,
    summary="Listar reclamos (con filtros por estado, prioridad y categoría)"
)
def listarReclamos(
    estado: Optional[EstadoReclamo] = Query(None, description="Filtrar por estado del ticket"),
    prioridad: Optional[PrioridadReclamo] = Query(None, description="Filtrar por prioridad"),
    categoriaId: Optional[int] = Query(None, description="Filtrar por categoría"),
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Retorna los reclamos. Si el usuario es de rol USER, solo se retornan sus propios reclamos.
    Si es OPERATOR o ADMIN, se pueden listar todos los reclamos con opciones de filtro.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.listarReclamos(
        usuarioActual=usuarioActual,
        estado=estado,
        prioridad=prioridad,
        categoriaId=categoriaId
    )


@reclamoRouter.get(
    "/{reclamoId}",
    response_model=ReclamoRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtener el detalle de un reclamo por ID"
)
def obtenerReclamo(
    reclamoId: int,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Retorna el detalle completo de un reclamo por su ID.
    Un usuario final solo puede consultar reclamos creados por él mismo.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.obtenerReclamoPorId(reclamoId, usuarioActual=usuarioActual)


@reclamoRouter.put(
    "/{reclamoId}/asignar",
    response_model=ReclamoRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Asignar un técnico responsable al reclamo (requiere OPERATOR o ADMIN)"
)
def asignarResponsable(
    reclamoId: int,
    datos: ReclamoAsignarResponsable,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Asigna un técnico u operador como responsable del ticket. Si estaba PENDING pasa a IN_PROGRESS.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.asignarResponsable(reclamoId, datos, usuarioActual=usuarioActual)


@reclamoRouter.put(
    "/{reclamoId}/estado",
    response_model=ReclamoRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Cambiar el estado del reclamo (requiere OPERATOR o ADMIN)"
)
def cambiarEstado(
    reclamoId: int,
    datos: ReclamoCambiarEstado,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Permite modificar el estado (ej: RESOLVED, CLOSED) y vincular la solución aplicada.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.cambiarEstado(reclamoId, datos, usuarioActual=usuarioActual)


# ==========================================
# ENDPOINTS PARA COMENTARIOS E INTERACCIONES
# ==========================================

@reclamoRouter.post(
    "/{reclamoId}/comentarios",
    response_model=ComentarioRespuestaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar un comentario público o nota interna al reclamo"
)
def agregarComentario(
    reclamoId: int,
    datos: ComentarioCrear,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Agrega una interacción al ticket. Las notas internas solo pueden ser creadas por técnicos.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.agregarComentario(
        reclamoId=reclamoId,
        contenido=datos.contenido,
        esInternoTecnico=datos.esInternoTecnico,
        usuarioActual=usuarioActual
    )


@reclamoRouter.get(
    "/{reclamoId}/comentarios",
    response_model=List[ComentarioRespuestaSchema],
    status_code=status.HTTP_200_OK,
    summary="Listar comentarios/interacciones de un reclamo"
)
def listarComentarios(
    reclamoId: int,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Retorna el hilo de conversación del ticket. Las notas internas privadas se ocultan al usuario final.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.obtenerComentariosPorReclamo(reclamoId=reclamoId, usuarioActual=usuarioActual)


# ==========================================
# ENDPOINTS PARA HISTORIAL DE AUDITORÍA
# ==========================================

@reclamoRouter.get(
    "/{reclamoId}/historial",
    response_model=List[HistorialRespuestaSchema],
    status_code=status.HTTP_200_OK,
    summary="Consultar historial de auditoría del reclamo"
)
def obtenerHistorial(
    reclamoId: int,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Retorna el registro cronológico de eventos y auditoría del reclamo.
    """
    servicio = ReclamoService(sesionDb)
    return servicio.obtenerHistorialPorReclamo(reclamoId=reclamoId, usuarioActual=usuarioActual)
