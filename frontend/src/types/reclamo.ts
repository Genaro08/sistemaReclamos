import type { ArticuloResumen, PlantillaRespuesta } from './articulo';
import type { Categoria } from './categoria';
import type { Usuario } from './usuario';

export const PrioridadReclamo = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
  CRITICAL: 'CRITICAL',
} as const;

export type PrioridadReclamo = (typeof PrioridadReclamo)[keyof typeof PrioridadReclamo];

export const EstadoReclamo = {
  PENDING: 'PENDING',
  IN_PROGRESS: 'IN_PROGRESS',
  WAITING_INFO: 'WAITING_INFO',
  RESOLVED: 'RESOLVED',
  CLOSED: 'CLOSED',
  CANCELLED: 'CANCELLED',
} as const;

export type EstadoReclamo = (typeof EstadoReclamo)[keyof typeof EstadoReclamo];

export interface Reclamo {
  id: number;
  titulo: string;
  descripcion: string;
  prioridad: PrioridadReclamo;
  estado: EstadoReclamo;
  categoriaId: number;
  creadorId: number;
  responsableId?: number | null;
  articuloAplicadoId?: number | null;
  plantillaAplicadaId?: number | null;
  porcentajeCoincidenciaAuto?: number | null;
  categoria?: Categoria;
  creador?: Usuario;
  responsable?: Usuario | null;
  articuloAplicado?: ArticuloResumen | null;
  plantillaAplicada?: PlantillaRespuesta | null;
  fechaCreacion: string;
  fechaActualizacion: string;
  fechaResolucion?: string | null;
  fechaCierre?: string | null;
}

export interface Comentario {
  id: number;
  reclamoId: number;
  usuarioId: number;
  contenido: string;
  esInternoTecnico: boolean;
  usuario?: Usuario;
  fechaCreacion: string;
}

export interface HistorialReclamo {
  id: number;
  reclamoId: number;
  usuarioId: number;
  accion: string;
  usuario?: Usuario;
  fecha: string;
}

export interface SolicitudCrearReclamo {
  titulo: string;
  descripcion: string;
  prioridad?: PrioridadReclamo;
  categoriaId: number;
}

export interface SolicitudCambiarEstadoReclamo {
  estado: EstadoReclamo;
  articuloAplicadoId?: number;
  plantillaAplicadaId?: number;
}

export interface SolicitudAsignarResponsable {
  responsableId: number;
}

export interface SolicitudCrearComentario {
  contenido: string;
  esInternoTecnico?: boolean;
}
