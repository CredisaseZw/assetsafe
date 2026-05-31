import axiosInstance from './axiosInstance';
import {
  mapBranchSearchResult,
  unwrapSearchList,
  type SearchOption,
} from '@/lib/searchResults';

export interface CompanyCreatePayload {
  registration_number: string;
  registration_name: string;
  trading_name: string;
  legal_status?: string;
  date_of_incorporation?: string | null;
  industry?: string;
}

export const companiesApi = {
  /** GET /api/companies/branches/search/?q=... */
  searchBranches: async (query: string): Promise<SearchOption[]> => {
    const term = query.trim();
    if (!term) return [];

    const { data } = await axiosInstance.get<unknown>(
      '/companies/branches/search/',
      { params: { q: term } },
    );

    return unwrapSearchList(data).map((row) =>
      mapBranchSearchResult(row as Record<string, unknown>),
    );
  },

  createCompany: async (
    payload: CompanyCreatePayload,
  ): Promise<{ id: number; name: string }> => {
    const { data } = await axiosInstance.post<unknown>('/companies/', payload);
    const body = (data as { data?: Record<string, unknown> })?.data ?? data;
    const record = body as Record<string, unknown>;
    return {
      id: Number(record.id),
      name: String(
        record.trading_name ?? record.registration_name ?? 'Company',
      ),
    };
  },
};
