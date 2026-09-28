from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.dependencias import obtenerSesionDb, requerirRoles
from app.models.usuarioModelo import RolUsuario
from app.schemas.categoriaSchema import CategoriaActualizar, CategoriaCrear, CategoriaRespuesta
from app.services.categoriaService import CategoriaService

categoriaRouter = APIRouter(prefix="/categorias", tags=["Categorías y Conceptos"])


@categoriaRouter.get(
    "",
    response_model=List[CategoriaRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las categorías/conceptos"
)
def listarCategorias(
    soloActivas: bool = Query(False, description="Si es True, retorna únicamente las categorías habilitadas"),
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Retorna la lista completa de categorías registradas en el sistema.
    Acceso público para usuarios autenticados.
    """
    servicio = CategoriaService(sesionDb)
    return servicio.obtenerCategorias(soloActivas=soloActivas)


@categoriaRouter.get(
    "/{categoriaId}",
    response_model=CategoriaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener una categoría por su ID"
)
def obtenerCategoria(
    categoriaId: int,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Retorna el detalle de una categoría específica.
    """
    servicio = CategoriaService(sesionDb)
    return servicio.obtenerCategoriaPorId(categoriaId)


@categoriaRouter.post(
    "",
    response_model=CategoriaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría (requiere rol OPERATOR o ADMIN)"
)
def crearCategoria(
    datos: CategoriaCrear,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual=Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Permite registrar una nueva categoría en el sistema.
    Protegido para operadores y administradores.
    """
    servicio = CategoriaService(sesionDb)
    return servicio.crearCategoria(datos)


@categoriaRouter.put(
    "/{categoriaId}",
    response_model=CategoriaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una categoría existente (requiere rol OPERATOR o ADMIN)"
)
def actualizarCategoria(
    categoriaId: int,
    datos: CategoriaActualizar,
    sesionDb: Session = Depends(obtenerSesionDb),
    usuarioActual=Depends(requerirRoles([RolUsuario.ADMIN, RolUsuario.OPERATOR]))
):
    """
    Permite modificar los datos o habilitar/deshabilitar una categoría existente.
    Protegido para operadores y administradores.
    """
    servicio = CategoriaService(sesionDb)
    return servicio.actualizarCategoria(categoriaId, datos)
