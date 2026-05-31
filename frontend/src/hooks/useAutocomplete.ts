import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';

const DEFAULT_MIN_CHARS = 2;

export function useAutocomplete<T = unknown>(
  queryKeyBase: string,
  q: string,
  fetchFn: (q: string) => Promise<T[]>,
  opts?: { debounceMs?: number; minChars?: number },
) {
  const debounceMs = opts?.debounceMs ?? 300;
  const minChars = opts?.minChars ?? DEFAULT_MIN_CHARS;
  const [debounced, setDebounced] = useState(q.trim());

  useEffect(() => {
    const t = setTimeout(() => setDebounced(q.trim()), debounceMs);
    return () => clearTimeout(t);
  }, [q, debounceMs]);

  const enabled = debounced.length >= minChars;

  const query = useQuery<T[], Error>({
    queryKey: [queryKeyBase, debounced],
    queryFn: () => fetchFn(debounced),
    enabled,
    staleTime: 1000 * 60 * 2,
    gcTime: 1000 * 60 * 5,
  });

  return { ...query, enabled, minChars, debounced };
}
