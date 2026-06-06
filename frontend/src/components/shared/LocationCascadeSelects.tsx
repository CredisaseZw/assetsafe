import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { locationsApi } from '@/api/locationsApi';
import { FieldError } from './FieldError';
import { queryOptions } from '@/api/queryOptions';

interface Props {
  value?: number;
  onChange: (suburbId: number) => void;
  error?: string;
}

export function LocationCascadeSelects({ value, onChange, error }: Props) {
  const [countryId, setCountryId] = useState<number | ''>('');
  const [cityId, setCityId] = useState<number | ''>('');

  const { data: countries = [] } = useQuery({
    queryKey: ['countries'],
    queryFn: locationsApi.getCountries,
    ...queryOptions.static,
  });

  const { data: cities = [] } = useQuery({
    queryKey: ['cities', countryId],
    queryFn: () => locationsApi.getCities(Number(countryId)),
    enabled: !!countryId,
    ...queryOptions.static,
  });

  const { data: suburbs = [] } = useQuery({
    queryKey: ['suburbs', cityId],
    queryFn: () => locationsApi.getSuburbs(Number(cityId)),
    enabled: !!cityId,
    ...queryOptions.static,
  });

  const selectClass =
    'mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e] disabled:bg-slate-100 disabled:cursor-not-allowed';

  return (
    <>
      <div>
        <label className="text-xs font-medium text-slate-600">Country</label>
        <select
          value={countryId}
          onChange={(e) => {
            setCountryId(Number(e.target.value) || '');
            setCityId('');
            onChange(0);
          }}
          className={selectClass}
        >
          <option value="">
            {countries.length ? 'Select country…' : 'Loading…'}
          </option>
          {countries.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-xs font-medium text-slate-600">City</label>
        <select
          value={cityId}
          disabled={!countryId}
          onChange={(e) => {
            setCityId(Number(e.target.value) || '');
            onChange(0);
          }}
          className={selectClass}
        >
          <option value="">
            {!countryId
              ? 'Select country first'
              : cities.length
                ? 'Select city…'
                : 'Loading…'}
          </option>
          {cities.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-xs font-medium text-slate-600">
          Suburb<span className="text-red-500 ml-0.5">*</span>
        </label>
        <select
          value={value || ''}
          disabled={!cityId}
          onChange={(e) => onChange(Number(e.target.value))}
          className={selectClass}
        >
          <option value="">
            {!cityId
              ? 'Select city first'
              : suburbs.length
                ? 'Select suburb…'
                : 'Loading…'}
          </option>
          {suburbs.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
        <FieldError message={error} />
      </div>
    </>
  );
}
