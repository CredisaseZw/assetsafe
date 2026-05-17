import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { LogOut } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';

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
  const { logout } = useAuth();

  return (
    <SidebarProvider>
      <AppSidebar />

      <main className="main-content">
        <SidebarTrigger />
        <div className="min-h-screen bg-[#f4f1eb] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
          <div className="relative mx-auto w-full max-w-[1380px] overflow-hidden border border-[#8f8f8f] bg-white shadow-[0_12px_32px_rgba(0,0,0,0.08)]">
            <div className="border-b border-[#8f8f8f] bg-black px-6 py-4 text-white">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <div className="text-[15px] font-semibold uppercase tracking-[0.25em] text-white/80">
                    AssetSafe v1.0
                  </div>
                </div>
              </div>
            </div>

            <div className="border-b border-[#8f8f8f] bg-[#e3e0da] px-4 pt-4">
              <nav className="grid w-full max-w-[560px] grid-cols-3 text-center text-[15px] font-bold leading-none sm:text-[16px]">
                {(() => {
                  const dashboard = MENU.find(
                    (m) => (m as any).label === 'Dashboard',
                  ) as any;
                  const tabs = dashboard?.children ?? [];
                  return tabs.map(({ label, path }: any) => {
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
                  });
                })()}
              </nav>
            </div>

            <main className="px-4 pb-8 pt-6 sm:px-6 lg:px-8">
              <Outlet />
            </main>
          </div>
        </div>
      </main>
    </SidebarProvider>
  );
}
