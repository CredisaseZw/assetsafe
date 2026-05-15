import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { queryOptions } from './queryOptions';

interface PaginationParams {
  page: number;
  limit: number;
  search?: string;
  filters?: Record<string, any>;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

/**
 * Hook for paginated queries with intelligent caching
 *
 * Each page/filter combination is cached independently, so:
 * - Returning to page 1 hits the cache
 * - Switching filters caches separately
 * - No unnecessary API calls for already-cached pages
 *
 * Usage:
 * const { data, isLoading } = usePaginatedQuery(
 *   ['collateral-records'],
 *   (params) => fetchCollateralRecords(params),
 *   { page: 1, limit: 10 },
 * );
 */
export function usePaginatedQuery<T>(
  baseQueryKey: string[],
  queryFn: (params: PaginationParams) => Promise<PaginatedResponse<T>>,
  params: PaginationParams,
  options?: Omit<UseQueryOptions, 'queryKey' | 'queryFn'>,
) {
  return useQuery({
    // Create unique cache key per page/filter combination
    queryKey: [
      ...baseQueryKey,
      {
        page: params.page,
        limit: params.limit,
        search: params.search,
        filters: params.filters,
      },
    ],
    queryFn: () => queryFn(params),
    // Use list caching by default for paginated data
    ...queryOptions.lists,
    // Allow override
    ...options,
  });
}

/**
 * Hook for dashboard/summary data with longer cache
 *
 * Usage:
 * const { data } = useDashboardQuery(
 *   ['hp-dashboard'],
 *   fetchHPDashboard,
 * );
 */
export function useDashboardQuery<T>(
  queryKey: string[],
  queryFn: () => Promise<T>,
  options?: Omit<UseQueryOptions, 'queryKey' | 'queryFn'>,
) {
  return useQuery({
    queryKey,
    queryFn,
    ...queryOptions.dashboard,
    ...options,
  });
}

/**
 * Hook for static/lookup data with very long cache
 *
 * Usage:
 * const { data: assetTypes } = useStaticQuery(
 *   ['asset-types'],
 *   fetchAssetTypes,
 * );
 */
export function useStaticQuery<T>(
  queryKey: string[],
  queryFn: () => Promise<T>,
  options?: Omit<UseQueryOptions, 'queryKey' | 'queryFn'>,
) {
  return useQuery({
    queryKey,
    queryFn,
    ...queryOptions.static,
    ...options,
  });
}
