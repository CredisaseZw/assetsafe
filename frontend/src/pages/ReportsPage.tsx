import { BarChart3 } from 'lucide-react';

export default function ReportsPage() {
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Reports</h1>
        <p className="text-sm text-slate-600">
          Registry analytics and export tools.
        </p>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center rounded border border-dashed border-[#8f8f8f] bg-[#f7f5f1] px-6 py-16 text-center">
        <BarChart3 className="mb-4 h-12 w-12 text-slate-400" />
        <h2 className="text-lg font-semibold text-slate-800">Coming soon</h2>
        <p className="mt-2 max-w-md text-sm text-slate-600">
          Report dashboards and downloads are not available yet. Check back here
          for collateral, hire purchase, and asset registry summaries.
        </p>
      </div>
    </div>
  );
}
