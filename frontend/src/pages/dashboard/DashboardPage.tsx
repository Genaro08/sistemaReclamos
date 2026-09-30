import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { LogOut, User, ShieldCheck } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { usuario, logout } = useAuth();

  return (
    <div style={{ padding: '2.5rem', maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: '#f8fafc' }}>
            ¡Bienvenido, {usuario?.nombre} {usuario?.apellido}!
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>
            Panel Principal del Sistema de Gestión de Reclamos e Inteligencia Técnica
          </p>
        </div>
        <button
          onClick={logout}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.6rem 1.2rem',
            backgroundColor: '#ef4444',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 600
          }}
        >
          <LogOut size={18} />
          <span>Cerrar Sesión</span>
        </button>
      </header>

      <div
        style={{
          backgroundColor: '#1e293b',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          padding: '1.75rem',
          display: 'grid',
          gap: '1rem'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <User style={{ color: '#38bdf8' }} size={22} />
          <span>
            <strong>Email:</strong> {usuario?.email}
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <ShieldCheck style={{ color: '#10b981' }} size={22} />
          <span>
            <strong>Rol Asignado:</strong>{' '}
            <span
              style={{
                backgroundColor: '#334155',
                padding: '0.2rem 0.6rem',
                borderRadius: '6px',
                fontSize: '0.85rem',
                color: '#38bdf8'
              }}
            >
              {usuario?.rol}
            </span>
          </span>
        </div>
      </div>
    </div>
  );
};
