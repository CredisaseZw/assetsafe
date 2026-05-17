import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export const companiesApi = {
  searchBranches: async (query: string): Promise<any[]> => {
    const { data } = await axiosInstance.get<ApiResponse<any[]>>(
      '/companies/branches/search/',
      { params: { q: query } },
    );
    return data.data ?? (data as unknown as any[]);
  },
  searchCompanies: async (query: string): Promise<any[]> => {
    const { data } = await axiosInstance.get<any>('/companies/', {
      params: { search: query },
    });
    const payload = data?.data ?? data;
    const results = payload?.results ?? payload ?? [];
    return Array.isArray(results) ? results : [];
  },
};
