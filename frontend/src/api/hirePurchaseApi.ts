import axiosInstance from './axiosInstance';
import { mapHirePurchaseFormToApi } from '@/lib/registryPayloads';
import { unwrapApiData } from '@/lib/parsePaginatedApi';
import type {
  ApiResponse,
  HirePurchaseDashboard,
  HirePurchaseRecord,
  HirePurchaseFormData,
  User,
} from '@/types';

function mapHirePurchaseRecord(
  record: Record<string, unknown>,
): HirePurchaseRecord {
  return {
    id: Number(record.id),
    lodge_date: String(record.lodge_date ?? ''),
    agreement_number: String(record.agreement_number ?? ''),
    purchaser_name: String(
      record.purchaser_display ?? record.purchaser_name ?? '',
    ),
    purchaser_type:
      (record.purchaser_type as HirePurchaseRecord['purchaser_type']) ??
      'individual',
    purchaser_id: Number(
      record.purchaser_id ??
        record.purchaser_individual ??
        record.purchaser_company ??
        0,
    ),
    asset_make: String(record.make ?? record.asset_make ?? ''),
    asset_model: String(record.model ?? record.asset_model ?? ''),
    asset_type: String(record.asset_type ?? ''),
    asset_year: Number(record.year_of_make ?? record.asset_year ?? 0),
    asset_condition:
      (record.condition as HirePurchaseRecord['asset_condition']) ?? 'new',
    reg_serial_number: String(
      record.mv_registration_number ??
        record.serial_number ??
        record.reg_serial_number ??
        '',
    ),
    chassis_number: String(record.chassis_number ?? ''),
    engine_number: String(record.engine_number ?? ''),
    currency: String(record.currency_code ?? record.currency ?? ''),
    purchase_amount: Number(record.purchase_amount ?? 0),
    instalment_amount: Number(record.instalment_amount ?? 0),
    instalment_date: Number(
      record.instalment_day ?? record.instalment_date ?? 1,
    ),
    total_paid_to_date: Number(record.total_paid_to_date ?? 0),
    balance: Number(record.balance ?? 0),
    start_date: String(record.agreement_start_date ?? record.start_date ?? ''),
    end_date: String(record.agreement_end_date ?? record.end_date ?? ''),
    financier_name: String(
      record.financier_display ?? record.financier_name ?? '',
    ),
    financier_id: Number(record.financier ?? record.financier_id ?? 0),
    data_date: String(record.data_date ?? record.lodge_date ?? ''),
    data_source_display: String(record.data_source_display ?? ''),
    data_source_position: String(record.data_source_position ?? ''),
    status: (record.closure_confirmed
      ? 'closed'
      : record.is_pending_closure
        ? 'pending_closure'
        : 'active') as HirePurchaseRecord['status'],
  };
}

export const hirePurchaseApi = {
  getDashboard: async (params?: {
    financier_id?: number;
  }): Promise<HirePurchaseDashboard> => {
    const { data } = await axiosInstance.get<
      ApiResponse<HirePurchaseDashboard>
    >('/hire-purchase/stats/', { params });
    return data.data ?? (data as unknown as HirePurchaseDashboard);
  },

  getRecords: async (params?: {
    financier_id?: number;
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ records: HirePurchaseRecord[]; count: number }> => {
    const { financier_id, ...rest } = params ?? {};
    const queryParams = {
      ...rest,
      ...(financier_id ? { financier: financier_id } : {}),
    };
    const { data } = await axiosInstance.get<any>('/hire-purchase/', {
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
      ? recordsRaw.map((record: Record<string, unknown>) =>
          mapHirePurchaseRecord(record),
        )
      : [];

    return { records, count };
  },

  getRecord: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.get<unknown>(`/hire-purchase/${id}/`);
    const raw = unwrapApiData<Record<string, unknown>>(data);
    return mapHirePurchaseRecord(raw);
  },

  createRecord: async (
    payload: HirePurchaseFormData,
  ): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<HirePurchaseRecord>>(
      '/hire-purchase/',
      mapHirePurchaseFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as HirePurchaseRecord);
  },

  updateRecord: async (
    id: number,
    payload: Partial<HirePurchaseFormData>,
  ): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<HirePurchaseRecord>>(
      `/hire-purchase/${id}/`,
      mapHirePurchaseFormToApi(payload as unknown as Record<string, unknown>),
    );
    return data.data ?? (data as unknown as HirePurchaseRecord);
  },

  deleteRecord: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/hire-purchase/${id}/`);
  },

  confirmClosure: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<HirePurchaseRecord>>(
      `/hire-purchase/${id}/confirm-closure/`,
      { closure_confirmed: true },
    );
    const raw = (data.data ?? data) as unknown as Record<string, unknown>;
    return {
      ...(data.data ?? (data as unknown as HirePurchaseRecord)),
      status: (raw.closure_confirmed
        ? 'closed'
        : raw.is_pending_closure
          ? 'pending_closure'
          : 'active') as HirePurchaseRecord['status'],
    };
  },

  getFinanciers: async (): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>(
      '/hire-purchase/financiers/',
    );
    return data.data ?? (data as unknown as User[]);
  },
};
