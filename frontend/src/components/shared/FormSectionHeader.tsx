import { cn } from '@/lib/utils';

interface FormSectionHeaderProps {
  title: string;
  variant?: 'teal' | 'red' | 'dark';
}

export function FormSectionHeader({
  title,
  variant = 'teal',
}: FormSectionHeaderProps) {
  return (
    <div
      className={cn(
        'px-4 py-2 text-center text-sm font-bold uppercase tracking-wider text-white sm:text-[15px]',
        variant === 'teal' && 'bg-[#7f7a7b]',
        variant === 'red' && 'bg-[#c81f1f]',
        variant === 'dark' && 'bg-black',
      )}
    >
      {title}
    </div>
  );
}
