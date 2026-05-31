import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  is_staff?: boolean;
  is_superuser?: boolean;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
  is_verified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

export function normalizeAuthUser(raw: Record<string, unknown>): AuthUser {
  const first = typeof raw.first_name === 'string' ? raw.first_name : '';
  const last = typeof raw.last_name === 'string' ? raw.last_name : '';
  const combined = [first, last].filter(Boolean).join(' ');

  return {
    id: Number(raw.id),
    name:
      (typeof raw.name === 'string' && raw.name) ||
      combined ||
      (typeof raw.username === 'string' ? raw.username : ''),
    email: typeof raw.email === 'string' ? raw.email : '',
    username: typeof raw.username === 'string' ? raw.username : '',
    first_name: first || undefined,
    last_name: last || undefined,
    role:
      typeof raw.user_type === 'string'
        ? raw.user_type
        : typeof raw.role === 'string'
          ? raw.role
          : undefined,
    is_staff: raw.is_staff === true,
    is_superuser: raw.is_superuser === true,
  };
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthUser> => {
    const { data } = await axiosInstance.post<any>('/auth/login/', credentials);
    const raw = data.user ?? data.data?.user ?? data;
    return normalizeAuthUser(raw as Record<string, unknown>);
  },

  logout: async (): Promise<void> => {
    try {
      await axiosInstance.post('/auth/logout/', {});
    } catch {
      // Ignore server errors on logout
    }
  },

  me: async (): Promise<AuthUser> => {
    const { data } =
      await axiosInstance.get<ApiResponse<AuthUser>>('/auth/me/');
    const raw = (data as { data?: Record<string, unknown> }).data ?? data;
    return normalizeAuthUser(raw as Record<string, unknown>);
  },

  getProfile: async (): Promise<UserProfile> => {
    const { data } = await axiosInstance.get<UserProfile>('/auth/me/');
    return data;
  },

  updateProfile: async (payload: {
    first_name?: string;
    last_name?: string;
    email?: string;
  }): Promise<UserProfile> => {
    const { data } = await axiosInstance.patch<UserProfile>(
      '/auth/me/',
      payload,
    );
    return data;
  },

  changePassword: async (payload: {
    current_password: string;
    new_password: string;
    confirm_password: string;
  }): Promise<void> => {
    await axiosInstance.post('/auth/password/change/', payload);
  },

  requestPasswordReset: async (email: string): Promise<{ message: string }> => {
    const { data } = await axiosInstance.post<{ message: string }>(
      '/auth/password/reset/',
      { email },
    );
    return data;
  },

  validatePasswordReset: async (
    uid: string,
    token: string,
  ): Promise<{ valid: boolean; message: string }> => {
    const { data } = await axiosInstance.post<{
      valid: boolean;
      message: string;
    }>('/auth/password/reset/validate/', { uid, token });
    return data;
  },

  confirmPasswordReset: async (
    uid: string,
    token: string,
    payload: { new_password: string; confirm_password: string },
  ): Promise<{ message: string }> => {
    const { data } = await axiosInstance.post<{ message: string }>(
      `/auth/password/reset/confirm/${encodeURIComponent(uid)}/${encodeURIComponent(token)}/`,
      payload,
    );
    return data;
  },
};
