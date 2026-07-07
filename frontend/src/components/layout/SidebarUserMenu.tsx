import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { LogOut, UserCircle } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/store';
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';

type MenuPosition = {
  top: number;
  left: number;
  transform: string;
};

export function SidebarUserMenu() {
  const { user } = useAuthStore();
  const { logout } = useAuth();
  const { state, isMobile } = useSidebar();
  const [open, setOpen] = useState(false);
  const [menuPosition, setMenuPosition] = useState<MenuPosition | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const collapsed = state === 'collapsed' && !isMobile;

  const displayName = user?.name || user?.username || 'User';

  const updateMenuPosition = useCallback(() => {
    const el = containerRef.current;
    if (!el) {
      return;
    }

    const rect = el.getBoundingClientRect();
    setMenuPosition(
      collapsed
        ? {
            // Match original collapsed placement: to the right, bottom-aligned.
            top: rect.bottom,
            left: rect.right + 8,
            transform: 'translateY(-100%)',
          }
        : {
            top: rect.top - 8,
            left: rect.left,
            transform: 'translateY(-100%)',
          },
    );
  }, [collapsed]);

  useLayoutEffect(() => {
    if (!open) {
      return;
    }

    updateMenuPosition();
    window.addEventListener('resize', updateMenuPosition);
    window.addEventListener('scroll', updateMenuPosition, true);

    return () => {
      window.removeEventListener('resize', updateMenuPosition);
      window.removeEventListener('scroll', updateMenuPosition, true);
    };
  }, [open, updateMenuPosition]);

  useEffect(() => {
    if (!open) {
      setMenuPosition(null);
    }
  }, [open]);

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      const target = e.target as Node;
      if (
        containerRef.current?.contains(target) ||
        menuRef.current?.contains(target)
      ) {
        return;
      }
      setOpen(false);
    }

    document.addEventListener('mousedown', onDocClick);
    return () => document.removeEventListener('mousedown', onDocClick);
  }, []);

  const handleToggle = () => {
    setOpen((v) => !v);
  };

  const menu =
    open && menuPosition
      ? createPortal(
          <div
            ref={menuRef}
            role="menu"
            className="fixed z-[200] min-w-[220px] border border-[#8f8f8f] bg-white py-2 shadow-lg"
            style={{
              top: menuPosition.top,
              left: menuPosition.left,
              transform: menuPosition.transform,
            }}
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
              className="flex w-full cursor-pointer items-center gap-2 px-4 py-2.5 text-sm font-medium text-[#c62828] hover:bg-red-100"
              onClick={async () => {
                setOpen(false);
                await logout();
              }}
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>,
          document.body,
        )
      : null;

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <div className="relative" ref={containerRef}>
          <SidebarMenuButton
            type="button"
            size="lg"
            tooltip={displayName}
            onClick={handleToggle}
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
          {menu}
        </div>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
