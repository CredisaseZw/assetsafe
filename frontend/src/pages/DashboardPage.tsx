import { Link } from 'react-router-dom';
import { Building2, Car, UserPlus } from 'lucide-react';
import { toast } from 'sonner';
import { useIsStaff } from '@/hooks/useIsStaff';

const TILES = [
  {
    key: 'individuals',
    label: 'Individuals',
    icon: UserPlus,
    href: null as string | null,
    comingSoon: true,
  },
  {
    key: 'companies',
    label: 'Companies',
    icon: Building2,
    href: null as string | null,
    comingSoon: true,
  },
  {
    key: 'assets',
    label: 'Assets',
    icon: Car,
    href: '/enquiries/assets',
    comingSoon: false,
  },
] as const;

export default function DashboardPage() {
  const isStaff = useIsStaff();

  return (
    <div className="flex min-h-0 flex-1 flex-col overflow-auto p-6">
      <h1 className="mb-6 text-center text-sm font-bold uppercase tracking-[0.2em] text-slate-700">
        Dashboard
      </h1>

      <div className="mx-auto w-full max-w-3xl overflow-hidden rounded border border-[#8f8f8f] bg-white shadow-sm">
        <div className="bg-[#006680] px-4 py-3 text-center text-[15px] font-semibold text-white">
          Enquiries
        </div>
        <div className="grid grid-cols-3 divide-x divide-[#cfcfcf]">
          {TILES.map(({ key, label, icon: Icon, href, comingSoon }) => {
            const body = (
              <div className="flex flex-col items-center gap-2 px-4 py-8 text-[#1a6a9a] transition-colors hover:bg-[#f3f8fa]">
                <Icon className="size-8" strokeWidth={1.5} />
                <span className="text-sm font-semibold">{label}</span>
              </div>
            );

            if (comingSoon || !href) {
              return (
                <button
                  key={key}
                  type="button"
                  className="w-full"
                  onClick={() =>
                    toast.message('Bureau enquiries coming soon')
                  }
                >
                  {body}
                </button>
              );
            }

            const to =
              isStaff && key === 'assets'
                ? '/enquiries/assets/type'
                : href;

            return (
              <Link key={key} to={to} className="block">
                {body}
              </Link>
            );
          })}
        </div>
      </div>

      <p className="mx-auto mt-4 max-w-3xl text-center text-xs text-slate-500">
        Statistics and graphs will appear on this landing page in a later
        release.
      </p>
    </div>
  );
}
