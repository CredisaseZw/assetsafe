import { cn } from '@/lib/utils'

interface StatCardProps {
  label: string
  value: string | number
  className?: string
}

export function StatCard({ label, value, className }: StatCardProps) {
  return (
    <div
      className={cn(
        'flex flex-col gap-0.5 rounded border border-slate-200 bg-white px-5 py-3 shadow-sm',
        className,
      )}
    >
      <span className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</span>
      <span className="text-2xl font-bold text-[#0d1f3c]">{value}</span>
    </div>
  )
}
