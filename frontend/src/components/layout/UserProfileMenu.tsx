import { useEffect, useRef, useState } from 'react';
import { LogOut, UserCircle } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

export function UserProfileMenu() {
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (!containerRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', onDocClick);
    return () => document.removeEventListener('mousedown', onDocClick);
  }, []);

  const displayName = user?.name || user?.username || 'User';

  return (
    <div className="relative" ref={containerRef}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex h-9 w-9 items-center justify-center rounded-full border border-sidebar-border bg-sidebar-accent text-sidebar-foreground transition-colors hover:bg-[#f3f0ea]"
        aria-label="Account menu"
        aria-expanded={open}
      >
        <UserCircle className="h-5 w-5" />
      </button>

      {open ? (
        <div
          className={cn(
            'absolute right-0 top-full z-50 mt-2 min-w-[220px] border border-[#8f8f8f] bg-white py-2 shadow-lg',
          )}
        >
          <div className="border-b border-slate-200 px-4 py-3">
            <p className="text-sm font-semibold text-slate-900">{displayName}</p>
            {user?.email ? (
              <p className="mt-0.5 text-xs text-slate-500">{user.email}</p>
            ) : null}
          </div>
          <button
            type="button"
            className="flex w-full items-center gap-2 px-4 py-2.5 text-sm font-medium text-slate-800 hover:bg-slate-50"
            onClick={async () => {
              setOpen(false);
              await logout();
            }}
          >
            <LogOut className="h-4 w-4" />
            Logout
          </button>
        </div>
      ) : null}
    </div>
  );
}
