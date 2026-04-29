import React from 'react'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ModalProps {
  open: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const sizeMap = {
  sm: 'max-w-md',
  md: 'max-w-2xl',
  lg: 'max-w-4xl',
  xl: 'max-w-6xl',
}

export function Modal({ open, onClose, title, children, size = 'lg' }: ModalProps) {
  if (!open) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/50 p-4 pt-16"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        className={cn(
          'relative w-full rounded-lg bg-white shadow-2xl',
          sizeMap[size],
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between bg-[#0d1f3c] px-4 py-3 rounded-t-lg">
          <h2 className="text-sm font-semibold text-white uppercase tracking-wide">{title}</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        {/* Content */}
        <div className="p-0">{children}</div>
      </div>
    </div>
  )
}
