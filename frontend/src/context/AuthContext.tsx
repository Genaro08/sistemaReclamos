import React, { createContext, useContext, useState, useEffect } from 'react';
import type { LoginRespuesta, SolicitudLogin, SolicitudRegistro, Usuario } from '../types/usuario';
import { authApi } from '../api/authApi';

interface AuthContextTipo {
  usuario: Usuario | null;
  cargando: boolean;
  error: string | null;
  login: (datos: SolicitudLogin) => Promise<void>;
  registro: (datos: SolicitudRegistro) => Promise<void>;
  logout: () => void;
  limpiarError: () => void;
}

const AuthContext = createContext<AuthContextTipo | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [cargando, setCargando] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Inicialización: Verificar si existe sesión guardada en localStorage
  useEffect(() => {
    const token = localStorage.getItem('tokenAcceso');
    const usuarioGuardado = localStorage.getItem('usuario');

    if (token && usuarioGuardado) {
      try {
        setUsuario(JSON.parse(usuarioGuardado));
      } catch {
        localStorage.removeItem('tokenAcceso');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('usuario');
      }
    }
    setCargando(false);
  }, []);

  const login = async (datos: SolicitudLogin) => {
    try {
      setError(null);
      setCargando(true);
      const respuesta: LoginRespuesta = await authApi.login(datos);

      // Guardar tokens y perfil en localStorage
      localStorage.setItem('tokenAcceso', respuesta.tokenAcceso);
      localStorage.setItem('refreshToken', respuesta.refreshToken);
      localStorage.setItem('usuario', JSON.stringify(respuesta.usuario));

      setUsuario(respuesta.usuario);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Error al iniciar sesión';
      setError(msg);
      throw err;
    } finally {
      setCargando(false);
    }
  };

  const registro = async (datos: SolicitudRegistro) => {
    try {
      setError(null);
      setCargando(true);
      await authApi.registro(datos);
      // Auto-login tras registro exitoso
      await login({ email: datos.email, password: datos.password });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Error al registrar usuario';
      setError(msg);
      throw err;
    } finally {
      setCargando(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('tokenAcceso');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('usuario');
    setUsuario(null);
  };

  const limpiarError = () => setError(null);

  return (
    <AuthContext.Provider
      value={{
        usuario,
        cargando,
        error,
        login,
        registro,
        logout,
        limpiarError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const contexto = useContext(AuthContext);
  if (!contexto) {
    throw new Error('useAuth debe utilizarse dentro de un AuthProvider');
  }
  return contexto;
};
