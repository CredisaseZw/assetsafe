import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export const clientsApi = {
  searchClients: async (query: string): Promise<any[]> => {
    const { data } = await axiosInstance.get<ApiResponse<any[]>>(
      '/clients/search/',
      { params: { q: query } },
    );
    return data.data ?? (data as unknown as any[]);
  },
};
