import { cn } from '@/lib/utils';

interface StatCardProps {
  label: string;
  value: string | number;
  className?: string;
}

export function StatCard({ label, value, className }: StatCardProps) {
  return (
    <div
      className={cn(
        'flex min-h-[92px] flex-col justify-between border border-[#8f8f8f] bg-white px-4 py-3',
        className,
      )}
    >
      <span className="text-[15px] font-semibold uppercase tracking-wide text-slate-800 sm:text-[16px]">
        {label}
      </span>
      <span className="text-left text-[28px] font-black leading-none text-[#c62828] sm:text-[32px]">
        {value}
      </span>
    </div>
  );
}
