import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { RutasApp } from './routes/RutasApp';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <RutasApp />
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
