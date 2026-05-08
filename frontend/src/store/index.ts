import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { AuthUser } from '@/api/authApi';

// ─── Auth Store ───────────────────────────────────────────────────────────────
interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isInitializing: boolean; // true while we check session on app boot

  // actions
  setUser: (user: AuthUser) => void;
  setInitializing: (v: boolean) => void;
  loginSuccess: (user: AuthUser) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isInitializing: false,

      setUser: (user) => set({ user, isAuthenticated: true }),
      setInitializing: (v) => set({ isInitializing: v }),

      loginSuccess: (user) =>
        set({ user, isAuthenticated: true, isInitializing: false }),

      logout: () => {
        set({ user: null, isAuthenticated: false, isInitializing: false });
      },
    }),
    {
      name: 'auth-store',
      storage: createJSONStorage(() => sessionStorage), // sessionStorage: cleared when tab closes
      partialize: (s) => ({ user: s.user, isAuthenticated: s.isAuthenticated }),
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
