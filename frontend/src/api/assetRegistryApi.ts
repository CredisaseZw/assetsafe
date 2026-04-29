import axiosInstance from './axiosInstance'
import type {
  ApiResponse,
  AssetRegistryDashboard,
  AssetRecord,
  AssetFormData,
  AssetType,
  User,
} from '@/types'

export const assetRegistryApi = {
  getDashboard: async (params?: { asset_type?: AssetType }): Promise<AssetRegistryDashboard> => {
    const { data } = await axiosInstance.get<ApiResponse<AssetRegistryDashboard>>(
      '/assetsafe/registry/dashboard/',
      { params },
    )
    return data.data
  },

  getRecord: async (id: number): Promise<AssetRecord> => {
    const { data } = await axiosInstance.get<ApiResponse<AssetRecord>>(
      `/assetsafe/registry/${id}/`,
    )
    return data.data
  },

  createRecord: async (payload: AssetFormData): Promise<AssetRecord> => {
    const { data } = await axiosInstance.post<ApiResponse<AssetRecord>>(
      '/assetsafe/registry/',
      payload,
    )
    return data.data
  },

  updateRecord: async (id: number, payload: Partial<AssetFormData>): Promise<AssetRecord> => {
    const { data } = await axiosInstance.patch<ApiResponse<AssetRecord>>(
      `/assetsafe/registry/${id}/`,
      payload,
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
