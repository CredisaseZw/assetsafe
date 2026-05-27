import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { MobileBlocker } from '@/components/MobileBlocker';

const MENU = [
  {
    label: 'Dashboard',
    children: [
      { label: 'Asset', path: '/registry' },
      { label: 'Collateral', path: '/collateral' },
      { label: 'HP', path: '/hire-purchase' },
    ],
  },
  { label: 'Report', path: '/reports' },
] as const;

export default function AssetSafeLayout() {
  const location = useLocation();

  const dashboardTabs = MENU[0].children;

  return (
    <SidebarProvider>
      <AppSidebar />

      <main className="flex h-screen flex-1 flex-col overflow-hidden">
        <div className="shrink-0 border-b border-[#8f8f8f] bg-sidebar px-6 py-4 text-sidebar-foreground">
          <div className="grid grid-cols-[auto_1fr_auto] items-center gap-4">
            <div>
              <SidebarTrigger />
            </div>
            <div className="justify-self-center">
              <div className="text-[15px] font-semibold uppercase tracking-[0.25em] text-sidebar-foreground/90">
                AssetSafe
              </div>
            </div>
            <div className="justify-self-end" />
          </div>
        </div>
        <div className="flex min-h-0 flex-1 overflow-hidden bg-[#f4f1eb] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
          <MobileBlocker />
          <div className="relative mx-auto flex h-full w-full max-w-[1380px] min-h-0 flex-col overflow-hidden border border-[#8f8f8f] bg-white shadow-[0_12px_32px_rgba(0,0,0,0.08)]">
            <div className="border-b border-[#8f8f8f] bg-[#e3e0da] px-4 pt-4">
              <nav className="grid w-full max-w-[560px] grid-cols-3 text-center text-[15px] font-bold leading-none sm:text-[16px]">
                {dashboardTabs.map(({ label, path }) => {
                  const isActive = location.pathname.startsWith(path);
                  return (
                    <NavLink
                      key={path}
                      to={path}
                      className={cn(
                        'border border-[#8f8f8f] border-b-0 px-4 py-3 text-[#111] transition-colors',
                        isActive
                          ? 'bg-white'
                          : 'bg-[#d1cec8] hover:bg-[#ddd9d2]',
                      )}
                    >
                      {label}
                    </NavLink>
                  );
                })}
              </nav>
            </div>

            <main className="flex min-h-0 flex-1 flex-col overflow-hidden px-4 pb-8 pt-6 sm:px-6 lg:px-8">
              <Outlet />
            </main>
          </div>
        </div>
      </main>
    </SidebarProvider>
  );
}
