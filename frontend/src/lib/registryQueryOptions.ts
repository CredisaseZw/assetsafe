/** TanStack Query defaults for registry list/dashboard fetches. */
export const registryQueryOptions = {
  staleTime: 0,
  refetchOnMount: 'always' as const,
  refetchOnWindowFocus: false,
};
