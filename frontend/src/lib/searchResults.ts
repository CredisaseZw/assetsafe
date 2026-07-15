/** Normalized option for owner/debtor/financier autocomplete fields. */
export interface SearchOption {
  id: number;
  name: string;
  subtitle?: string;
}

export function unwrapSearchList(data: unknown): unknown[] {
  if (Array.isArray(data)) return data;
  if (!data || typeof data !== 'object') return [];

  const obj = data as Record<string, unknown>;

  if (Array.isArray(obj.data)) return obj.data;
  if (Array.isArray(obj.results)) return obj.results;

  if (obj.data && typeof obj.data === 'object') {
    const inner = obj.data as Record<string, unknown>;
    if (Array.isArray(inner.results)) return inner.results;
    if (Array.isArray(inner.data)) return inner.data;
  }

  return [];
}

export function mapIndividualSearchResult(
  item: Record<string, unknown>,
): SearchOption {
  const first = String(item.first_name ?? '');
  const last = String(item.last_name ?? '');
  const name =
    (typeof item.name === 'string' && item.name) ||
    `${first} ${last}`.trim() ||
    `Individual #${item.id}`;

  return {
    id: Number(item.id),
    name,
    subtitle:
      (item.identification_number as string | undefined) ??
      (item.phone as string | undefined) ??
      (item.email as string | undefined),
  };
}

export function mapBranchSearchResult(
  item: Record<string, unknown>,
): SearchOption {
  const company = item.company as Record<string, unknown> | undefined;
  const branchName = String(item.branch_name ?? '').trim();
  const companyName = String(
    company?.trading_name ?? company?.registration_name ?? '',
  ).trim();
  const regNo = String(company?.registration_number ?? '').trim();
  const isHq = item.is_headquarters === true;

  const branchIsDistinct =
    Boolean(branchName) &&
    Boolean(companyName) &&
    !isHq &&
    branchName.toLowerCase() !== companyName.toLowerCase() &&
    branchName.toLowerCase() !==
      String(company?.registration_name ?? '')
        .trim()
        .toLowerCase() &&
    branchName.toLowerCase() !==
      String(company?.trading_name ?? '')
        .trim()
        .toLowerCase();

  const name = branchIsDistinct
    ? `${companyName} — ${branchName}`
    : companyName || branchName || `Branch #${item.id}`;

  return {
    id: Number(item.id),
    // Match Individual list labels: "Name (ID/Reg)".
    // Reg lives in `name` only (not also as subtitle) to avoid double display.
    name: regNo ? `${name} (${regNo})` : name,
    subtitle: undefined,
  };
}

export function mapClientSearchResult(
  item: Record<string, unknown>,
): SearchOption {
  return {
    id: Number(item.id),
    name: String(item.name ?? item.trading_name ?? `Client #${item.id}`),
    subtitle: item.external_client_id
      ? String(item.external_client_id)
      : undefined,
  };
}
