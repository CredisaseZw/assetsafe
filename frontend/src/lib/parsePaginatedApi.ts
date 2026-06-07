/** Normalise DRF paginated list responses (`{ count, results }` or wrapped variants). */
export function parsePaginatedList<T>(
  data: unknown,
  mapRecord: (row: Record<string, unknown>) => T,
): { records: T[]; count: number } {
  const root =
    data && typeof data === 'object' ? (data as Record<string, unknown>) : {};

  const payload =
    root.data && typeof root.data === 'object' && !Array.isArray(root.data)
      ? (root.data as Record<string, unknown>)
      : root;

  const recordsRaw =
    (Array.isArray(payload.results) && payload.results) ||
    (Array.isArray(root.results) && root.results) ||
    (Array.isArray(payload.data) && payload.data) ||
    (Array.isArray(root.data) && root.data) ||
    (Array.isArray(payload) && payload) ||
    [];

  const count =
    typeof payload.count === 'number'
      ? payload.count
      : typeof root.count === 'number'
        ? root.count
        : recordsRaw.length;

  return {
    records: recordsRaw.map((row) => mapRecord(row as Record<string, unknown>)),
    count,
  };
}

/** Unwrap `{ data: T }` API envelopes or return the body as-is. */
export function unwrapApiData<T>(data: unknown): T {
  if (
    data &&
    typeof data === 'object' &&
    'data' in data &&
    (data as { data?: unknown }).data !== undefined &&
    !Array.isArray((data as { data?: unknown }).data)
  ) {
    return (data as { data: T }).data;
  }
  return data as T;
}
