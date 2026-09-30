from datetime import datetime, timezone
from typing import List, Optional
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.excepciones import ExcepcionDominio
from app.models.articuloConocimientoModelo import ArticuloConocimiento
from app.models.categoriaModelo import Categoria
from app.models.comentarioModelo import Comentario
from app.models.historialReclamoModelo import HistorialReclamo
from app.models.plantillaRespuestaModelo import PlantillaRespuesta
from app.models.reclamoModelo import EstadoReclamo, PrioridadReclamo, Reclamo
from app.models.usuarioModelo import RolUsuario, Usuario
from app.schemas.reclamoSchema import (
    ReclamoAsignarResponsable,
    ReclamoCambiarEstado,
    ReclamoCrear,
)
from app.services.articuloService import ArticuloService


class ReclamoService:
    """
    Servicio de Lógica de Negocio para el ciclo de vida de Reclamos,
    Comentarios (interacciones públicas y notas internas) y Registro de Auditoría (Historial).
    """
    def __init__(self, sesionDb: Session):
        self.sesionDb = sesionDb

    def crearReclamo(self, datos: ReclamoCrear, creadorId: int) -> Reclamo:
        """
        Crea un nuevo ticket de reclamo.
        1. Verifica que la categoría seleccionada exista y esté activa.
        2. Ejecuta el algoritmo de % de coincidencia automática contra la Base de Conocimiento.
        3. Registra la creación en el Historial de Auditoría.
        """
        categoria = self.sesionDb.get(Categoria, datos.categoriaId)
        if not categoria or not categoria.activa:
            raise ExcepcionDominio(
                mensaje=f"La categoría con ID {datos.categoriaId} no existe o está inactiva.",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        nuevoReclamo = Reclamo(
            titulo=datos.titulo.strip(),
            descripcion=datos.descripcion.strip(),
            prioridad=datos.prioridad,
            estado=EstadoReclamo.PENDING,
            categoriaId=datos.categoriaId,
            creadorId=creadorId,
        )

        # Calcular % de coincidencia automática con la Base de Conocimientos
        articuloService = ArticuloService(self.sesionDb)
        textoCoincidencia = f"{datos.titulo} {datos.descripcion}"
        coincidencias = articuloService.buscarArticulosPorTexto(textoBusqueda=textoCoincidencia, limite=1)
        if coincidencias:
            _, porcentajeTop = coincidencias[0]
            nuevoReclamo.porcentajeCoincidenciaAuto = porcentajeTop

        self.sesionDb.add(nuevoReclamo)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevoReclamo)

        # Registrar evento inicial en el Historial
        self._registrarHistorial(
            reclamoId=nuevoReclamo.id,
            usuarioId=creadorId,
            accion="Creación del ticket de reclamo"
        )

        return nuevoReclamo

    def obtenerReclamoPorId(self, reclamoId: int, usuarioActual: Usuario) -> Reclamo:
        """
        Busca un reclamo por su ID.
        Los usuarios comunes (USER) solo pueden ver sus propios reclamos.
        Técnicos (OPERATOR) y Administradores (ADMIN) pueden ver cualquier reclamo.
        """
        reclamo = self.sesionDb.get(Reclamo, reclamoId)
        if not reclamo:
            raise ExcepcionDominio(
                mensaje=f"No se encontró el reclamo con ID {reclamoId}.",
                codigoEstado=status.HTTP_404_NOT_FOUND
            )

        if usuarioActual.rol == RolUsuario.USER and reclamo.creadorId != usuarioActual.id:
            raise ExcepcionDominio(
                mensaje="No tiene permisos para acceder a este reclamo.",
                codigoEstado=status.HTTP_403_FORBIDDEN
            )

        return reclamo

    def listarReclamos(
        self,
        usuarioActual: Usuario,
        estado: Optional[EstadoReclamo] = None,
        prioridad: Optional[PrioridadReclamo] = None,
        categoriaId: Optional[int] = None
    ) -> List[Reclamo]:
        """
        Lista los reclamos registrados.
        Si el usuario tiene rol USER, solo se retornan sus propios reclamos.
        Si es OPERATOR o ADMIN, se retornan todos con posibilidad de filtros.
        """
        consulta = select(Reclamo)

        if usuarioActual.rol == RolUsuario.USER:
            consulta = consulta.where(Reclamo.creadorId == usuarioActual.id)

        if estado:
            consulta = consulta.where(Reclamo.estado == estado)

        if prioridad:
            consulta = consulta.where(Reclamo.prioridad == prioridad)

        if categoriaId:
            consulta = consulta.where(Reclamo.categoriaId == categoriaId)

        consulta = consulta.order_by(Reclamo.fechaCreacion.desc())
        return list(self.sesionDb.execute(consulta).scalars().all())

    def asignarResponsable(
        self,
        reclamoId: int,
        datos: ReclamoAsignarResponsable,
        usuarioActual: Usuario
    ) -> Reclamo:
        """
        Asigna o reasigna un técnico/operador responsable al ticket (requiere OPERATOR o ADMIN).
        Si el estado actual era PENDING, cambia automáticamente a IN_PROGRESS.
        """
        reclamo = self.obtenerReclamoPorId(reclamoId, usuarioActual)

        responsable = self.sesionDb.get(Usuario, datos.responsableId)
        if not responsable or responsable.rol == RolUsuario.USER:
            raise ExcepcionDominio(
                mensaje=f"El usuario asignado (ID {datos.responsableId}) no existe o no posee rol técnico.",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        reclamo.responsableId = datos.responsableId
        if reclamo.estado == EstadoReclamo.PENDING:
            reclamo.estado = EstadoReclamo.IN_PROGRESS

        self.sesionDb.commit()
        self.sesionDb.refresh(reclamo)

        self._registrarHistorial(
            reclamoId=reclamo.id,
            usuarioId=usuarioActual.id,
            accion=f"Asignado técnico responsable {responsable.nombre} {responsable.apellido} (ID {responsable.id})"
        )

        return reclamo

    def cambiarEstado(
        self,
        reclamoId: int,
        datos: ReclamoCambiarEstado,
        usuarioActual: Usuario
    ) -> Reclamo:
        """
        Modifica el estado del ticket y vincula opcionalmente artículos o plantillas de respuesta.
        Gestiona las estampas de tiempo fechaResolucion y fechaCierre.
        """
        reclamo = self.obtenerReclamoPorId(reclamoId, usuarioActual)

        estadoAnterior = reclamo.estado
        reclamo.estado = datos.estado

        # Manejo de artículos y plantillas asociadas a la solución
        if datos.articuloAplicadoId is not None:
            articulo = self.sesionDb.get(ArticuloConocimiento, datos.articuloAplicadoId)
            if not articulo:
                raise ExcepcionDominio(
                    mensaje=f"El artículo de conocimiento con ID {datos.articuloAplicadoId} no existe.",
                    codigoEstado=status.HTTP_400_BAD_REQUEST
                )
            reclamo.articuloAplicadoId = datos.articuloAplicadoId
            articulo.vecesUtilizado += 1

        if datos.plantillaAplicadaId is not None:
            plantilla = self.sesionDb.get(PlantillaRespuesta, datos.plantillaAplicadaId)
            if not plantilla:
                raise ExcepcionDominio(
                    mensaje=f"La plantilla de respuesta con ID {datos.plantillaAplicadaId} no existe.",
                    codigoEstado=status.HTTP_400_BAD_REQUEST
                )
            reclamo.plantillaAplicadaId = datos.plantillaAplicadaId

        # Marcar timestamps de resolución y cierre
        ahora = datetime.now(timezone.utc)
        if datos.estado == EstadoReclamo.RESOLVED and not reclamo.fechaResolucion:
            reclamo.fechaResolucion = ahora
        elif datos.estado == EstadoReclamo.CLOSED and not reclamo.fechaCierre:
            reclamo.fechaCierre = ahora
            if not reclamo.fechaResolucion:
                reclamo.fechaResolucion = ahora

        self.sesionDb.commit()
        self.sesionDb.refresh(reclamo)

        self._registrarHistorial(
            reclamoId=reclamo.id,
            usuarioId=usuarioActual.id,
            accion=f"Cambio de estado: {estadoAnterior.value} -> {datos.estado.value}"
        )

        return reclamo

    # ==========================================
    # LÓGICA DE COMENTARIOS (NOTAS PÚBLICAS / INTERNAS)
    # ==========================================

    def agregarComentario(
        self,
        reclamoId: int,
        contenido: str,
        esInternoTecnico: bool,
        usuarioActual: Usuario
    ) -> Comentario:
        """
        Agrega un mensaje al ticket.
        Si esInternoTecnico es True, valida que el usuario sea OPERATOR o ADMIN (nota interna).
        """
        reclamo = self.obtenerReclamoPorId(reclamoId, usuarioActual)

        if esInternoTecnico and usuarioActual.rol == RolUsuario.USER:
            raise ExcepcionDominio(
                mensaje="Los usuarios comunes no pueden agregar notas internas privadas.",
                codigoEstado=status.HTTP_403_FORBIDDEN
            )

        nuevoComentario = Comentario(
            reclamoId=reclamo.id,
            usuarioId=usuarioActual.id,
            contenido=contenido.strip(),
            esInternoTecnico=esInternoTecnico
        )

        self.sesionDb.add(nuevoComentario)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevoComentario)

        tipoComentario = "nota interna técnica" if esInternoTecnico else "comentario público"
        self._registrarHistorial(
            reclamoId=reclamo.id,
            usuarioId=usuarioActual.id,
            accion=f"Agregó {tipoComentario}"
        )

        return nuevoComentario

    def obtenerComentariosPorReclamo(
        self,
        reclamoId: int,
        usuarioActual: Usuario
    ) -> List[Comentario]:
        """
        Retorna la conversación del reclamo.
        Si el usuario es USER, se filtran y ocultan las notas internas de técnicos.
        """
        reclamo = self.obtenerReclamoPorId(reclamoId, usuarioActual)

        consulta = select(Comentario).where(Comentario.reclamoId == reclamo.id)

        # Ocultar notas internas al usuario final
        if usuarioActual.rol == RolUsuario.USER:
            consulta = consulta.where(Comentario.esInternoTecnico == False)

        consulta = consulta.order_by(Comentario.fechaCreacion.asc())
        return list(self.sesionDb.execute(consulta).scalars().all())

    # ==========================================
    # HISTORIAL DE AUDITORÍA
    # ==========================================

    def obtenerHistorialPorReclamo(
        self,
        reclamoId: int,
        usuarioActual: Usuario
    ) -> List[HistorialReclamo]:
        """
        Retorna el registro de auditoría completo del ticket.
        Solo accesible por OPERATOR o ADMIN (o el creador).
        """
        reclamo = self.obtenerReclamoPorId(reclamoId, usuarioActual)
        consulta = select(HistorialReclamo).where(
            HistorialReclamo.reclamoId == reclamo.id
        ).order_by(HistorialReclamo.fecha.asc())

        return list(self.sesionDb.execute(consulta).scalars().all())

    def _registrarHistorial(self, reclamoId: int, usuarioId: int, accion: str) -> None:
        """Helper privado para insertar eventos en el HistorialReclamo."""
        entrada = HistorialReclamo(
            reclamoId=reclamoId,
            usuarioId=usuarioId,
            accion=accion
        )
        self.sesionDb.add(entrada)
        self.sesionDb.commit()
