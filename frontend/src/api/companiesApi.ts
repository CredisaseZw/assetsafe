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
  addresses?: {
    address_type?: string;
    is_primary?: boolean;
    street_address: string;
    suburb_id: number;
  }[];
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
    const { data } = await axiosInstance.post<unknown>(
      '/companies/companies/',
      payload,
    );
    const body = (data as { data?: Record<string, unknown> })?.data ?? data;
    const record = body as Record<string, unknown>;
    // Create returns the HQ branch (CompanyBranchDetailSerializer).
    const mapped = mapBranchSearchResult(record);
    return {
      id: mapped.id || Number(record.id),
      name: mapped.name,
    };
  },
};
