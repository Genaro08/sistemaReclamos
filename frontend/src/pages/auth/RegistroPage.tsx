import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { UserPlus, AlertCircle, Loader2 } from 'lucide-react';
import './AuthPages.css';


export const RegistroPage: React.FC = () => {
  const { registro, error, cargando, limpiarError } = useAuth();
  const navigate = useNavigate();

  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await registro({ nombre, apellido, email, password });
      navigate('/dashboard');
    } catch {
      // Manejado por AuthContext
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-brand">Crear una Cuenta</h1>
          <p className="auth-subtitle">Registrate para generar y hacer seguimiento a tus reclamos</p>
        </div>

        {error && (
          <div className="alert-danger">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              type="text"
              className="form-input"
              placeholder="Juan"
              value={nombre}
              onChange={(e) => {
                limpiarError();
                setNombre(e.target.value);
              }}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="apellido">Apellido</label>
            <input
              id="apellido"
              type="text"
              className="form-input"
              placeholder="Pérez"
              value={apellido}
              onChange={(e) => {
                limpiarError();
                setApellido(e.target.value);
              }}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder="juan@organizacion.com"
              value={email}
              onChange={(e) => {
                limpiarError();
                setEmail(e.target.value);
              }}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Contraseña (Mínimo 6 caracteres)</label>
            <input
              id="password"
              type="password"
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => {
                limpiarError();
                setPassword(e.target.value);
              }}
              minLength={6}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={cargando}>
            {cargando ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                <span>Registrando...</span>
              </>
            ) : (
              <>
                <UserPlus size={20} />
                <span>Crear Cuenta</span>
              </>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            ¿Ya tenés una cuenta?{' '}
            <Link to="/login" className="auth-link">
              Ingresá acá
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
