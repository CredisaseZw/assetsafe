import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';

const SEGMENTS = [
  { label: 'Collateral', path: '/assetsafe/collateral' },
  { label: 'HP', path: '/assetsafe/hire-purchase' },
  { label: 'Registry', path: '/assetsafe/registry' },
] as const;

export default function AssetSafeLayout() {
  const location = useLocation();
  const { logout } = useAuth();

  return (
    <div className="app-layout">
      <aside className="left-nav h-screen" aria-label="Primary navigation">
        <div className="nav-brand">ASSETSAFE</div>
        <nav className="flex-1">
          {SEGMENTS.map(({ label, path }) => {
            const isActive = location.pathname.startsWith(path);
            return (
              <NavLink
                key={path}
                to={path}
                className={cn(
                  'px-4 py-2.5 transition-colors',
                  isActive ? 'bg-white text-[#111]' : 'text-white/95',
                )}
              >
                {label}
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-auto pt-4">
          <button
            type="button"
            onClick={logout}
            className="inline-flex items-center gap-2 rounded-sm px-3 py-2 text-sm font-semibold text-white/90 transition-colors hover:bg-white/10 hover:text-white focus:outline-none focus:ring-2 focus:ring-white/30"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="main-content">
        <div className="min-h-screen bg-[#f4f1eb] px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
          <div className="relative mx-auto w-full max-w-[1380px] overflow-hidden border border-[#8f8f8f] bg-white shadow-[0_12px_32px_rgba(0,0,0,0.08)]">
            <div className="border-b border-[#8f8f8f] bg-black px-6 py-4 text-white">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <div className="text-[15px] font-semibold uppercase tracking-[0.25em] text-white/80">
                    AssetSafe
                  </div>
                  <div className="text-[30px] font-black leading-none sm:text-[36px]">
                    Registry Workspace
                  </div>
                </div>
              </div>
            </div>

            <div className="border-b border-[#8f8f8f] bg-[#e3e0da] px-4 pt-4">
              <nav className="grid w-full max-w-[560px] grid-cols-3 text-center text-[15px] font-bold leading-none sm:text-[16px]">
                {SEGMENTS.map(({ label, path }) => {
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

            <main className="px-4 pb-8 pt-6 sm:px-6 lg:px-8">
              <Outlet />
            </main>
          </div>
        </div>
      </main>
    </div>
  );
}
