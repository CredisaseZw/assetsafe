import React from 'react';
import { cn } from '@/lib/utils';

interface DateInputProps {
  label?: string;
  error?: string;
  required?: boolean;
  value?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
  name?: string;
  disabled?: boolean;
  id?: string;
  min?: string;
  max?: string;
}

const MAX_DATE_YEAR = new Date().getFullYear() + 10;

export const DateInput = React.forwardRef<HTMLInputElement, DateInputProps>(
  (
    {
      label,
      error,
      required,
      value,
      onChange,
      onBlur,
      name,
      disabled,
      id,
      min = '1990-01-01',
      max = `${MAX_DATE_YEAR}-12-31`,
    },
    ref,
  ) => {
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-');
    const isoValue =
      value && /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : '';

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label
            htmlFor={inputId}
            className="text-xs font-medium text-slate-700"
          >
            {label}
            {required && <span className="text-red-500 ml-0.5">*</span>}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          name={name}
          type="date"
          value={isoValue}
          min={min}
          max={max}
          onChange={(e) => onChange?.(e.target.value)}
          onBlur={onBlur}
          disabled={disabled}
          className={cn(
            'h-8 w-full rounded-sm border border-slate-500 bg-white px-2.5 text-sm text-slate-900',
            'focus:border-black focus:outline-none focus:ring-0',
            'disabled:cursor-not-allowed disabled:bg-slate-100',
            '[&::-webkit-calendar-picker-indicator]:cursor-pointer',
            '[&::-webkit-calendar-picker-indicator]:opacity-60',
            '[&::-webkit-calendar-picker-indicator]:hover:opacity-100',
            error && 'border-red-500 focus:border-red-500',
          )}
        />
        {error && <p className="text-xs text-red-500">{error}</p>}
      </div>
    );
  },
);
DateInput.displayName = 'DateInput';
