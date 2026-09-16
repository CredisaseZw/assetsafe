import type { AssetRecord } from '@/types';
import { ReportRow } from './StandViewReport';
import {
  BUILDING_BACKUP_POWER_OPTIONS,
  BUILDING_PARKING_OPTIONS,
  BUILDING_SECURITY_OPTIONS,
} from '@/lib/buildingChoices';

function featureLabel(
  options: { value: string; label: string }[],
  value?: string,
) {
  if (!value) return '';
  return options.find((option) => option.value === value)?.label ?? value;
}

export function BuildingViewReport({ detail }: { detail: AssetRecord }) {
  return (
    <div>
      <div className="bg-[#0d47a1] px-4 py-3 text-center text-[15px] font-semibold uppercase tracking-wide text-white">
        Building Report
      </div>
      <div className="space-y-1 px-4 py-3">
        <ReportRow
          label="Building Type"
          value={detail.building_type_display || detail.building_type || ''}
        />
        <ReportRow
          label="Property Details"
          value={detail.building_description ?? ''}
        />
        <ReportRow
          label="Building/Complex Name"
          value={detail.building_name ?? ''}
        />
        <ReportRow
          label="Total Units"
          value={
            detail.total_number_of_units != null
              ? String(detail.total_number_of_units)
              : ''
          }
        />
        <ReportRow
          label="Total Area (sq m)"
          value={
            detail.total_area != null && detail.total_area !== ''
              ? String(detail.total_area)
              : ''
          }
        />
        <ReportRow
          label="Year Built"
          value={
            detail.year_built != null ? String(detail.year_built) : ''
          }
        />
        <ReportRow
          label="Status"
          value={detail.building_status_display || detail.building_status || ''}
        />
        <ReportRow
          label="Furnished"
          value={detail.is_furnished ? 'Yes' : 'No'}
        />
        <ReportRow
          label="Parking"
          value={featureLabel(BUILDING_PARKING_OPTIONS, detail.feature_parking)}
        />
        <ReportRow
          label="Security"
          value={featureLabel(
            BUILDING_SECURITY_OPTIONS,
            detail.feature_security,
          )}
        />
        <ReportRow
          label="Backup Power"
          value={featureLabel(
            BUILDING_BACKUP_POWER_OPTIONS,
            detail.feature_backup_power,
          )}
        />
        <ReportRow label="Suburb/Area" value={detail.suburb_name ?? ''} />
        <ReportRow label="City/Town" value={detail.city_name ?? ''} />
        <ReportRow label="Street Address" value={detail.street_address ?? ''} />
        <ReportRow label="Postal Code" value={detail.postal_code ?? ''} />
        <ReportRow label="Stand Number" value={detail.stand_number ?? ''} />
        <ReportRow label="Owner" value={detail.owner_name} />
        {/* TODO: re-enable building valuation/title when required again
        <ReportRow label="Valuation Type" value={detail.valuation_type ?? ''} />
        <ReportRow label="Title Status" value={detail.title_status ?? ''} />
        */}
      </div>
    </div>
  );
}
