import React, { useEffect, useRef, useState } from 'react';
import { useAutocomplete } from '@/hooks/useAutocomplete';
import type { SearchOption } from '@/lib/searchResults';
import { cn } from '@/lib/utils';

interface Props {
  label?: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  value?: number | string;
  displayLabel?: string;
  queryKey?: string;
  minChars?: number;
  onChange?: (v: number) => void;
  onBlur?: () => void;
  fetchFn: (q: string) => Promise<SearchOption[]>;
}

export function AutocompleteInput({
  label,
  placeholder,
  error,
  required,
  value,
  displayLabel,
  queryKey = 'autocomplete',
  minChars = 2,
  onChange,
  onBlur,
  fetchFn,
}: Props) {
  const [query, setQuery] = useState(displayLabel ?? '');
  const [showList, setShowList] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (displayLabel !== undefined) {
      setQuery(displayLabel);
    }
  }, [displayLabel]);

  const {
    data: items = [],
    isFetching,
    isError,
    enabled: searchEnabled,
  } = useAutocomplete<SearchOption>(queryKey, query, fetchFn, {
    debounceMs: 300,
    minChars,
  });

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (!containerRef.current?.contains(e.target as Node)) {
        setShowList(false);
      }
    }
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, []);

  const trimmed = query.trim();
  const showPanel = showList && trimmed.length > 0;

  return (
    <div className="relative" ref={containerRef}>
      {label ? (
        <label className="text-xs font-medium text-slate-700">
          {label}
          {required ? <span className="text-red-500 ml-0.5">*</span> : null}
        </label>
      ) : null}

      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setShowList(true);
          if (!e.target.value.trim() && value) {
            onChange?.(0);
          }
        }}
        onFocus={() => setShowList(true)}
        onBlur={onBlur}
        placeholder={placeholder}
        autoComplete="off"
        className={cn(
          'h-8 w-full rounded-sm border border-slate-500 bg-white px-2.5 text-sm text-slate-900',
          'placeholder:text-slate-400 focus:border-black focus:outline-none focus:ring-0',
          error && 'border-red-500 focus:border-red-500',
        )}
      />

      {showPanel ? (
        <div className="absolute z-[60] mt-1 max-h-48 w-full overflow-auto rounded border border-slate-300 bg-white shadow-md">
          {!searchEnabled ? (
            <div className="p-2 text-sm text-slate-500">
              Type at least {minChars} characters to search
            </div>
          ) : isFetching ? (
            <div className="p-2 text-sm text-slate-500">Searching...</div>
          ) : isError ? (
            <div className="p-2 text-sm text-red-500">
              Search failed. Please try again.
            </div>
          ) : items.length > 0 ? (
            items.map((item) => (
              <button
                key={item.id}
                type="button"
                className="block w-full px-3 py-2 text-left text-sm hover:bg-slate-100"
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => {
                  setQuery(item.name);
                  setShowList(false);
                  onChange?.(item.id);
                }}
              >
                <div className="font-medium">{item.name}</div>
                {item.subtitle ? (
                  <div className="text-xs text-slate-400">{item.subtitle}</div>
                ) : null}
              </button>
            ))
          ) : (
            <div className="p-2 text-sm text-slate-500">No results found</div>
          )}
        </div>
      ) : null}

      {error ? <p className="text-xs text-red-500">{error}</p> : null}
    </div>
  );
}

export default AutocompleteInput;
