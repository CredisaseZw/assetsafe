import React, { useEffect, useRef, useState } from 'react';
import { useAutocomplete } from '@/hooks/useAutocomplete';
import { cn } from '@/lib/utils';

interface Props {
  label?: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  // control value is the selected id (number | string)
  value?: any;
  onChange?: (v: any) => void;
  onBlur?: () => void;
  // fetch function (q) => Promise<any[]>
  fetchFn: (q: string) => Promise<any[]>;
  ownerType?: 'individual' | 'company';
}

export function AutocompleteInput({
  label,
  placeholder,
  error,
  required,
  value,
  onChange,
  onBlur,
  fetchFn,
  ownerType,
}: Props) {
  const [query, setQuery] = useState('');
  const [showList, setShowList] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const {
    data: items,
    isFetching,
    isError,
    error: queryError,
  } = useAutocomplete<any>('search-users', query, (q) => fetchFn(q), {
    debounceMs: 300,
  });

  // debugging: log queries and results to console to help trace issues
  React.useEffect(() => {
    if (!query) return;

    console.debug(
      '[Autocomplete] query=',
      query,
      'items=',
      items,
      'isFetching=',
      isFetching,
      'error=',
      isError ? queryError : null,
    );
  }, [query, items, isFetching, isError, queryError]);

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (!containerRef.current) return;
      if (!containerRef.current.contains(e.target as Node)) setShowList(false);
    }
    document.addEventListener('click', onDoc);
    return () => document.removeEventListener('click', onDoc);
  }, []);

  return (
    <div className="relative" ref={containerRef}>
      {label && (
        <label className="text-xs font-medium text-slate-700">
          {label}
          {required && <span className="text-red-500 ml-0.5">*</span>}
        </label>
      )}

      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setShowList(true);
        }}
        onBlur={onBlur}
        placeholder={placeholder}
        className={cn(
          'h-8 w-full rounded-sm border border-slate-500 bg-white px-2.5 text-sm text-slate-900',
          'placeholder:text-slate-400 focus:border-black focus:outline-none focus:ring-0',
          error && 'border-red-500 focus:border-red-500',
        )}
      />

      {showList && ((Array.isArray(items) && items.length) || isFetching) ? (
        <div className="absolute z-50 mt-1 max-h-48 w-full overflow-auto rounded border bg-white shadow-sm">
          {isFetching && (
            <div className="p-2 text-sm text-slate-500">Searching...</div>
          )}
          {Array.isArray(items) && items.length > 0 ? (
            items.map((u) => {
              const display =
                u.name ??
                u.branch_name ??
                u.company?.trading_name ??
                u.registration_name ??
                u.trading_name ??
                String(u.id);
              const secondary =
                u.id_number ??
                u.reg_number ??
                u.registration_number ??
                u.external_client_id ??
                '';

              return (
                <button
                  key={u.id}
                  type="button"
                  className="block w-full px-3 py-2 text-left text-sm hover:bg-slate-100"
                  onClick={() => {
                    setQuery(display);
                    setShowList(false);
                    onChange?.(u.id);
                  }}
                >
                  <div className="font-medium">{display}</div>
                  <div className="text-xs text-slate-400">{secondary}</div>
                </button>
              );
            })
          ) : isFetching ? null : isError ? (
            <div className="p-2 text-sm text-red-500">
              Error loading results
            </div>
          ) : (
            <div className="p-2 text-sm text-slate-500">No results</div>
          )}
        </div>
      ) : null}

      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

export default AutocompleteInput;
