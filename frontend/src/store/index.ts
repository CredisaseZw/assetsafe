import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { AuthUser } from '@/api/authApi';

// ─── Auth Store ───────────────────────────────────────────────────────────────
interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isInitializing: boolean; // true while we check session on app boot
  /** false until login/me has set user.is_staff for this session */
  authReady: boolean;

  // actions
  setUser: (user: AuthUser) => void;
  setInitializing: (v: boolean) => void;
  setAuthReady: (v: boolean) => void;
  loginSuccess: (user: AuthUser) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isInitializing: false,
      authReady: false,

      setUser: (user) => set({ user, isAuthenticated: true, authReady: true }),
      setInitializing: (v) => set({ isInitializing: v }),
      setAuthReady: (v) => set({ authReady: v }),

      loginSuccess: (user) =>
        set({
          user,
          isAuthenticated: true,
          isInitializing: false,
          authReady: true,
        }),

      logout: () => {
        set({
          user: null,
          isAuthenticated: false,
          isInitializing: false,
          authReady: false,
        });
      },
    }),
    {
      name: 'auth-store',
      storage: createJSONStorage(() => sessionStorage), // sessionStorage: cleared when tab closes
      partialize: (s) => ({
        user: s.user,
        isAuthenticated: s.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        if (state?.isAuthenticated) {
          state.setAuthReady(false);
          state.setInitializing(true);
        }
      },
    },
  ),
);

// ─── UI Store ─────────────────────────────────────────────────────────────────
interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}));
