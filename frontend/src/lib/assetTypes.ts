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

const VALUE_TO_LABEL: Record<string, string> = {
  computers: 'Computers',
  machinery: 'Machinery',
  equipment: 'Equipment',
  vehicles: 'Vehicles',
  land: 'Land',
  building: 'Building',
  furniture: 'Furniture',
  shares: 'Shares',
  inventory: 'Inventory',
  accounts_receivable: 'Accounts Receivable',
};

export function toBackendAssetType(value: string): string {
  if (!value) return value;
  if (VALUE_TO_LABEL[value]) return value;
  return (
    LEGACY_LABEL_TO_VALUE[value] ?? value.toLowerCase().replace(/\s+/g, '_')
  );
}

export function assetTypeLabel(value: string): string {
  return VALUE_TO_LABEL[toBackendAssetType(value)] ?? value;
}
