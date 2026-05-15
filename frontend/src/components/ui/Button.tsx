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
  primary: 'bg-[#196A86] hover:bg-[#15586f] text-white border-[#196A86]',
  secondary: 'bg-[#0f4f7a] hover:bg-[#0b3f61] text-white border-[#0f4f7a]',
  success: 'bg-[#137a46] hover:bg-[#0f6038] text-white border-[#137a46]',
  danger: 'bg-[#c62828] hover:bg-[#a61f1f] text-white border-[#c62828]',
  ghost: 'bg-transparent hover:bg-slate-100 text-slate-700 border-transparent',
  outline: 'bg-white hover:bg-slate-50 text-[#196A86] border-[#196A86]',
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
        'focus:ring-[#196A86]/35 disabled:cursor-not-allowed disabled:opacity-50',
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
