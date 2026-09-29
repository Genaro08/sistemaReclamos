from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.dependencias import obtenerSesionDb, obtenerUsuarioActual, requerirRoles
from app.models.usuarioModelo import RolUsuario, Usuario
from app.schemas.articuloSchema import (
    ArticuloActualizar,
    ArticuloBusquedaRespuesta,
    ArticuloCrear,
    ArticuloRespuestaSchema,
)
from app.schemas.plantillaSchema import (
    PlantillaActualizar,
    PlantillaCrear,
    PlantillaRespuestaSchema,
)
from app.services.articuloService import ArticuloService

articuloRouter = APIRouter(prefix="/articulos", tags=["Base de Conocimiento y Plantillas"])


@articuloRouter.get(
    "",
    response_model=List[ArticuloRespuestaSchema],
    status_code=status.HTTP_200_OK,
    summary="Listar artículos de conocimiento"
)
def listarArticulos(
    categoriaId: Optional[int] = Query(None, description="Filtrar por ID de categoría/concepto"),
    etiqueta: Optional[str] = Query(None, description="Filtrar por palabra clave/etiqueta"),
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Retorna la lista de desarrollos técnicos de conocimiento registrados.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.obtenerArticulos(categoriaId=categoriaId, etiqueta=etiqueta)


@articuloRouter.get(
    "/buscar",
    response_model=List[ArticuloBusquedaRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Buscar artículos por coincidencia de texto (% de similitud)"
)
def buscarArticulosPorCoincidencia(
    q: str = Query(..., min_length=3, description="Texto o consulta del problema para calcular % de coincidencia"),
    limite: int = Query(5, ge=1, le=20, description="Cantidad máxima de resultados a retornar"),
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Motor de Recomendaciones: Compara las palabras ingresadas contra los títulos y etiquetas
    de la base de datos y retorna los artículos ordenados por % de coincidencia.
    """
    servicio = ArticuloService(sesionDb)
    resultados = servicio.buscarArticulosPorTexto(textoBusqueda=q, limite=limite)

    respuesta = []
    for art, porcentaje in resultados:
        dto = ArticuloBusquedaRespuesta.model_validate(art)
        dto.porcentajeCoincidencia = porcentaje
        respuesta.append(dto)

    return respuesta


@articuloRouter.get(
    "/{articuloId}",
    response_model=ArticuloRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtener un artículo de conocimiento por su ID"
)
def obtenerArticulo(
    articuloId: int,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Retorna el detalle completo de un desarrollo técnico, incluyendo sus plantillas y artículos relacionados.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.obtenerArticuloPorId(articuloId)


@articuloRouter.post(
    "",
    response_model=ArticuloRespuestaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo artículo de conocimiento (requiere OPERATOR o ADMIN)"
)
def crearArticulo(
    datos: ArticuloCrear,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Permite a un técnico u operador redactar un nuevo desarrollo de conocimiento.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.crearArticulo(datos, autorId=usuarioActual.id)


@articuloRouter.put(
    "/{articuloId}",
    response_model=ArticuloRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un artículo de conocimiento existente (requiere OPERATOR o ADMIN)"
)
def actualizarArticulo(
    articuloId: int,
    datos: ArticuloActualizar,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Permite modificar el contenido técnico, etiquetas o artículos relacionados.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.actualizarArticulo(articuloId, datos)


# ==========================================
# ENDPOINTS PARA PLANTILLAS DE RESPUESTA
# ==========================================

@articuloRouter.post(
    "/{articuloId}/plantillas",
    response_model=PlantillaRespuestaSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar una plantilla de respuesta pública a un artículo"
)
def crearPlantilla(
    articuloId: int,
    datos: PlantillaCrear,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Agrega una plantilla de respuesta dirigida al usuario final asociada al artículo.
    """
    datos.articuloId = articuloId
    servicio = ArticuloService(sesionDb)
    return servicio.crearPlantilla(datos)


@articuloRouter.get(
    "/{articuloId}/plantillas",
    response_model=List[PlantillaRespuestaSchema],
    status_code=status.HTTP_200_OK,
    summary="Listar las plantillas de respuesta de un artículo"
)
def listarPlantillasPorArticulo(
    articuloId: int,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Retorna todas las plantillas de respuesta pública asociadas a un artículo de conocimiento.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.obtenerPlantillasPorArticulo(articuloId)


@articuloRouter.put(
    "/plantillas/{plantillaId}",
    response_model=PlantillaRespuestaSchema,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una plantilla de respuesta (requiere OPERATOR o ADMIN)"
)
def actualizarPlantilla(
    plantillaId: int,
    datos: PlantillaActualizar,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual: Usuario = Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Modifica el contenido o título de una plantilla de respuesta.
    """
    servicio = ArticuloService(sesionDb)
    return servicio.actualizarPlantilla(plantillaId, datos)
