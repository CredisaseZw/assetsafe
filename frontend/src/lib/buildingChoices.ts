import type { ChoiceOption } from '@/api/commonApi';

export const BUILDING_PARKING_OPTIONS: ChoiceOption[] = [
  { value: 'all', label: 'All' },
  { value: 'underground', label: 'Underground' },
  { value: 'integrated_garage', label: 'Integrated Garage' },
  { value: 'external_garage', label: 'External Garage' },
  { value: 'open', label: 'Open' },
  { value: 'street', label: 'Street' },
];

export const BUILDING_SECURITY_OPTIONS: ChoiceOption[] = [
  { value: '24/7', label: '24/7' },
  { value: 'day_time', label: 'Day Time' },
  { value: 'night_time', label: 'Night Time' },
  { value: 'none', label: 'None' },
];

export const BUILDING_BACKUP_POWER_OPTIONS: ChoiceOption[] = [
  { value: 'all', label: 'All' },
  { value: 'generator', label: 'Generator' },
  { value: 'solar', label: 'Solar' },
  { value: 'battery', label: 'Battery' },
  { value: 'none', label: 'None' },
];

export const BUILDING_STATUS_FALLBACK: ChoiceOption[] = [
  { value: 'vacant', label: 'Vacant' },
  { value: 'partially_occupied', label: 'Partially Occupied' },
  { value: 'occupied', label: 'Occupied' },
  { value: 'maintenance', label: 'Maintenance' },
  { value: 'sold', label: 'Sold' },
];

export const BUILDING_TYPE_FALLBACK: ChoiceOption[] = [
  { value: 'residential_house', label: 'Residential - House' },
  { value: 'residential_cottage', label: 'Residential - Cottage' },
  { value: 'residential_townhouse', label: 'Residential - Townhouse' },
  { value: 'residential_flat', label: 'Residential - Flat' },
  {
    value: 'residential_small_holding',
    label: 'Residential - Small Holding',
  },
  { value: 'commercial_offices', label: 'Commercial - Offices' },
  { value: 'commercial_retail', label: 'Commercial - Retail' },
  { value: 'commercial_industrial', label: 'Commercial - Industrial' },
  { value: 'commercial_warehouse', label: 'Commercial - Warehouse' },
  { value: 'commercial_hospitality', label: 'Commercial - Hospitality' },
  { value: 'institutional_education', label: 'Institutional - Education' },
  { value: 'institutional_medical', label: 'Institutional - Medical' },
  { value: 'agricultural_warehouse', label: 'Agricultural - Warehouse' },
  { value: 'agricultural_greenhouse', label: 'Agricultural - Greenhouse' },
];
