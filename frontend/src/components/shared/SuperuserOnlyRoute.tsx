import { Navigate } from 'react-router-dom';
import { useIsSuperuser } from '@/hooks/useIsSuperuser';

interface SuperuserOnlyRouteProps {
  children: React.ReactNode;
}

export function SuperuserOnlyRoute({ children }: SuperuserOnlyRouteProps) {
  const isSuperuser = useIsSuperuser();

  if (!isSuperuser) {
    return <Navigate to="/collateral" replace />;
  }

  return <>{children}</>;
}
