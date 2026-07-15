import { Navigate } from 'react-router-dom';
import { useIsStaff } from '@/hooks/useIsStaff';

interface StaffOnlyRouteProps {
  children: React.ReactNode;
}

export function StaffOnlyRoute({ children }: StaffOnlyRouteProps) {
  const isStaff = useIsStaff();

  if (!isStaff) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}
