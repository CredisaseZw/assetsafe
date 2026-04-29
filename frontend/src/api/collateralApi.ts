import axiosInstance from './axiosInstance'
import type {
  ApiResponse,
  CollateralDashboard,
  CollateralRecord,
  CollateralFormData,
  User,
} from '@/types'

export const collateralApi = {
  getDashboard: async (params?: {
    search_field?: string
    search_value?: string
  }): Promise<CollateralDashboard> => {
    const { data } = await axiosInstance.get<ApiResponse<CollateralDashboard>>(
      '/assetsafe/collateral/dashboard/',
      { params },
    )
    return data.data
  },

  getRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<CollateralRecord>>(
      `/assetsafe/collateral/${id}/`,
    )
    return data.data
  },

  createRecord: async (payload: CollateralFormData): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<CollateralRecord>>(
      '/assetsafe/collateral/',
      payload,
    )
    return data.data
  },

  updateRecord: async (id: number, payload: Partial<CollateralFormData>): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<CollateralRecord>>(
      `/assetsafe/collateral/${id}/`,
      payload,
    )
    return data.data
  },

  dischargeRecord: async (id: number): Promise<CollateralRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<CollateralRecord>>(
      `/assetsafe/collateral/${id}/discharge/`,
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
