import { clienteAxios } from './clienteAxios';
import type { Categoria, SolicitudActualizarCategoria, SolicitudCrearCategoria } from '../types/categoria';

export const categoriaApi = {
  /**
   * Obtiene el listado de categorías/conceptos.
   * Permite filtrar únicamente las activas mediante soloActivas=true.
   */
  async obtenerCategorias(soloActivas: boolean = false): Promise<Categoria[]> {
    const respuesta = await clienteAxios.get<Categoria[]>('/categorias', {
      params: { soloActivas }
    });
    return respuesta.data;
  },

  /**
   * Obtiene una categoría por su ID.
   */
  async obtenerCategoriaPorId(categoriaId: number): Promise<Categoria> {
    const respuesta = await clienteAxios.get<Categoria>(`/categorias/${categoriaId}`);
    return respuesta.data;
  },

  /**
   * Crea una nueva categoría (requiere rol ADMIN).
   */
  async crearCategoria(datos: SolicitudCrearCategoria): Promise<Categoria> {
    const respuesta = await clienteAxios.post<Categoria>('/categorias', datos);
    return respuesta.data;
  },

  /**
   * Actualiza los datos o estado de una categoría existente (requiere rol ADMIN).
   */
  async actualizarCategoria(categoriaId: number, datos: SolicitudActualizarCategoria): Promise<Categoria> {
    const respuesta = await clienteAxios.put<Categoria>(`/categorias/${categoriaId}`, datos);
    return respuesta.data;
  }
};
