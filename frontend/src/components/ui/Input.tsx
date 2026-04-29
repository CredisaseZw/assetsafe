import React from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  required?: boolean
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, required, className, id, ...props }, ref) => {
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-')
    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label htmlFor={inputId} className="text-xs font-medium text-slate-600">
            {label}
            {required && <span className="text-red-500 ml-0.5">*</span>}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            'h-8 rounded border border-slate-300 bg-white px-2.5 text-sm text-slate-800',
            'placeholder:text-slate-400 focus:border-[#0f7d8e] focus:outline-none focus:ring-1',
            'focus:ring-[#0f7d8e]/30 disabled:bg-slate-100 disabled:cursor-not-allowed',
            error && 'border-red-400 focus:border-red-400 focus:ring-red-400/20',
            className,
          )}
          {...props}
        />
        {error && <p className="text-xs text-red-500">{error}</p>}
      </div>
    )
  },
)
Input.displayName = 'Input'
