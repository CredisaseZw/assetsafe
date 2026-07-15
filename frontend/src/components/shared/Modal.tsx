import React, { useEffect, useRef, useState } from 'react';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  disableBackdropClose?: boolean;
  /** Vertically center the panel (default: top with offset). */
  centered?: boolean;
  /** Allow dragging the panel by its header. */
  draggable?: boolean;
}

const sizeMap = {
  sm: 'max-w-md',
  md: 'max-w-2xl',
  lg: 'max-w-4xl',
  xl: 'max-w-6xl',
};

export function Modal({
  open,
  onClose,
  title,
  children,
  size = 'lg',
  disableBackdropClose = false,
  centered = false,
  draggable = false,
}: ModalProps) {
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const dragRef = useRef<{
    startX: number;
    startY: number;
    origX: number;
    origY: number;
  } | null>(null);

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    setOffset({ x: 0, y: 0 });
    return () => {
      document.body.style.overflow = prev || '';
    };
  }, [open]);

  useEffect(() => {
    if (!open || !draggable) return;

    const onMove = (e: MouseEvent) => {
      if (!dragRef.current) return;
      setOffset({
        x: dragRef.current.origX + e.clientX - dragRef.current.startX,
        y: dragRef.current.origY + e.clientY - dragRef.current.startY,
      });
    };
    const onUp = () => {
      dragRef.current = null;
    };

    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [open, draggable]);

  if (!open) return null;

  return (
    <div
      className={cn(
        'fixed inset-0 z-50 flex justify-center overflow-y-auto bg-black/45 p-4',
        centered ? 'items-center' : 'items-start pt-16',
      )}
      onClick={(e) =>
        !disableBackdropClose && e.target === e.currentTarget && onClose()
      }
    >
      <div
        className={cn(
          'relative w-full border border-[#8f8f8f] bg-white shadow-2xl',
          sizeMap[size],
        )}
        style={
          draggable
            ? { transform: `translate(${offset.x}px, ${offset.y}px)` }
            : undefined
        }
      >
        {/* Header */}
        <div
          className={cn(
            'flex items-center justify-between bg-black px-4 py-3',
            draggable && 'cursor-move select-none',
          )}
          onMouseDown={
            draggable
              ? (e) => {
                  // Don't start a drag when clicking the close button.
                  if ((e.target as HTMLElement).closest('button')) return;
                  dragRef.current = {
                    startX: e.clientX,
                    startY: e.clientY,
                    origX: offset.x,
                    origY: offset.y,
                  };
                }
              : undefined
          }
        >
          <h2 className="text-sm font-bold uppercase tracking-wide text-white">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="text-slate-300 transition-colors hover:text-white"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        {/* Content */}
        <div className="p-0">{children}</div>
      </div>
    </div>
  );
}
