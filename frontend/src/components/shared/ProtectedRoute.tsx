import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store';
import { useAuthBootstrap } from '@/hooks/useAuthBootstrap';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const location = useLocation();
  const { isAuthenticated, isInitializing } = useAuthStore();

  useAuthBootstrap();

  // While checking session on first load, show a centered spinner
  if (isInitializing) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0d1f3c]">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-[#1a9aad]" />
          <p className="text-sm text-slate-400">Loading session…</p>
        </div>
      </div>
    );
  }

  // Not authenticated → send to /login, preserve intended destination
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
