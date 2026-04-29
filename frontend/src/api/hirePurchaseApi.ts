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
      '/assetsafe/hire-purchase/dashboard/',
      { params },
    )
    return data.data
  },

  getRecord: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<HirePurchaseRecord>>(
      `/assetsafe/hire-purchase/${id}/`,
    )
    return data.data
  },

  createRecord: async (payload: HirePurchaseFormData): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<HirePurchaseRecord>>(
      '/assetsafe/hire-purchase/',
      payload,
    )
    return data.data
  },

  updateRecord: async (id: number, payload: Partial<HirePurchaseFormData>): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<HirePurchaseRecord>>(
      `/assetsafe/hire-purchase/${id}/`,
      payload,
    )
    return data.data
  },

  confirmClosure: async (id: number): Promise<HirePurchaseRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<HirePurchaseRecord>>(
      `/assetsafe/hire-purchase/${id}/confirm-closure/`,
    )
    return data.data
  },

  getFinanciers: async (): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>(
      '/assetsafe/hire-purchase/financiers/',
    )
    return data.data
  },

  searchUsers: async (query: string, type?: 'individual' | 'company'): Promise<User[]> => {
    const { data } = await axiosInstance.get<ApiResponse<User[]>>('/users/search/', {
      params: { q: query, type },
    })
    return data.data
  },
}
