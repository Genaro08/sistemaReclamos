from typing import List, Optional
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.excepciones import ExcepcionDominio
from app.models.categoriaModelo import Categoria
from app.schemas.categoriaSchema import CategoriaActualizar, CategoriaCrear


class CategoriaService:
    """
    Servicio de Lógica de Negocio para la gestión de Categorías / Conceptos.
    Aísla las operaciones de base de datos y validaciones de dominio de los controladores HTTP.
    """
    def __init__(self, sesionDb: Session):
        self.sesionDb = sesionDb

    def crearCategoria(self, datos: CategoriaCrear) -> Categoria:
        """
        Valida que el nombre de la categoría no esté registrado previamente
        y crea una nueva entrada en la base de datos.
        """
        nombreLimpio = datos.nombre.strip()

        # Verificar duplicados (insensible a mayúsculas/minúsculas)
        consulta = select(Categoria).where(Categoria.nombre.ilike(nombreLimpio))
        existente = self.sesionDb.execute(consulta).scalar_one_or_none()

        if existente:
            raise ExcepcionDominio(
                mensaje=f"Ya existe una categoría registrada con el nombre '{nombreLimpio}'.",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        nuevaCategoria = Categoria(
            nombre=nombreLimpio,
            descripcion=datos.descripcion.strip() if datos.descripcion else None,
            activa=True
        )
        self.sesionDb.add(nuevaCategoria)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevaCategoria)
        return nuevaCategoria

    def obtenerCategorias(self, soloActivas: bool = False) -> List[Categoria]:
        """
        Retorna el listado completo de categorías.
        Si soloActivas es True, filtra únicamente las categorías habilitadas.
        """
        consulta = select(Categoria)
        if soloActivas:
            consulta = consulta.where(Categoria.activa == True)

        consulta = consulta.order_by(Categoria.nombre.asc())
        return list(self.sesionDb.execute(consulta).scalars().all())

    def obtenerCategoriaPorId(self, categoriaId: int) -> Categoria:
        """
        Busca y retorna una categoría por su ID.
        Si no existe, lanza una ExcepcionDominio con código HTTP 404.
        """
        categoria = self.sesionDb.get(Categoria, categoriaId)
        if not categoria:
            raise ExcepcionDominio(
                mensaje=f"No se encontró la categoría con ID {categoriaId}.",
                codigoEstado=status.HTTP_404_NOT_FOUND
            )
        return categoria

    def actualizarCategoria(self, categoriaId: int, datos: CategoriaActualizar) -> Categoria:
        """
        Actualiza parcialmente los campos de una categoría existente.
        Verifica que el nuevo nombre no colisione con otra categoría registrada.
        """
        categoria = self.obtenerCategoriaPorId(categoriaId)

        if datos.nombre is not None:
            nombreLimpio = datos.nombre.strip()
            # Verificar que no colisione con otra categoría existente diferente a la actual
            consulta = select(Categoria).where(
                Categoria.nombre.ilike(nombreLimpio),
                Categoria.id != categoriaId
            )
            colision = self.sesionDb.execute(consulta).scalar_one_or_none()
            if colision:
                raise ExcepcionDominio(
                    mensaje=f"Ya existe otra categoría registrada con el nombre '{nombreLimpio}'.",
                    codigoEstado=status.HTTP_400_BAD_REQUEST
                )
            categoria.nombre = nombreLimpio

        if datos.descripcion is not None:
            categoria.descripcion = datos.descripcion.strip() if datos.descripcion else None

        if datos.activa is not None:
            categoria.activa = datos.activa

        self.sesionDb.commit()
        self.sesionDb.refresh(categoria)
        return categoria
