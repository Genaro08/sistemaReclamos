import { clienteAxios } from './clienteAxios';
import type {
  Comentario,
  EstadoReclamo,
  HistorialReclamo,
  PrioridadReclamo,
  Reclamo,
  SolicitudAsignarResponsable,
  SolicitudCambiarEstadoReclamo,
  SolicitudCrearComentario,
  SolicitudCrearReclamo,
} from '../types/reclamo';

export const reclamoApi = {
  /**
   * Crea un nuevo ticket de reclamo.
   * El backend calcula automáticamente el % de coincidencia con la Base de Conocimiento.
   */
  async crearReclamo(datos: SolicitudCrearReclamo): Promise<Reclamo> {
    const respuesta = await clienteAxios.post<Reclamo>('/reclamos', datos);
    return respuesta.data;
  },

  /**
   * Obtiene la lista de reclamos.
   * Filtra por estado, prioridad o categoría. Los usuarios comunes solo ven sus propios tickets.
   */
  async obtenerReclamos(
    estado?: EstadoReclamo,
    prioridad?: PrioridadReclamo,
    categoriaId?: number
  ): Promise<Reclamo[]> {
    const respuesta = await clienteAxios.get<Reclamo[]>('/reclamos', {
      params: { estado, prioridad, categoriaId }
    });
    return respuesta.data;
  },

  /**
   * Obtiene el detalle completo de un reclamo por su ID.
   */
  async obtenerReclamoPorId(reclamoId: number): Promise<Reclamo> {
    const respuesta = await clienteAxios.get<Reclamo>(`/reclamos/${reclamoId}`);
    return respuesta.data;
  },

  /**
   * Asigna o reasigna un técnico responsable a un ticket (requiere OPERATOR o ADMIN).
   */
  async asignarResponsable(reclamoId: number, datos: SolicitudAsignarResponsable): Promise<Reclamo> {
    const respuesta = await clienteAxios.put<Reclamo>(`/reclamos/${reclamoId}/asignar`, datos);
    return respuesta.data;
  },

  /**
   * Cambia el estado del reclamo y vincula opcionalmente artículos o plantillas aplicadas.
   */
  async cambiarEstado(reclamoId: number, datos: SolicitudCambiarEstadoReclamo): Promise<Reclamo> {
    const respuesta = await clienteAxios.put<Reclamo>(`/reclamos/${reclamoId}/estado`, datos);
    return respuesta.data;
  },

  // ==========================================
  // HILO DE COMENTARIOS E INTERACCIONES
  // ==========================================

  /**
   * Agrega un comentario público o una nota técnica privada (exclusiva de operadores).
   */
  async agregarComentario(reclamoId: number, datos: SolicitudCrearComentario): Promise<Comentario> {
    const respuesta = await clienteAxios.post<Comentario>(`/reclamos/${reclamoId}/comentarios`, datos);
    return respuesta.data;
  },

  /**
   * Lista los comentarios de un ticket. Oculta automáticamente las notas privadas si el usuario es USER.
   */
  async obtenerComentarios(reclamoId: number): Promise<Comentario[]> {
    const respuesta = await clienteAxios.get<Comentario[]>(`/reclamos/${reclamoId}/comentarios`);
    return respuesta.data;
  },

  // ==========================================
  // HISTORIAL DE AUDITORÍA
  // ==========================================

  /**
   * Consulta el registro de auditoría cronológico del reclamo.
   */
  async obtenerHistorial(reclamoId: number): Promise<HistorialReclamo[]> {
    const respuesta = await clienteAxios.get<HistorialReclamo[]>(`/reclamos/${reclamoId}/historial`);
    return respuesta.data;
  }
};
