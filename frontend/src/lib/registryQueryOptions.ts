/** TanStack Query defaults for registry list/dashboard fetches. */
export const registryQueryOptions = {
  staleTime: 5 * 60 * 1000, // 5 minutes
  gcTime: 30 * 60 * 1000, // 30 minutes
  refetchOnMount: true,
  refetchOnWindowFocus: false,
};
