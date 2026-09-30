import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LogIn, AlertCircle, Loader2 } from 'lucide-react';
import './AuthPages.css';


export const LoginPage: React.FC = () => {
  const { login, error, cargando, limpiarError } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch {
      // El error ya es manejado por el AuthContext
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-brand">Sistema de Reclamos</h1>
          <p className="auth-subtitle">Ingresá tus credenciales para acceder a la plataforma</p>
        </div>

        {error && (
          <div className="alert-danger">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder="ejemplo@organizacion.com"
              value={email}
              onChange={(e) => {
                limpiarError();
                setEmail(e.target.value);
              }}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Contraseña</label>
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
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={cargando}>
            {cargando ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                <span>Iniciando sesión...</span>
              </>
            ) : (
              <>
                <LogIn size={20} />
                <span>Iniciar Sesión</span>
              </>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            ¿No tenés una cuenta?{' '}
            <Link to="/registro" className="auth-link">
              Registrate acá
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
