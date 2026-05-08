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
        'flex items-center gap-3 bg-transparent px-0 py-0',
        className,
      )}
    >
      <span className="text-[16px] font-normal text-black underline decoration-1 underline-offset-4 sm:text-[18px]">
        {label}
      </span>
      <span className="min-w-[120px] border border-[#8c8c8c] bg-white px-4 py-1.5 text-center text-[18px] font-bold text-[#d31616] sm:min-w-[135px] sm:text-[20px]">
        {value}
      </span>
    </div>
  );
}
