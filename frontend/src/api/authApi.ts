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
  role?: string;
  is_staff?: boolean;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthUser> => {
    const { data } = await axiosInstance.post<any>('/auth/login/', credentials);
    // Backend returns { user: {...}, message: "..." } and sets HTTP-only cookies.
    return data.user ?? data.data?.user ?? data;
  },

  logout: async (): Promise<void> => {
    try {
      await axiosInstance.post('/auth/logout/', {});
    } catch {
      // Ignore server errors on logout; browser-managed cookies will expire server-side.
    }
  },

  me: async (): Promise<AuthUser> => {
    const { data } =
      await axiosInstance.get<ApiResponse<AuthUser>>('/auth/me/');
    return data.data ?? (data as unknown as AuthUser);
  },
};
