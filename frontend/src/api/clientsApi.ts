import axiosInstance from './axiosInstance';
import {
  mapClientSearchResult,
  unwrapSearchList,
  type SearchOption,
} from '@/lib/searchResults';

export interface CreateClientPayload {
  individual_id?: number;
  company_branch_id?: number;
  client_type?: string;
  status?: string;
}

export interface CreatedClient {
  id: number;
  name: string;
}

export const clientsApi = {
  /** POST /api/clients/ */
  createClient: async (payload: CreateClientPayload): Promise<CreatedClient> => {
    const { data } = await axiosInstance.post<unknown>('/clients/', payload);
    const raw =
      data && typeof data === 'object' && 'data' in (data as object)
        ? (data as { data: Record<string, unknown> }).data
        : (data as Record<string, unknown>);

    return {
      id: Number(raw.id),
      name: String(raw.name ?? `Client #${raw.id}`),
    };
  },

  /** GET /api/clients/search/?q=...&entity_type=individual|company */
  searchClients: async (
    query: string,
    options?: { entityType?: 'individual' | 'company' },
  ): Promise<SearchOption[]> => {
    const term = query.trim();
    if (!term) return [];

    const { data } = await axiosInstance.get<unknown>('/clients/search/', {
      params: {
        q: term,
        ...(options?.entityType ? { entity_type: options.entityType } : {}),
      },
    });

    return unwrapSearchList(data).map((row) =>
      mapClientSearchResult(row as Record<string, unknown>),
    );
  },
};
