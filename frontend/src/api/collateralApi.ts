import axiosInstance from './axiosInstance';
import { mapCollateralFormToApi } from '@/lib/registryPayloads';
import { parsePaginatedList, unwrapApiData } from '@/lib/parsePaginatedApi';
import type {
  CollateralDashboard,
  CollateralRecord,
  CollateralFormData,
} from '@/types';

function mapCollateralRecord(
  record: Record<string, unknown>,
): CollateralRecord {
  return {
    id: Number(record.id),
    lodge_date: String(record.lodge_date ?? ''),
    agreement_number: String(record.agreement_number ?? ''),
    debtor_name: String(record.debtor_display ?? record.debtor_name ?? ''),
    debtor_type:
      (record.debtor_type as CollateralRecord['debtor_type']) ?? 'individual',
    debtor_id: Number(
      record.debtor_id ??
        record.individual_debtor ??
        record.company_debtor ??
        0,
    ),
    asset_description: String(
      record.description ?? `${record.make ?? ''} ${record.model ?? ''}`.trim(),
    ),
    asset_type: String(record.asset_type ?? ''),
    asset_make: String(record.make ?? ''),
    asset_model: String(record.model ?? ''),
    asset_year: Number(record.year_of_make ?? 0),
    asset_condition:
      (record.condition as CollateralRecord['asset_condition']) ?? 'new',
    asset_registration_no: String(
      record.asset_registration_number ?? record.primary_identifier ?? '',
    ),
    chassis_number: String(record.chassis_number ?? ''),
    engine_number: String(record.engine_number ?? ''),
    serial_number: String(
      record.serial_number ?? record.primary_identifier ?? '',
    ),
    currency: String(record.currency_code ?? record.currency ?? 'USD'),
    loan_amount: Number(record.total_debt ?? record.loan_amount ?? 0),
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
    financier_type:
      (record.financier_type as CollateralRecord['financier_type']) ??
      'company',
    financier_id: Number(record.financier ?? record.financier_id ?? 0),
    data_date: String(record.data_date ?? record.lodge_date ?? ''),
    status: record.is_discharged
      ? 'discharged'
      : record.is_pending_discharge
        ? 'pending_discharge'
        : 'active',
  };
}

export const collateralApi = {
  getDashboard: async (params?: {
    search_field?: string;
    search_value?: string;
  }): Promise<CollateralDashboard> => {
    const { data } = await axiosInstance.get('/collateral/stats/', { params });
    return unwrapApiData<CollateralDashboard>(data);
  },

  getRecords: async (params?: {
    search?: string;
    search_field?: string;
    search_value?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ records: CollateralRecord[]; count: number }> => {
    const { data } = await axiosInstance.get('/collateral/', { params });
    return parsePaginatedList(data, mapCollateralRecord);
  },

  getRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.get(`/collateral/${id}/`);
    const raw = unwrapApiData<Record<string, unknown>>(data);
    return mapCollateralRecord(raw);
  },

  createRecord: async (
    payload: CollateralFormData,
  ): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.post(
      '/collateral/',
      mapCollateralFormToApi(payload as unknown as Record<string, unknown>),
    );
    return mapCollateralRecord(unwrapApiData<Record<string, unknown>>(data));
  },

  updateRecord: async (
    id: number,
    payload: Partial<CollateralFormData>,
  ): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.patch(
      `/collateral/${id}/`,
      mapCollateralFormToApi(payload as unknown as Record<string, unknown>),
    );
    return mapCollateralRecord(unwrapApiData<Record<string, unknown>>(data));
  },

  deleteRecord: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/collateral/${id}/`);
  },

  dischargeRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.patch(`/collateral/${id}/discharge/`, {
      is_discharged: true,
    });
    return mapCollateralRecord(unwrapApiData<Record<string, unknown>>(data));
  },
};
