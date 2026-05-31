import axiosInstance from './axiosInstance';
import { toBackendAssetType } from '@/lib/assetTypes';
import { mapAssetFormToApi } from '@/lib/registryPayloads';
import type {
  ApiResponse,
  AssetRegistryDashboard,
  AssetRecord,
  AssetFormData,
  AssetType,
  User,
} from '@/types';

export const assetRegistryApi = {
  getDashboard: async (params?: {
    asset_type?: AssetType;
  }): Promise<AssetRegistryDashboard> => {
    const { data } = await axiosInstance.get<
      ApiResponse<AssetRegistryDashboard>
    >('/asset-management/stats/', { params });
    return data.data ?? (data as unknown as AssetRegistryDashboard);
  },

  getRecords: async (params?: {
    asset_type?: AssetType;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ records: AssetRecord[]; count: number }> => {
    const queryParams = params?.asset_type
      ? { ...params, asset_type: toBackendAssetType(params.asset_type) }
      : params;
    const { data } = await axiosInstance.get<any>('/asset-management/', {
      params: queryParams,
    });
    const payload = data?.data ?? data;
    const recordsRaw = payload?.results ?? payload?.data ?? payload ?? [];
    const count =
      typeof payload?.count === 'number'
        ? payload.count
        : Array.isArray(recordsRaw)
          ? recordsRaw.length
          : 0;
    const records = Array.isArray(recordsRaw)
      ? recordsRaw.map((record: any) => ({
          id: record.id,
          lodge_date: record.lodge_date,
          registration_number: record.registration_number,
          owner_name: record.owner_display ?? record.owner_name ?? '',
          owner_type: record.owner_type ?? 'individual',
          owner_id:
            record.owner_id ??
            record.individual_owner ??
            record.company_owner ??
            0,
          owner_asset_number: record.owner_asset_number ?? '',
          asset_description:
            record.description ??
            `${record.asset_make ?? ''} ${record.asset_model ?? ''}`.trim(),
          asset_type: toBackendAssetType(record.asset_type ?? ''),
          asset_make: record.asset_make ?? '',
          asset_model: record.asset_model ?? '',
          year_of_make: record.year_of_make ?? 0,
          condition: record.condition ?? 'new',
          mv_registration_no: record.mv_registration_number ?? '',
          chassis_number: record.chassis_number ?? '',
          engine_number: record.engine_number ?? '',
          serial_number:
            record.primary_identifier ?? record.serial_number ?? '',
          currency: record.currency_code ?? record.currency ?? 'USD',
          estimated_value: record.estimated_value ?? 0,
          location_address: record.location_address ?? '',
          subscription_start_date: record.subscription_start_date ?? '',
          subscription_end_date: record.subscription_end_date ?? '',
          status: record.is_active === false ? 'expired' : 'active',
        }))
      : [];

    return { records, count };
  },

  getRecord: async (id: number): Promise<AssetRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<AssetRecord>>(
      `/asset-management/${id}/`,
    );
    return data.data ?? (data as unknown as AssetRecord);
  },

  createRecord: async (payload: AssetFormData): Promise<AssetRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<AssetRecord>>(
      '/asset-management/',
      mapAssetFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as AssetRecord);
  },

  updateRecord: async (
    id: number,
    payload: Partial<AssetFormData>,
  ): Promise<AssetRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<AssetRecord>>(
      `/asset-management/${id}/`,
      mapAssetFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as AssetRecord);
  },

  deleteRecord: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/asset-management/${id}/`);
  },

  searchUsers: async (
    query: string,
    type?: 'individual' | 'company',
  ): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>(
      '/users/search/',
      {
        params: { q: query, type },
      },
    );
    return data.data ?? (data as unknown as User[]);
  },
};
