import axiosInstance from './axiosInstance';
import { unwrapApiData } from '@/lib/parsePaginatedApi';
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

export interface ClientUserOption {
  id: number;
  name: string;
  position?: string;
}

export interface ClientDetail {
  id: number;
  name: string;
  client_details?: {
    full_name?: string;
    first_name?: string;
    last_name?: string;
  };
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

  /** GET /api/clients/{id}/ */
  getClient: async (id: number): Promise<ClientDetail> => {
    const { data } = await axiosInstance.get<unknown>(`/clients/${id}/`);
    const raw = unwrapApiData<Record<string, unknown>>(data);
    return {
      id: Number(raw.id),
      name: String(raw.name ?? ''),
      client_details: raw.client_details as ClientDetail['client_details'],
    };
  },

  /** GET /api/clients/users/?client_id=... */
  listClientUsers: async (clientId: number): Promise<ClientUserOption[]> => {
    const { data } = await axiosInstance.get<unknown>('/clients/users/', {
      params: { client_id: clientId },
    });
    const rows = unwrapSearchList(data);
    return rows.map((row) => {
      const item = row as Record<string, unknown>;
      const first = String(item.first_name ?? '');
      const last = String(item.last_name ?? '');
      const name =
        `${first} ${last}`.trim() ||
        String(item.username ?? item.email ?? `User #${item.id}`);
      return {
        id: Number(item.id),
        name,
        position:
          typeof item.position === 'string' ? item.position : undefined,
      };
    });
  },
};
