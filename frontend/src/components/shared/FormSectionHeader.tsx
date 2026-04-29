import { cn } from '@/lib/utils'

interface FormSectionHeaderProps {
  title: string
  variant?: 'teal' | 'red' | 'dark'
}

export function FormSectionHeader({ title, variant = 'teal' }: FormSectionHeaderProps) {
  return (
    <div
      className={cn(
        'px-4 py-2 text-center text-sm font-semibold uppercase tracking-wider text-white',
        variant === 'teal' && 'bg-[#1a6070]',
        variant === 'red' && 'bg-red-600',
        variant === 'dark' && 'bg-[#1a1a2e]',
      )}
    >
      {title}
    </div>
  )
}
