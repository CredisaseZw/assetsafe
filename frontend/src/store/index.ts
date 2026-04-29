import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// ─── Auth Store ───────────────────────────────────────────────────────────────
interface AuthState {
  user: { id: number; name: string; email: string } | null
  token: string | null
  isAuthenticated: boolean
  setAuth: (user: AuthState['user'], token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setAuth: (user, token) => {
        localStorage.setItem('access_token', token)
        set({ user, token, isAuthenticated: true })
      },
      logout: () => {
        localStorage.removeItem('access_token')
        set({ user: null, token: null, isAuthenticated: false })
      },
    }),
    { name: 'auth-store' },
  ),
)

// ─── UI Store ─────────────────────────────────────────────────────────────────
interface UIState {
  sidebarOpen: boolean
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
}

export const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}))
