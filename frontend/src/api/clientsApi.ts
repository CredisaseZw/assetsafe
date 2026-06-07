import axiosInstance from './axiosInstance';
import {
  mapClientSearchResult,
  unwrapSearchList,
  type SearchOption,
} from '@/lib/searchResults';

export const clientsApi = {
  /** GET /api/clients/search/?q=... */
  searchClients: async (query: string): Promise<SearchOption[]> => {
    const term = query.trim();
    if (!term) return [];

    const { data } = await axiosInstance.get<unknown>('/clients/search/', {
      params: { q: term },
    });

    return unwrapSearchList(data).map((row) =>
      mapClientSearchResult(row as Record<string, unknown>),
    );
  },
};
