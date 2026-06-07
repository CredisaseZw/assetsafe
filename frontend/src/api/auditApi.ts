import axiosInstance from './axiosInstance';

export interface AuditLogEntry {
  id: number;
  timestamp: string;
  created_by: number | null;
  created_by_username: string | null;
  action: string;
  resource_type: string;
  resource_id: string | null;
  details: Record<string, unknown> | null;
  ip_address: string | null;
  user_agent: string | null;
  success: boolean;
}

export const auditApi = {
  list: async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    resource_type?: string;
    success?: boolean;
  }): Promise<{ results: AuditLogEntry[]; count: number }> => {
    const { data } = await axiosInstance.get<{
      count: number;
      results: AuditLogEntry[];
    }>('/audit-log/', { params });
    return { results: data.results ?? [], count: data.count ?? 0 };
  },
};
