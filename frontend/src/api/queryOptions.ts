/**
 * Preset cache strategies for different types of queries
 * Use these with useQuery({ ...queryOptions.dashboard, queryKey: ['key'] })
 */

export const queryOptions = {
  // Dashboard data: rarely changes, cache for 15 minutes
  dashboard: {
    staleTime: 15 * 60 * 1000,
    gcTime: 60 * 60 * 1000, // 1 hour
  },

  // Lists: changes less frequently, cache for 10 minutes
  lists: {
    staleTime: 10 * 60 * 1000,
    gcTime: 45 * 60 * 1000,
  },

  // Detail views: moderate changes, cache for 5 minutes (default)
  details: {
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  },

  // Real-time data: frequent changes, cache for 30 seconds
  realtime: {
    staleTime: 30 * 1000,
    gcTime: 5 * 60 * 1000,
  },

  // Static data: almost never changes, cache for 1 hour
  static: {
    staleTime: 60 * 60 * 1000,
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  },
};
