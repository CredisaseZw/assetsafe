import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';

export function useAutocomplete<T = any>(
  queryKeyBase: string,
  q: string,
  fetchFn: (q: string) => Promise<T[]>,
  opts?: { debounceMs?: number },
) {
  const debounceMs = opts?.debounceMs ?? 300;
  const [debounced, setDebounced] = useState(q);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(q), debounceMs);
    return () => clearTimeout(t);
  }, [q, debounceMs]);

  const enabled = Boolean(debounced && debounced.length >= 3);

  const query = useQuery<T[], Error>({
    queryKey: [queryKeyBase, debounced],
    queryFn: () => fetchFn(debounced),
    enabled,
    staleTime: 1000 * 60 * 5,
    keepPreviousData: true,
  });

  return query;
}
