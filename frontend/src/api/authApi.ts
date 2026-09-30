import { clienteAxios } from './clienteAxios';
import type { LoginRespuesta, SolicitudLogin, SolicitudRegistro, Usuario } from '../types/usuario';

export const authApi = {
  /**
   * Petición de inicio de sesión de usuario.
   */
  async login(datos: SolicitudLogin): Promise<LoginRespuesta> {
    const respuesta = await clienteAxios.post<LoginRespuesta>('/auth/login', datos);
    return respuesta.data;
  },

  /**
   * Petición de registro de nuevo usuario.
   */
  async registro(datos: SolicitudRegistro): Promise<Usuario> {
    const respuesta = await clienteAxios.post<Usuario>('/auth/registro', datos);
    return respuesta.data;
  },

  /**
   * Petición de solicitud de recuperación de contraseña por email.
   */
  async recuperarPassword(email: string): Promise<{ mensaje: string }> {
    const respuesta = await clienteAxios.post<{ mensaje: string }>('/auth/recuperar-password', { email });
    return respuesta.data;
  },

  /**
   * Petición de renovación de token de acceso vía Refresh Token.
   */
  async refreshToken(refreshToken: string): Promise<LoginRespuesta> {
    const respuesta = await clienteAxios.post<LoginRespuesta>('/auth/refresh', { refreshToken });
    return respuesta.data;
  }
};
