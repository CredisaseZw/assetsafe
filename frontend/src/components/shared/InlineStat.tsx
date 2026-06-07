interface InlineStatProps {
  label: string;
  value: string | number;
}

export function InlineStat({ label, value }: InlineStatProps) {
  return (
    <div className="flex items-baseline gap-2 border-r border-[#8f8f8f] pr-4 last:border-r-0">
      <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-600">
        {label}
      </span>
      <span className="text-lg font-black leading-none text-[#c62828]">
        {value}
      </span>
    </div>
  );
}
