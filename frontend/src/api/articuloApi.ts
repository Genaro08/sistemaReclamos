import { clienteAxios } from './clienteAxios';
import type {
  Articulo,
  ArticuloCoincidencia,
  PlantillaRespuesta,
  SolicitudActualizarArticulo,
  SolicitudCrearArticulo,
  SolicitudCrearPlantilla,
} from '../types/articulo';

export const articuloApi = {
  /**
   * Obtiene la lista de artículos de conocimiento.
   * Permite filtrar por ID de categoría o por etiqueta.
   */
  async obtenerArticulos(categoriaId?: number, etiqueta?: string): Promise<Articulo[]> {
    const respuesta = await clienteAxios.get<Articulo[]>('/articulos', {
      params: { categoriaId, etiqueta }
    });
    return respuesta.data;
  },

  /**
   * Motor de Recomendación por % de Coincidencia:
   * Compara la consulta ingresada contra títulos y etiquetas de la Base de Conocimientos.
   */
  async buscarPorCoincidencia(consulta: string, limite: number = 5): Promise<ArticuloCoincidencia[]> {
    const respuesta = await clienteAxios.get<ArticuloCoincidencia[]>('/articulos/buscar', {
      params: { q: consulta, limite }
    });
    return respuesta.data;
  },

  /**
   * Obtiene el detalle completo de un artículo por su ID.
   */
  async obtenerArticuloPorId(articuloId: number): Promise<Articulo> {
    const respuesta = await clienteAxios.get<Articulo>(`/articulos/${articuloId}`);
    return respuesta.data;
  },

  /**
   * Redacta un nuevo artículo de conocimiento (requiere rol OPERATOR o ADMIN).
   */
  async crearArticulo(datos: SolicitudCrearArticulo): Promise<Articulo> {
    const respuesta = await clienteAxios.post<Articulo>('/articulos', datos);
    return respuesta.data;
  },

  /**
   * Modifica un artículo existente (requiere rol OPERATOR o ADMIN).
   */
  async actualizarArticulo(articuloId: number, datos: SolicitudActualizarArticulo): Promise<Articulo> {
    const respuesta = await clienteAxios.put<Articulo>(`/articulos/${articuloId}`, datos);
    return respuesta.data;
  },

  // ==========================================
  // PLANTILLAS DE RESPUESTA PÚBLICA
  // ==========================================

  /**
   * Agrega una nueva plantilla de respuesta pública asociada a un artículo.
   */
  async crearPlantilla(articuloId: number, datos: SolicitudCrearPlantilla): Promise<PlantillaRespuesta> {
    const respuesta = await clienteAxios.post<PlantillaRespuesta>(`/articulos/${articuloId}/plantillas`, datos);
    return respuesta.data;
  },

  /**
   * Lista todas las plantillas de respuesta asociadas a un artículo técnico.
   */
  async obtenerPlantillasPorArticulo(articuloId: number): Promise<PlantillaRespuesta[]> {
    const respuesta = await clienteAxios.get<PlantillaRespuesta[]>(`/articulos/${articuloId}/plantillas`);
    return respuesta.data;
  }
};
