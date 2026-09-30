export const RolUsuario = {
  USER: 'USER',
  OPERATOR: 'OPERATOR',
  ADMIN: 'ADMIN',
} as const;

export type RolUsuario = (typeof RolUsuario)[keyof typeof RolUsuario];

export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  rol: RolUsuario;
  activo: boolean;
  fechaCreacion: string;
}

export interface LoginRespuesta {
  tokenAcceso: string;
  refreshToken: string;
  tipoToken: string;
  usuario: Usuario;
}

export interface SolicitudRegistro {
  nombre: string;
  apellido: string;
  email: string;
  password: string;
}

export interface SolicitudLogin {
  email: string;
  password: string;
}
