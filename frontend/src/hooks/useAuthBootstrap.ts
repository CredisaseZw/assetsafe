import { useEffect, useRef } from 'react';
import { useAuthStore } from '@/store';
import { authApi } from '@/api/authApi';

/** Refresh the session user (including is_staff) on protected app load. */
export function useAuthBootstrap() {
  const runId = useRef(0);
  const { setUser, setInitializing, setAuthReady, logout } = useAuthStore();

  useEffect(() => {
    const id = ++runId.current;
    let cancelled = false;

    async function bootstrap() {
      if (!useAuthStore.getState().isAuthenticated) {
        setAuthReady(false);
        setInitializing(false);
        return;
      }

      setAuthReady(false);
      setInitializing(true);
      try {
        const user = await authApi.me();
        if (!cancelled && id === runId.current) {
          setUser(user);
        }
      } catch {
        if (!cancelled && id === runId.current) {
          logout();
        }
      } finally {
        if (!cancelled && id === runId.current) {
          setInitializing(false);
        }
      }
    }

    void bootstrap();
    return () => {
      cancelled = true;
    };
  }, [setUser, setInitializing, setAuthReady, logout]);
}
