import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import type { RolUsuario } from '../types/usuario';

interface RutaProtegidaProps {
  rolesPermitidos?: RolUsuario[];
}

export const RutaProtegida: React.FC<RutaProtegidaProps> = ({ rolesPermitidos }) => {
  const { usuario, cargando } = useAuth();

  if (cargando) {
    return (
      <div className="auth-container">
        <div style={{ color: '#94a3b8', fontSize: '1.1rem' }}>Cargando aplicación...</div>
      </div>
    );
  }

  // Si no está autenticado, redirigir al login
  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  // Si requiere roles específicos y el rol actual no está en la lista, redirigir al dashboard
  if (rolesPermitidos && !rolesPermitidos.includes(usuario.rol)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};
