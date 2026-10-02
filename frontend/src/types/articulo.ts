import type { Categoria } from './categoria';

export interface PlantillaRespuesta {
  id: number;
  articuloId: number;
  titulo: string;
  contenidoUsuario: string;
  fechaCreacion: string;
  fechaActualizacion: string;
}

export interface ArticuloResumen {
  id: number;
  titulo: string;
  resumen?: string | null;
  etiquetas: string;
}

export interface Articulo {
  id: number;
  titulo: string;
  resumen?: string | null;
  contenidoTecnico: string;
  etiquetas: string;
  categoriaId: number;
  vecesUtilizado: number;
  autorId: number;
  fechaCreacion: string;
  fechaActualizacion: string;
  categoria?: Categoria;
  plantillas?: PlantillaRespuesta[];
  articulosRelacionados?: ArticuloResumen[];
}

export interface ArticuloCoincidencia extends Articulo {
  porcentajeCoincidencia: number;
}

export interface SolicitudCrearArticulo {
  titulo: string;
  resumen?: string;
  contenidoTecnico: string;
  etiquetas: string;
  categoriaId: number;
  articulosRelacionadosIds?: number[];
}

export interface SolicitudActualizarArticulo {
  titulo?: string;
  resumen?: string;
  contenidoTecnico?: string;
  etiquetas?: string;
  categoriaId?: number;
  articulosRelacionadosIds?: number[];
}

export interface SolicitudCrearPlantilla {
  articuloId?: number;
  titulo: string;
  contenidoUsuario: string;
}
