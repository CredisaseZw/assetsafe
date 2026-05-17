import { useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { useAuthStore } from '@/store';
import { authApi, type LoginCredentials } from '@/api/authApi';

export function useAuth() {
  const navigate = useNavigate();
  const qc = useQueryClient();
  const {
    user,
    isAuthenticated,
    isInitializing,
    loginSuccess,
    logout: storeLogout,
    setInitializing,
  } = useAuthStore();

  // ── Bootstrap: clear the initial loading gate on mount ────────────────────
  useEffect(() => {
    setInitializing(false);
  }, [setInitializing]);

  // ── Login ──────────────────────────────────────────────────────────────────
  const login = useCallback(
    async (credentials: LoginCredentials) => {
      const user = await authApi.login(credentials);
      loginSuccess(user);
      navigate('/collateral', { replace: true });
      return user;
    },
    [loginSuccess, navigate],
  );

  // ── Logout ─────────────────────────────────────────────────────────────────
  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } catch {
      // Always clear even if server errors
    } finally {
      storeLogout();
      // Nuke all TanStack Query cache so no stale data leaks between users
      qc.clear();
      navigate('/login', { replace: true });
      toast.success('Signed out successfully');
    }
  }, [storeLogout, qc, navigate]);

  return { user, isAuthenticated, isInitializing, login, logout };
}
