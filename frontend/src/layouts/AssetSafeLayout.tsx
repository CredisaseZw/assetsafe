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
    <div className="min-h-screen bg-white px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
      <div className="relative mx-auto w-full max-w-[1340px] border border-[#8f8f8f] bg-white shadow-[0_12px_32px_rgba(0,0,0,0.08)]">
        <button
          type="button"
          onClick={logout}
          className="absolute right-4 top-4 z-10 inline-flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.22em] text-[#666] transition-colors hover:text-black"
        >
          <LogOut className="h-3.5 w-3.5" />
          Sign out
        </button>

        <div className="bg-black py-4 text-center text-[40px] font-black tracking-[0.08em] text-white sm:text-[46px]">
          ASSETSAFE
        </div>

        <div className="flex justify-center px-6 pt-10">
          <nav className="grid w-full max-w-[460px] grid-cols-3 text-center text-[16px] font-bold leading-none sm:text-[18px]">
            {SEGMENTS.map(({ label, path }) => {
              const isActive = location.pathname.startsWith(path);
              return (
                <NavLink
                  key={path}
                  to={path}
                  className={cn(
                    'border border-[#2a2a2a] px-4 py-2.5 text-[#111] transition-colors',
                    isActive ? 'bg-white' : 'bg-[#dcdcdc]',
                  )}
                >
                  {label}
                </NavLink>
              );
            })}
          </nav>
        </div>

        <main className="px-6 pb-10 pt-10 sm:px-8 lg:px-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
