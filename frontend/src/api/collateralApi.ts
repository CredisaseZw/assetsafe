import axiosInstance from './axiosInstance';
import { mapCollateralFormToApi } from '@/lib/registryPayloads';
import type {
  ApiResponse,
  CollateralDashboard,
  CollateralRecord,
  CollateralFormData,
  User,
} from '@/types';

export const collateralApi = {
  getDashboard: async (params?: {
    search_field?: string;
    search_value?: string;
  }): Promise<CollateralDashboard> => {
    const { data } = await axiosInstance.get<ApiResponse<CollateralDashboard>>(
      '/collateral/stats/',
      { params },
    );
    return data.data ?? (data as unknown as CollateralDashboard);
  },

  getRecords: async (params?: {
    search?: string;
    search_field?: string;
    search_value?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ records: CollateralRecord[]; count: number }> => {
    const { data } = await axiosInstance.get<any>('/collateral/', { params });
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
          agreement_number: record.agreement_number,
          debtor_name: record.debtor_display ?? record.debtor_name ?? '',
          debtor_type: record.debtor_type ?? 'individual',
          debtor_id:
            record.debtor_id ??
            record.individual_debtor ??
            record.company_debtor ??
            0,
          asset_description:
            record.description ??
            `${record.make ?? ''} ${record.model ?? ''}`.trim(),
          asset_type: record.asset_type,
          asset_make: record.make ?? '',
          asset_model: record.model ?? '',
          asset_year: record.year_of_make ?? 0,
          asset_condition: record.condition ?? 'new',
          asset_registration_no:
            record.asset_registration_number ?? record.primary_identifier ?? '',
          chassis_number: record.chassis_number ?? '',
          engine_number: record.engine_number ?? '',
          serial_number:
            record.serial_number ?? record.primary_identifier ?? '',
          currency: record.currency_code ?? record.currency ?? 'USD',
          loan_amount: record.total_debt ?? record.loan_amount ?? 0,
          instalment_amount: record.instalment_amount ?? 0,
          instalment_date: record.instalment_day ?? record.instalment_date ?? 1,
          total_paid_to_date: record.total_paid_to_date ?? 0,
          balance: record.balance ?? 0,
          start_date: record.agreement_start_date ?? record.start_date ?? '',
          end_date: record.agreement_end_date ?? record.end_date ?? '',
          financier_name:
            record.financier_display ?? record.financier_name ?? '',
          financier_type: record.financier_type ?? 'company',
          financier_id: record.financier_id ?? 0,
          data_source_name: record.data_source_name ?? '',
          data_source_position: record.data_source_position ?? '',
          data_date: record.data_date ?? record.lodge_date ?? '',
          status: record.is_discharged ? 'discharged' : 'active',
        }))
      : [];

    return { records, count };
  },

  getRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<CollateralRecord>>(
      `/collateral/${id}/`,
    );
    return data.data ?? (data as unknown as CollateralRecord);
  },

  createRecord: async (
    payload: CollateralFormData,
  ): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<CollateralRecord>>(
      '/collateral/',
      mapCollateralFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as CollateralRecord);
  },

  updateRecord: async (
    id: number,
    payload: Partial<CollateralFormData>,
  ): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<CollateralRecord>>(
      `/collateral/${id}/`,
      mapCollateralFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as CollateralRecord);
  },

  deleteRecord: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/collateral/${id}/`);
  },

  dischargeRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<CollateralRecord>>(
      `/collateral/${id}/discharge/`,
    );
    return data.data ?? (data as unknown as CollateralRecord);
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
