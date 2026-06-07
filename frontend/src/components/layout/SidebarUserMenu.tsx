import { useEffect, useRef, useState } from 'react';
import { LogOut, UserCircle } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/store';
import { cn } from '@/lib/utils';
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';

export function SidebarUserMenu() {
  const { user } = useAuthStore();
  const { logout } = useAuth();
  const { state, isMobile } = useSidebar();
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const collapsed = state === 'collapsed' && !isMobile;

  const displayName = user?.name || user?.username || 'User';

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (!containerRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', onDocClick);
    return () => document.removeEventListener('mousedown', onDocClick);
  }, []);

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <div className="relative" ref={containerRef}>
          <SidebarMenuButton
            type="button"
            size="lg"
            tooltip={displayName}
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-haspopup="menu"
            className="group-data-[collapsible=icon]:justify-center"
          >
            <span className="flex size-8 shrink-0 items-center justify-center rounded-full border border-sidebar-border bg-[#f3f0ea] text-[#0f7d8e]">
              <UserCircle className="size-4" />
            </span>
            <span className="truncate text-sm font-semibold group-data-[collapsible=icon]:hidden">
              {displayName}
            </span>
          </SidebarMenuButton>

          {open ? (
            <div
              role="menu"
              className={cn(
                'absolute z-50 min-w-[220px] border border-[#8f8f8f] bg-white py-2 shadow-lg',
                collapsed
                  ? 'bottom-0 left-full ml-2'
                  : 'bottom-full left-0 mb-2',
              )}
            >
              <div className="border-b border-slate-200 px-4 py-3">
                <p className="text-sm font-semibold text-slate-900">
                  {displayName}
                </p>
                {user?.email ? (
                  <p className="mt-0.5 truncate text-xs text-slate-500">
                    {user.email}
                  </p>
                ) : null}
              </div>
              <button
                type="button"
                role="menuitem"
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
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
