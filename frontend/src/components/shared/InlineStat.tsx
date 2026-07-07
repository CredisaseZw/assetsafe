import { cn } from '@/lib/utils';

interface InlineStatProps {
  label: string;
  value: string | number;
  valueClassName?: string;
}

export function InlineStat({ label, value, valueClassName }: InlineStatProps) {
  return (
    <div className="flex items-center gap-2 border-r border-[#8f8f8f] pr-4 last:border-r-0">
      <span className="shrink-0 text-[11px] font-semibold uppercase tracking-wide text-slate-600">
        {label}
      </span>
      <span
        className={cn(
          'whitespace-nowrap text-lg font-black tabular-nums leading-snug text-[#c62828]',
          valueClassName,
        )}
      >
        {value}
      </span>
    </div>
  );
}
