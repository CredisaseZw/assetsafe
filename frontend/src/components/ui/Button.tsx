import React from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | 'primary'
    | 'secondary'
    | 'success'
    | 'danger'
    | 'ghost'
    | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
}

const variantClasses = {
  primary: 'bg-[#1f6f93] hover:bg-[#175873] text-white border-[#1f6f93]',
  secondary: 'bg-[#0b4f86] hover:bg-[#093c67] text-white border-[#0b4f86]',
  success: 'bg-[#10b54b] hover:bg-[#0f993f] text-white border-[#10b54b]',
  danger: 'bg-red-600 hover:bg-red-700 text-white border-transparent',
  ghost: 'bg-transparent hover:bg-slate-100 text-slate-700 border-transparent',
  outline: 'bg-white hover:bg-slate-50 text-[#1f6f93] border-[#1f6f93]',
};

const sizeClasses = {
  sm: 'text-xs px-2.5 py-1.5 h-7',
  md: 'text-sm px-4 py-2 h-9',
  lg: 'text-sm px-5 py-2.5 h-10',
};

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  leftIcon,
  className,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-1.5 rounded-sm border font-semibold',
        'transition-colors duration-150 focus:outline-none focus:ring-2',
        'focus:ring-[#1f6f93]/35 disabled:cursor-not-allowed disabled:opacity-50',
        variantClasses[variant],
        sizeClasses[size],
        className,
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : leftIcon}
      {children}
    </button>
  );
}
