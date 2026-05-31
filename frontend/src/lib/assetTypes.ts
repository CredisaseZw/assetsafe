export const ASSET_TYPE_OPTIONS = [
  { value: 'computers', label: 'Computers' },
  { value: 'machinery', label: 'Machinery' },
  { value: 'equipment', label: 'Equipment' },
  { value: 'vehicles', label: 'Vehicles' },
  { value: 'land', label: 'Land' },
  { value: 'building', label: 'Building' },
  { value: 'furniture', label: 'Furniture' },
  { value: 'shares', label: 'Shares' },
] as const;

export const COLLATERAL_ASSET_TYPE_OPTIONS = [
  ...ASSET_TYPE_OPTIONS,
  { value: 'inventory', label: 'Inventory' },
  { value: 'accounts_receivable', label: 'Accounts Receivable' },
] as const;

const LEGACY_LABEL_TO_VALUE: Record<string, string> = {
  Computers: 'computers',
  Machinery: 'machinery',
  Equipment: 'equipment',
  Vehicles: 'vehicles',
  Land: 'land',
  Building: 'building',
  Furniture: 'furniture',
  Shares: 'shares',
  Inventory: 'inventory',
  'Accounts Receivable': 'accounts_receivable',
};

const VALUE_TO_LABEL = Object.fromEntries(
  [...ASSET_TYPE_OPTIONS, ...COLLATERAL_ASSET_TYPE_OPTIONS].map((o) => [
    o.value,
    o.label,
  ]),
) as Record<string, string>;

export function toBackendAssetType(value: string): string {
  if (!value) return value;
  if (VALUE_TO_LABEL[value]) return value;
  return (
    LEGACY_LABEL_TO_VALUE[value] ??
    value.toLowerCase().replace(/\s+/g, '_')
  );
}

export function assetTypeLabel(value: string): string {
  return VALUE_TO_LABEL[toBackendAssetType(value)] ?? value;
}

export const ASSET_TYPE_VALUES = ASSET_TYPE_OPTIONS.map((o) => o.value);
export const COLLATERAL_ASSET_TYPE_VALUES = COLLATERAL_ASSET_TYPE_OPTIONS.map(
  (o) => o.value,
);
