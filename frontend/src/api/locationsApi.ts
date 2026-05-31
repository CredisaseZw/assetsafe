import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export interface SuburbOption {
  id: number;
  name: string;
}

export const locationsApi = {
  searchSuburbs: async (query?: string): Promise<SuburbOption[]> => {
    const { data } = await axiosInstance.get<ApiResponse<SuburbOption[]>>(
      '/suburbs/',
      { params: query ? { search: query } : undefined },
    );
    const payload = data?.data ?? data;
    return Array.isArray(payload) ? payload : [];
  },
};
