import { useAuthStore } from '@/store';

export function useIsSuperuser(): boolean {
  const user = useAuthStore((s) => s.user);
  return user?.is_superuser === true;
}
