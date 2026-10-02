export interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string | null;
  activa: boolean;
  fechaCreacion?: string;
}

export interface SolicitudCrearCategoria {
  nombre: string;
  descripcion?: string;
}

export interface SolicitudActualizarCategoria {
  nombre?: string;
  descripcion?: string;
  activa?: boolean;
}
