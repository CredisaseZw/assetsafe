import type { FieldValues, Path, UseFormSetError } from 'react-hook-form';

/** Maps API / serializer field names to form field names. */
const API_FIELD_MAP: Record<string, string> = {
  individual_owner: 'owner_id',
  company_owner: 'owner_id',
  individual_debtor: 'debtor_id',
  company_debtor: 'debtor_id',
  purchaser_individual: 'purchaser_id',
  purchaser_company: 'purchaser_id',
  financier: 'financier_id',
  make: 'asset_make',
  model: 'asset_model',
  year_of_make: 'asset_year',
  condition: 'asset_condition',
  asset_registration_number: 'asset_registration_no',
  mv_registration_number: 'mv_registration_no',
  reg_serial_number: 'reg_serial_number',
  total_debt: 'loan_amount',
  instalment_day: 'instalment_date',
  agreement_start_date: 'start_date',
  agreement_end_date: 'end_date',
  subscription_start_date: 'subscription_start_date',
  subscription_end_date: 'subscription_end_date',
};

function messageFromValue(value: unknown): string {
  if (Array.isArray(value)) return String(value[0] ?? 'Invalid value');
  if (typeof value === 'string') return value;
  if (value && typeof value === 'object' && 'message' in value) {
    return String((value as { message: unknown }).message);
  }
  return 'Invalid value';
}

function flattenApiErrors(
  payload: unknown,
  prefix = '',
): { field: string; message: string }[] {
  if (!payload || typeof payload !== 'object') return [];

  const out: { field: string; message: string }[] = [];

  for (const [key, value] of Object.entries(payload as Record<string, unknown>)) {
    const path = prefix ? `${prefix}.${key}` : key;

    if (
      value &&
      typeof value === 'object' &&
      !Array.isArray(value) &&
      !(key in API_FIELD_MAP)
    ) {
      out.push(...flattenApiErrors(value, path));
      continue;
    }

    const formField = API_FIELD_MAP[key] ?? key;
    out.push({ field: formField, message: messageFromValue(value) });
  }

  return out;
}

/**
 * Applies Django / DRF validation errors to react-hook-form fields.
 * Returns true if any field error was set.
 */
export function applyApiValidationErrors<T extends FieldValues>(
  setError: UseFormSetError<T>,
  err: unknown,
): boolean {
  const data = (err as { response?: { data?: unknown } })?.response?.data;
  if (!data || typeof data !== 'object') return false;

  const body = data as Record<string, unknown>;

  // A plain string in `error` is a global message, not a field-level error.
  // Return false so the caller can show it as a toast.
  if (typeof body.error === 'string' && !body.errors) return false;

  const errorPayload =
    body.errors ??
    (typeof body.error === 'object' ? body.error : null) ??
    body;

  const flattened = flattenApiErrors(errorPayload);
  if (!flattened.length) return false;

  for (const { field, message } of flattened) {
    setError(field as Path<T>, { type: 'server', message });
  }

  return true;
}

