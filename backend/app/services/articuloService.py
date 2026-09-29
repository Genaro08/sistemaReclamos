from typing import List, Optional, Tuple
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.excepciones import ExcepcionDominio
from app.models.articuloConocimientoModelo import ArticuloConocimiento
from app.models.categoriaModelo import Categoria
from app.models.plantillaRespuestaModelo import PlantillaRespuesta
from app.schemas.articuloSchema import ArticuloActualizar, ArticuloCrear
from app.schemas.plantillaSchema import PlantillaActualizar, PlantillaCrear


class ArticuloService:
    """
    Servicio de Lógica de Negocio para la Base de Conocimientos (Artículos Técnicos,
    Plantillas de Respuesta Pública y Motor de Búsqueda por % de coincidencia).
    """
    def __init__(self, sesionDb: Session):
        self.sesionDb = sesionDb

    def crearArticulo(self, datos: ArticuloCrear, autorId: int) -> ArticuloConocimiento:
        """
        Crea un nuevo desarrollo de conocimiento técnico.
        Verifica que la categoría exista y vincula artículos relacionados opcionales.
        """
        # Verificar existencia de la categoría
        categoria = self.sesionDb.get(Categoria, datos.categoriaId)
        if not categoria or not categoria.activa:
            raise ExcepcionDominio(
                mensaje=f"La categoría con ID {datos.categoriaId} no existe o está inactiva.",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        nuevoArticulo = ArticuloConocimiento(
            titulo=datos.titulo.strip(),
            resumen=datos.resumen.strip() if datos.resumen else None,
            contenidoTecnico=datos.contenidoTecnico.strip(),
            etiquetas=datos.etiquetas.lower().strip(),
            categoriaId=datos.categoriaId,
            autorId=autorId,
            vecesUtilizado=0
        )

        # Vincular artículos relacionados si se especificaron
        if datos.articulosRelacionadosIds:
            consultaRel = select(ArticuloConocimiento).where(
                ArticuloConocimiento.id.in_(datos.articulosRelacionadosIds)
            )
            relacionados = list(self.sesionDb.execute(consultaRel).scalars().all())
            nuevoArticulo.articulosRelacionados = relacionados

        self.sesionDb.add(nuevoArticulo)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevoArticulo)
        return nuevoArticulo

    def obtenerArticuloPorId(self, articuloId: int) -> ArticuloConocimiento:
        """
        Busca y retorna un artículo por su ID.
        Si no existe, lanza una ExcepcionDominio 404.
        """
        articulo = self.sesionDb.get(ArticuloConocimiento, articuloId)
        if not articulo:
            raise ExcepcionDominio(
                mensaje=f"No se encontró el artículo de conocimiento con ID {articuloId}.",
                codigoEstado=status.HTTP_404_NOT_FOUND
            )
        return articulo

    def obtenerArticulos(
        self,
        categoriaId: Optional[int] = None,
        etiqueta: Optional[str] = None
    ) -> List[ArticuloConocimiento]:
        """
        Retorna la lista de artículos de conocimiento.
        Permite filtrar por categoría o por una etiqueta/keyword específica.
        """
        consulta = select(ArticuloConocimiento)

        if categoriaId:
            consulta = consulta.where(ArticuloConocimiento.categoriaId == categoriaId)

        if etiqueta:
            consulta = consulta.where(ArticuloConocimiento.etiquetas.ilike(f"%{etiqueta.strip()}%"))

        consulta = consulta.order_by(ArticuloConocimiento.fechaCreacion.desc())
        return list(self.sesionDb.execute(consulta).scalars().all())

    def buscarArticulosPorTexto(
        self,
        textoBusqueda: str,
        limite: int = 5
    ) -> List[Tuple[ArticuloConocimiento, float]]:
        """
        Motor de Búsqueda por % de Coincidencia:
        Compara las palabras del texto de búsqueda contra el título y las etiquetas
        de los artículos de conocimiento y retorna una lista de tuplas:
        (ArticuloConocimiento, porcentajeCoincidencia) ordenada de mayor a menor.
        """
        if not textoBusqueda or len(textoBusqueda.strip()) < 3:
            return []

        # Limpiar y separar palabras de búsqueda (ignorando palabras muy cortas)
        palabrasBusqueda = set(
            w.lower().strip() for w in textoBusqueda.split() if len(w.strip()) > 2
        )
        if not palabrasBusqueda:
            return []

        todosArticulos = self.sesionDb.execute(select(ArticuloConocimiento)).scalars().all()
        resultados: List[Tuple[ArticuloConocimiento, float]] = []

        for art in todosArticulos:
            # Extraer palabras del título y de las etiquetas del artículo
            palabrasArticulo = set(
                w.lower().strip().strip(",")
                for w in (art.titulo + " " + art.etiquetas).split()
                if len(w.strip().strip(",")) > 2
            )

            # Calcular coincidencia de intersección
            coincidencias = palabrasBusqueda.intersection(palabrasArticulo)
            if coincidencias:
                porcentaje = round((len(coincidencias) / len(palabrasBusqueda)) * 100.0, 2)
                # Cap a 100.0%
                porcentaje = min(porcentaje, 100.0)
                resultados.append((art, porcentaje))

        # Ordenar resultados de mayor a menor porcentaje
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados[:limite]

    def actualizarArticulo(self, articuloId: int, datos: ArticuloActualizar) -> ArticuloConocimiento:
        """
        Actualiza los campos o relaciones de un artículo existente.
        """
        articulo = self.obtenerArticuloPorId(articuloId)

        if datos.titulo is not None:
            articulo.titulo = datos.titulo.strip()
        if datos.resumen is not None:
            articulo.resumen = datos.resumen.strip() if datos.resumen else None
        if datos.contenidoTecnico is not None:
            articulo.contenidoTecnico = datos.contenidoTecnico.strip()
        if datos.etiquetas is not None:
            articulo.etiquetas = datos.etiquetas.lower().strip()
        if datos.categoriaId is not None:
            categoria = self.sesionDb.get(Categoria, datos.categoriaId)
            if not categoria or not categoria.activa:
                raise ExcepcionDominio(
                    mensaje=f"La categoría con ID {datos.categoriaId} no existe o está inactiva.",
                    codigoEstado=status.HTTP_400_BAD_REQUEST
                )
            articulo.categoriaId = datos.categoriaId

        if datos.articulosRelacionadosIds is not None:
            consultaRel = select(ArticuloConocimiento).where(
                ArticuloConocimiento.id.in_(datos.articulosRelacionadosIds)
            )
            relacionados = list(self.sesionDb.execute(consultaRel).scalars().all())
            articulo.articulosRelacionados = relacionados

        self.sesionDb.commit()
        self.sesionDb.refresh(articulo)
        return articulo

    def incrementarContadorUso(self, articuloId: int) -> ArticuloConocimiento:
        """
        Incrementa en +1 el contador vecesUtilizado de un artículo cuando resuelve un ticket.
        """
        articulo = self.obtenerArticuloPorId(articuloId)
        articulo.vecesUtilizado += 1
        self.sesionDb.commit()
        self.sesionDb.refresh(articulo)
        return articulo

    # ==========================================
    # LÓGICA PARA PLANTILLAS DE RESPUESTA
    # ==========================================

    def crearPlantilla(self, datos: PlantillaCrear) -> PlantillaRespuesta:
        """
        Crea una plantilla de respuesta pública asociada a un artículo.
        """
        articulo = self.obtenerArticuloPorId(datos.articuloId)

        nuevaPlantilla = PlantillaRespuesta(
            articuloId=articulo.id,
            titulo=datos.titulo.strip(),
            contenidoUsuario=datos.contenidoUsuario.strip()
        )
        self.sesionDb.add(nuevaPlantilla)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevaPlantilla)
        return nuevaPlantilla

    def obtenerPlantillasPorArticulo(self, articuloId: int) -> List[PlantillaRespuesta]:
        """
        Retorna todas las plantillas de respuesta pública pertenecientes a un artículo.
        """
        self.obtenerArticuloPorId(articuloId)  # Valida existencia
        consulta = select(PlantillaRespuesta).where(PlantillaRespuesta.articuloId == articuloId)
        return list(self.sesionDb.execute(consulta).scalars().all())

    def actualizarPlantilla(self, plantillaId: int, datos: PlantillaActualizar) -> PlantillaRespuesta:
        """
        Actualiza el contenido o título de una plantilla existente.
        """
        plantilla = self.sesionDb.get(PlantillaRespuesta, plantillaId)
        if not plantilla:
            raise ExcepcionDominio(
                mensaje=f"No se encontró la plantilla de respuesta con ID {plantillaId}.",
                codigoEstado=status.HTTP_404_NOT_FOUND
            )

        if datos.titulo is not None:
            plantilla.titulo = datos.titulo.strip()
        if datos.contenidoUsuario is not None:
            plantilla.contenidoUsuario = datos.contenidoUsuario.strip()

        self.sesionDb.commit()
        self.sesionDb.refresh(plantilla)
        return plantilla
