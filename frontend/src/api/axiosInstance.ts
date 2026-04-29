import axios, { type AxiosResponse, type AxiosError } from 'axios'

const BASE_URL = ((import.meta as any).env?.VITE_API_BASE_URL) ?? 'http://localhost:8000/api'

export const axiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,           // supports session auth + CSRF
  headers: { 'Content-Type': 'application/json' },
  timeout: 30_000,
})

// ── Request interceptor ────────────────────────────────────────────────────────
axiosInstance.interceptors.request.use((config) => {
  // JWT token (if using token auth)
  const token = localStorage.getItem('access_token')
  if (token) config.headers['Authorization'] = `Bearer ${token}`

  // Django CSRF for session auth
  const csrfToken = getCookie('csrftoken')
  if (csrfToken) config.headers['X-CSRFToken'] = csrfToken

  return config
})

// ── Response interceptor ───────────────────────────────────────────────────────
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

// ── Helper ─────────────────────────────────────────────────────────────────────
function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))
  return match ? decodeURIComponent(match[2]) : null
}

export default axiosInstance
