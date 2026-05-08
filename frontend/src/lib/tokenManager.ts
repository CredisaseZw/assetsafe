import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

// ─── Constants ────────────────────────────────────────────────────────────────
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const COOKIE_OPTIONS = {
  secure: window.location.protocol === 'https:',
  sameSite: 'strict' as const,
  expires: 7, // days
};

// ─── Types ────────────────────────────────────────────────────────────────────
interface JwtPayload {
  user_id: number;
  email?: string;
  name?: string;
  username?: string;
  exp: number;
  iat: number;
  jti?: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

// ─── Token Manager ────────────────────────────────────────────────────────────
class TokenManager {
  private refreshTimer: ReturnType<typeof setTimeout> | null = null;

  // ── Storage: prefer httpOnly-like cookies; fallback localStorage ──────────

  setTokens(pair: TokenPair): void {
    // Store in cookies (sent automatically by browser, SameSite=strict protects CSRF)
    Cookies.set(ACCESS_TOKEN_KEY, pair.access, COOKIE_OPTIONS);
    Cookies.set(REFRESH_TOKEN_KEY, pair.refresh, COOKIE_OPTIONS);
    // Also keep in memory via localStorage for easy read from JS
    localStorage.setItem(ACCESS_TOKEN_KEY, pair.access);
    localStorage.setItem(REFRESH_TOKEN_KEY, pair.refresh);
    this.scheduleRefresh(pair.access);
  }

  getAccessToken(): string | null {
    return (
      Cookies.get(ACCESS_TOKEN_KEY) ?? localStorage.getItem(ACCESS_TOKEN_KEY)
    );
  }

  getRefreshToken(): string | null {
    return (
      Cookies.get(REFRESH_TOKEN_KEY) ?? localStorage.getItem(REFRESH_TOKEN_KEY)
    );
  }

  clearTokens(): void {
    Cookies.remove(ACCESS_TOKEN_KEY);
    Cookies.remove(REFRESH_TOKEN_KEY);
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
      this.refreshTimer = null;
    }
  }

  // ── JWT Decode ────────────────────────────────────────────────────────────

  decodeToken(token: string): JwtPayload | null {
    try {
      return jwtDecode<JwtPayload>(token);
    } catch {
      return null;
    }
  }

  getPayload(): JwtPayload | null {
    const token = this.getAccessToken();
    return token ? this.decodeToken(token) : null;
  }

  isAccessTokenExpired(): boolean {
    const payload = this.getPayload();
    if (!payload) return true;
    // Add 30s buffer
    return Date.now() / 1000 > payload.exp - 30;
  }

  isRefreshTokenExpired(): boolean {
    const token = this.getRefreshToken();
    if (!token) return true;
    const payload = this.decodeToken(token);
    if (!payload) return true;
    return Date.now() / 1000 > payload.exp - 30;
  }

  getSecondsUntilExpiry(): number {
    const payload = this.getPayload();
    if (!payload) return 0;
    return Math.max(0, payload.exp - Date.now() / 1000);
  }

  // ── Auto Refresh Scheduler ────────────────────────────────────────────────

  scheduleRefresh(accessToken: string, onRefresh?: () => Promise<void>): void {
    if (this.refreshTimer) clearTimeout(this.refreshTimer);
    const payload = this.decodeToken(accessToken);
    if (!payload) return;
    // Refresh 60 seconds before expiry
    const msUntilRefresh = (payload.exp - Date.now() / 1000 - 60) * 1000;
    if (msUntilRefresh <= 0) return;
    this.refreshTimer = setTimeout(async () => {
      if (onRefresh) await onRefresh();
    }, msUntilRefresh);
  }

  // ── Session User ──────────────────────────────────────────────────────────

  getUserFromToken(): { id: number; name: string; email: string } | null {
    const payload = this.getPayload();
    if (!payload) return null;
    return {
      id: payload.user_id,
      name:
        payload.name ??
        payload.username ??
        payload.email?.split('@')[0] ??
        'User',
      email: payload.email ?? '',
    };
  }
}

export const tokenManager = new TokenManager();
