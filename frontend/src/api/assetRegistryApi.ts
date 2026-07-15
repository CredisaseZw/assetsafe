import axiosInstance from './axiosInstance';
import { toBackendAssetType } from '@/lib/assetTypes';
import { mapAssetFormToApi } from '@/lib/registryPayloads';
import type {
  ApiResponse,
  AssetRegistryDashboard,
  AssetRecord,
  AssetFormData,
} from '@/types';

export const assetRegistryApi = {
  getDashboard: async (params?: {
    asset_category?: string;
  }): Promise<AssetRegistryDashboard> => {
    const { data } = await axiosInstance.get<
      ApiResponse<AssetRegistryDashboard>
    >('/asset-management/stats/', { params });
    return data.data ?? (data as unknown as AssetRegistryDashboard);
  },

  getRecords: async (params?: {
    asset_category?: string;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ records: AssetRecord[]; count: number }> => {
    const queryParams = params?.asset_category
      ? {
          ...params,
          asset_category: toBackendAssetType(params.asset_category),
        }
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
            `${record.make ?? record.asset_make ?? ''} ${record.model ?? record.asset_model ?? ''}`.trim(),
          asset_category: toBackendAssetType(record.asset_category ?? ''),
          asset_type: String(record.asset_type ?? ''),
          asset_make: record.make ?? record.asset_make ?? '',
          asset_model: record.model ?? record.asset_model ?? '',
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
          status: (record.is_active === false
            ? 'expired'
            : 'active') as AssetRecord['status'],
        }))
      : [];

    return { records, count };
  },

  getRecord: async (id: number): Promise<AssetRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<any>>(
      `/asset-management/${id}/`,
    );
    const r = data.data ?? data;
    return {
      id: r.id,
      lodge_date: r.lodge_date ?? '',
      registration_number: r.registration_number ?? '',
      owner_name: r.owner_display ?? '',
      owner_type: r.owner_type ?? 'individual',
      owner_id: r.individual_owner ?? r.company_owner ?? 0,
      owner_asset_number: r.owner_asset_number ?? '',
      asset_description: `${r.make ?? ''} ${r.model ?? ''}`.trim(),
      asset_category: r.asset_category ?? '',
      asset_type: r.asset_type ?? '',
      asset_make: r.make ?? '',
      asset_model: r.model ?? '',
      year_of_make: r.year_of_make ?? 0,
      condition: r.condition ?? 'new',
      mv_registration_no: r.mv_registration_number ?? '',
      chassis_number: r.chassis_number ?? '',
      engine_number: r.engine_number ?? '',
      serial_number: r.serial_number ?? '',
      currency: r.currency ?? '',
      estimated_value: r.estimated_value ?? 0,
      location_address: r.location_address ?? '',
      subscription_start_date: r.subscription_start_date ?? '',
      subscription_end_date: r.subscription_end_date ?? '',
      status: (r.is_active === false
        ? 'expired'
        : 'active') as AssetRecord['status'],
    };
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
};
