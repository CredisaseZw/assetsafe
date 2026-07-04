import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export interface ManagedUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
  is_verified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  date_joined: string;
}

export interface CreateUserPayload {
  email: string;
  username?: string;
  password: string;
  first_name?: string;
  last_name?: string;
  position?: string;
  client_id?: number;
  is_staff?: boolean;
  is_superuser?: boolean;
}

export const usersApi = {
  list: async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
  }): Promise<{ results: ManagedUser[]; count: number }> => {
    const { data } = await axiosInstance.get<{
      count: number;
      results: ManagedUser[];
    }>('/auth/', { params });
    return {
      results: data.results ?? [],
      count: data.count ?? 0,
    };
  },

  create: async (payload: CreateUserPayload): Promise<ManagedUser> => {
    const { data } = await axiosInstance.post<ApiResponse<ManagedUser>>(
      '/auth/',
      payload,
    );
    return data.data ?? (data as unknown as ManagedUser);
  },

  update: async (
    id: number,
    payload: Partial<CreateUserPayload>,
  ): Promise<ManagedUser> => {
    const { data } = await axiosInstance.patch<ApiResponse<ManagedUser>>(
      `/auth/${id}/`,
      payload,
    );
    return data.data ?? (data as unknown as ManagedUser);
  },

  remove: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/auth/${id}/`);
  },
};
