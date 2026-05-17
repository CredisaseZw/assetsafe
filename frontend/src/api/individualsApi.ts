import axiosInstance from './axiosInstance';
import type { ApiResponse, User } from '@/types';

export const individualsApi = {
  searchIndividuals: async (query: string): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>(
      '/individuals/search/',
      { params: { q: query } },
    );
    return data.data ?? (data as unknown as User[]);
  },
};
