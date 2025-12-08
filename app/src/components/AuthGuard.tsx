import React, { useEffect, useState } from 'react';
import { Dashboard } from './Dashboard';

interface AuthGuardProps {
  children?: React.ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    setIsAuthenticated(!!token);
  }, []);

  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen bg-tana-bg text-tana-text flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Checking authentication...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to signin page
    window.location.href = '/signin';
    return null;
  }

  return children ? <>{children}</> : <Dashboard />;
}
