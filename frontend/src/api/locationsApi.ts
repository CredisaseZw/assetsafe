import axiosInstance from './axiosInstance';
import type { ApiResponse } from '@/types';

export interface SuburbOption {
  id: number;
  name: string;
}

export interface CityOption {
  id: number;
  name: string;
}

export interface CountryOption {
  id: number;
  name: string;
  code?: string;
}

function unwrapList<T>(data: unknown): T[] {
  const payload = (data as { data?: unknown })?.data ?? data;
  if (Array.isArray(payload)) return payload as T[];
  const inner = (payload as { results?: unknown })?.results;
  if (Array.isArray(inner)) return inner as T[];
  return [];
}

export const locationsApi = {
  getCountries: async (): Promise<CountryOption[]> => {
    const { data } = await axiosInstance.get('/common/locations/countries/');
    return unwrapList<CountryOption>(data);
  },

  getCities: async (countryId: number): Promise<CityOption[]> => {
    const { data } = await axiosInstance.get('/common/locations/cities/', {
      params: { country_id: countryId },
    });
    return unwrapList<CityOption>(data);
  },

  getSuburbs: async (cityId: number): Promise<SuburbOption[]> => {
    const { data } = await axiosInstance.get('/common/locations/suburbs/', {
      params: { city_id: cityId },
    });
    return unwrapList<SuburbOption>(data);
  },

  searchSuburbs: async (query?: string): Promise<SuburbOption[]> => {
    const { data } = await axiosInstance.get<ApiResponse<SuburbOption[]>>(
      '/common/locations/suburbs/',
      { params: query ? { search: query } : undefined },
    );
    const payload = data?.data ?? data;
    return Array.isArray(payload) ? payload : [];
  },
};
