import axiosInstance from './axiosInstance'
import type {
  ApiResponse,
  HirePurchaseDashboard,
  HirePurchaseRecord,
  HirePurchaseFormData,
  User,
} from '@/types'

export const hirePurchaseApi = {
  getDashboard: async (params?: { financier_id?: number }): Promise<HirePurchaseDashboard> => {
    const { data } = await axiosInstance.get<ApiResponse<HirePurchaseDashboard>>(
      '/hire-purchase/stats/',
      { params },
    )
    return data.data ?? (data as unknown as HirePurchaseDashboard)
  },

  getRecords: async (params?: { financier_id?: number; search?: string }): Promise<HirePurchaseRecord[]> => {
    const { data } = await axiosInstance.get<any>('/hire-purchase/', { params })
    const payload = data?.data ?? data
    const records = payload?.results ?? payload?.data ?? payload ?? []
    if (!Array.isArray(records)) return []

    return records.map((record: any) => ({
      id: record.id,
      lodge_date: record.lodge_date,
      agreement_number: record.agreement_number,
      purchaser_name: record.purchaser_display ?? record.purchaser_name ?? '',
      purchaser_type: record.purchaser_type ?? 'individual',
      purchaser_id: record.purchaser_id ?? record.purchaser_individual ?? record.purchaser_company ?? 0,
      asset_make: record.make ?? record.asset_make ?? '',
      asset_model: record.model ?? record.asset_model ?? '',
      asset_type: record.asset_type,
      asset_year: record.year_of_make ?? record.asset_year ?? 0,
      asset_condition: record.condition ?? record.asset_condition ?? 'new',
      reg_serial_number: record.mv_registration_number ?? record.serial_number ?? record.reg_serial_number ?? '',
      chassis_number: record.chassis_number ?? '',
      engine_number: record.engine_number ?? '',
      currency: record.currency,
      purchase_amount: record.purchase_amount ?? 0,
      instalment_amount: record.instalment_amount ?? 0,
      instalment_date: record.instalment_day ?? record.instalment_date ?? 1,
      total_paid_to_date: record.total_paid_to_date ?? 0,
      balance: record.balance ?? 0,
      start_date: record.agreement_start_date ?? record.start_date ?? '',
      end_date: record.agreement_end_date ?? record.end_date ?? '',
      financier_name: record.financier_display ?? record.financier_name ?? '',
      financier_id: record.financier_id ?? 0,
      data_date: record.data_date ?? record.lodge_date ?? '',
      status: record.closure_confirmed ? 'closed' : 'active',
    }))
  },

  getRecord: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<HirePurchaseRecord>>(
      `/hire-purchase/${id}/`,
    )
    return data.data ?? (data as unknown as HirePurchaseRecord)
  },

  createRecord: async (payload: HirePurchaseFormData): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<HirePurchaseRecord>>(
      '/hire-purchase/',
      payload,
    )
    return data.data ?? (data as unknown as HirePurchaseRecord)
  },

  updateRecord: async (id: number, payload: Partial<HirePurchaseFormData>): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<HirePurchaseRecord>>(
      `/hire-purchase/${id}/`,
      payload,
    )
    return data.data ?? (data as unknown as HirePurchaseRecord)
  },

  confirmClosure: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<HirePurchaseRecord>>(
      `/hire-purchase/${id}/confirm-closure/`,
    )
    return data.data ?? (data as unknown as HirePurchaseRecord)
  },

  getFinanciers: async (): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>(
      '/hire-purchase/financiers/',
    )
    return data.data ?? (data as unknown as User[])
  },

  searchUsers: async (query: string, type?: 'individual' | 'company'): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>('/users/search/', {
      params: { q: query, type },
    })
    return data.data ?? (data as unknown as User[])
  },
}
