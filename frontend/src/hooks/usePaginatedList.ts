import { useEffect, useMemo, useRef, useState } from 'react';
import {
  keepPreviousData,
  useQuery,
  useQueryClient,
  type UseQueryOptions,
} from '@tanstack/react-query';
import { paginationPrefetchTargets } from '@/lib/pagination';

export interface PaginatedListPage<TRow> {
  rows: TRow[];
  count: number;
}

interface UsePaginatedListConfig<TResponse, TRow> extends Omit<
  UseQueryOptions<
    TResponse,
    Error,
    PaginatedListPage<TRow>,
    readonly unknown[]
  >,
  'queryKey' | 'queryFn' | 'select' | 'placeholderData'
> {
  /** Cache key for one page; must be stable per page + filters. */
  queryKeyForPage: (page: number) => readonly unknown[];
  /** Fetches one page. Used for the active query and for page prefetching. */
  fetchPage: (page: number) => Promise<TResponse>;
  /** Maps the API response to rows + total count (must be referentially stable). */
  select: (response: TResponse) => PaginatedListPage<TRow>;
  pageSize: number;
}

/**
 * Page state + list query for a numbered, paginated table.
 *
 * Keeps the previous page's rows and count visible while the next page loads
 * (`placeholderData: keepPreviousData`), so the page indicator cannot collapse
 * to page 1 mid-fetch, and warms the cache for the page numbers currently shown.
 */
export function usePaginatedList<TResponse, TRow>({
  queryKeyForPage,
  fetchPage,
  select,
  pageSize,
  enabled = true,
  ...queryOptions
}: UsePaginatedListConfig<TResponse, TRow>) {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);

  // eslint-disable-next-line @tanstack/query/exhaustive-deps -- the key is built by the caller from `page`
  const { data, isError, isLoading, isFetching } = useQuery({
    queryKey: queryKeyForPage(page),
    queryFn: () => fetchPage(page),
    select,
    placeholderData: keepPreviousData,
    enabled,
    ...queryOptions,
  });

  const rows = data?.rows ?? [];
  const count = data?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(count / pageSize));
  const activePage = Math.min(page, totalPages);
  /** Nothing to show yet: first load, or the query has not been enabled. */
  const isInitialLoading = isLoading || !enabled;
  /** A page change is in flight while the previous page's rows stay rendered. */
  const isPageLoading = isFetching && !isInitialLoading;

  // Only clamp once the loaded data actually belongs to the requested page,
  // otherwise the stale count of the previous page would snap the page back.
  useEffect(() => {
    if (isPageLoading) {
      return;
    }
    if (page > totalPages) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- clamp once the real total has landed
      setPage(totalPages);
    }
  }, [isPageLoading, page, totalPages]);

  const prefetchTargets = useMemo(
    () =>
      enabled && totalPages > 1
        ? paginationPrefetchTargets(activePage, totalPages)
        : [],
    [activePage, enabled, totalPages],
  );
  const prefetchTargetsKey = prefetchTargets.join(',');

  const latestConfig = useRef({ queryKeyForPage, fetchPage, queryOptions });
  useEffect(() => {
    latestConfig.current = { queryKeyForPage, fetchPage, queryOptions };
  });

  useEffect(() => {
    if (!prefetchTargetsKey) {
      return;
    }

    const { queryKeyForPage, fetchPage, queryOptions } = latestConfig.current;
    const targetPages = prefetchTargetsKey.split(',').map(Number);

    for (const targetPage of targetPages) {
      if (targetPage === page) {
        continue;
      }
      // prefetchQuery swallows failures: a missed prefetch is not user-facing.
      // eslint-disable-next-line @tanstack/query/exhaustive-deps -- the key is built by the caller from `targetPage`
      void queryClient.prefetchQuery({
        queryKey: queryKeyForPage(targetPage),
        queryFn: () => fetchPage(targetPage),
        ...queryOptions,
      });
    }
  }, [page, prefetchTargetsKey, queryClient]);

  return {
    page,
    setPage,
    rows,
    count,
    totalPages,
    activePage,
    startItem: count === 0 ? 0 : (activePage - 1) * pageSize + 1,
    endItem: Math.min(activePage * pageSize, count),
    isInitialLoading,
    isPageLoading,
    isError,
  };
}
