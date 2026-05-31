import { useAuthStore } from '@/store';
import { canAccessAssetRegistry } from '@/lib/registryNav';

export function useIsStaff(): boolean {
  const user = useAuthStore((s) => s.user);
  const authReady = useAuthStore((s) => s.authReady);
  return canAccessAssetRegistry(user, authReady);
}
