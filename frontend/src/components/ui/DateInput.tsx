import React, { useState, useEffect } from 'react';
import * as Popover from '@radix-ui/react-popover';
import { DayPicker } from 'react-day-picker';
import { format, parse, isValid } from 'date-fns';
import { CalendarIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import 'react-day-picker/style.css';

function toDisplay(iso: string): string {
  if (!iso || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return '';
  const [y, m, d] = iso.split('-');
  return `${d}/${m}/${y}`;
}

function toISO(display: string): string {
  const match = display.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (!match) return '';
  const [, d, m, y] = match;
  return `${y}-${m}-${d}`;
}

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
}

export const DateInput = React.forwardRef<HTMLInputElement, DateInputProps>(
  ({ label, error, required, value, onChange, onBlur, name, disabled, id }, _ref) => {
    const [display, setDisplay] = useState(() => toDisplay(value ?? ''));
    const [open, setOpen] = useState(false);

    useEffect(() => {
      setDisplay(toDisplay(value ?? ''));
    }, [value]);

    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

    const selectedDate: Date | undefined = (() => {
      if (value && /^\d{4}-\d{2}-\d{2}$/.test(value)) {
        const d = new Date(value + 'T00:00:00');
        return isValid(d) ? d : undefined;
      }
      return undefined;
    })();

    const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      let digits = e.target.value.replace(/\D/g, '');
      if (digits.length > 8) digits = digits.slice(0, 8);

      let formatted = digits;
      if (digits.length > 4) {
        formatted = `${digits.slice(0, 2)}/${digits.slice(2, 4)}/${digits.slice(4)}`;
      } else if (digits.length > 2) {
        formatted = `${digits.slice(0, 2)}/${digits.slice(2)}`;
      }

      setDisplay(formatted);
      onChange?.(toISO(formatted));
    };

    const handleDaySelect = (day: Date | undefined) => {
      if (!day) return;
      const iso = format(day, 'yyyy-MM-dd');
      const disp = format(day, 'dd/MM/yyyy');
      setDisplay(disp);
      onChange?.(iso);
      setOpen(false);
    };

    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label htmlFor={inputId} className="text-xs font-medium text-slate-700">
            {label}
            {required && <span className="text-red-500 ml-0.5">*</span>}
          </label>
        )}
        <div className="relative flex items-center">
          <input
            id={inputId}
            name={name}
            type="text"
            inputMode="numeric"
            placeholder="dd/mm/yyyy"
            value={display}
            onChange={handleTextChange}
            onBlur={onBlur}
            disabled={disabled}
            maxLength={10}
            className={cn(
              'h-8 w-full rounded-sm border border-slate-500 bg-white pl-2.5 pr-8 text-sm text-slate-900',
              'placeholder:text-slate-400 focus:border-black focus:outline-none focus:ring-0',
              'disabled:cursor-not-allowed disabled:bg-slate-100',
              error && 'border-red-500 focus:border-red-500',
            )}
          />
          <Popover.Root open={open} onOpenChange={setOpen}>
            <Popover.Trigger asChild>
              <button
                type="button"
                disabled={disabled}
                className="absolute right-1.5 flex h-5 w-5 items-center justify-center rounded text-slate-400 hover:text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <CalendarIcon className="h-3.5 w-3.5" />
              </button>
            </Popover.Trigger>
            <Popover.Portal>
              <Popover.Content
                align="start"
                sideOffset={6}
                className="z-[9999] rounded border border-slate-200 bg-white shadow-lg"
              >
                <DayPicker
                  mode="single"
                  selected={selectedDate}
                  onSelect={handleDaySelect}
                  defaultMonth={selectedDate ?? new Date()}
                  captionLayout="dropdown"
                  startMonth={new Date(1990, 0)}
                  endMonth={new Date(2100, 11)}
                  classNames={{
                    root: 'p-3 text-sm',
                    month_caption: 'flex items-center justify-between mb-2 px-1',
                    dropdowns: 'flex gap-1',
                    dropdown: 'rounded border border-slate-300 bg-white px-1 py-0.5 text-xs',
                    nav: 'flex gap-1',
                    button_previous: 'rounded p-1 hover:bg-slate-100',
                    button_next: 'rounded p-1 hover:bg-slate-100',
                    month_grid: 'w-full border-collapse',
                    weekdays: 'flex',
                    weekday: 'w-8 text-center text-xs text-slate-400 font-normal pb-1',
                    weeks: '',
                    week: 'flex',
                    day: 'w-8 h-8 flex items-center justify-center',
                    day_button: 'w-8 h-8 rounded text-xs hover:bg-slate-100 focus:outline-none',
                    selected: '[&>button]:bg-[#0f7d8e] [&>button]:text-white [&>button]:hover:bg-[#0c6a79]',
                    today: '[&>button]:font-bold [&>button]:text-[#0f7d8e]',
                    outside: 'opacity-30',
                    disabled: 'opacity-30 cursor-not-allowed',
                  }}
                />
                <Popover.Arrow className="fill-slate-200" />
              </Popover.Content>
            </Popover.Portal>
          </Popover.Root>
        </div>
        {error && <p className="text-xs text-red-500">{error}</p>}
      </div>
    );
  },
);
DateInput.displayName = 'DateInput';
