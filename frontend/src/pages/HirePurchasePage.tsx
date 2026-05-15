import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Plus, Search, Eye, Building2 } from 'lucide-react';
import { hirePurchaseApi } from '@/api/hirePurchaseApi';
import { StatCard } from '@/components/shared/StatCard';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/shared/Modal';
import { HirePurchaseForm } from '@/components/hire-purchase/HirePurchaseForm';
import { HirePurchaseViewModal } from '@/components/hire-purchase/HirePurchaseViewModal';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import type { HirePurchaseRecord } from '@/types';

export default function HirePurchasePage() {
  const queryClient = useQueryClient();
  const [selectedFinancier, setSelectedFinancier] = useState('');
  const [addOpen, setAddOpen] = useState(false);
  const [viewRecord, setViewRecord] = useState<HirePurchaseRecord | null>(null);

  const { data: statsData } = useQuery({
    queryKey: ['hp-dashboard', selectedFinancier],
    queryFn: () =>
      hirePurchaseApi.getDashboard(
        selectedFinancier
          ? { financier_id: Number(selectedFinancier) }
          : undefined,
      ),
  });

  const { data: recordsData, isLoading } = useQuery({
    queryKey: ['hp-records', selectedFinancier],
    queryFn: () =>
      hirePurchaseApi.getRecords(
        selectedFinancier
          ? { financier_id: Number(selectedFinancier) }
          : undefined,
      ),
  });

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <StatCard
          label="Number of Financiers"
          value={statsData?.number_of_financiers ?? 0}
        />
        <StatCard
          label="Active Agreements"
          value={statsData?.active_agreements ?? 0}
        />
        <StatCard
          label="Pending Closure Confirmation"
          value={statsData?.pending_closure_confirmation ?? 0}
        />
      </div>

      <div className="space-y-0 border border-[#8f8f8f] bg-white">
        <div className="bg-[#7f7a7b] px-4 py-2.5 text-center text-[18px] font-bold uppercase tracking-wide text-white">
          Hire Purchase Registry
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#8f8f8f] px-4 py-6 lg:px-10">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-[18px] font-bold text-black">Search</span>
            <Building2 className="h-4 w-4 text-black" />
            <select
              value={selectedFinancier}
              onChange={(e) => setSelectedFinancier(e.target.value)}
              className="h-10 w-64 rounded-sm border border-black bg-white px-3 text-[14px] text-black focus:outline-none"
            >
              <option value="">Financier</option>
              <option value="2">ABC Money Lenders (PVT) Ltd</option>
              <option value="4">CBZ Bank</option>
            </select>
            <Button
              size="sm"
              variant="primary"
              leftIcon={<Search className="h-3.5 w-3.5" />}
              className="h-10 px-5 text-[14px]"
            >
              Search
            </Button>
          </div>

          <div className="flex items-center gap-0 self-end">
            <Button
              size="sm"
              variant="success"
              leftIcon={<Plus className="h-3.5 w-3.5" />}
              onClick={() => setAddOpen(true)}
              className="h-12 rounded-none px-5 text-[15px] font-bold text-white"
            >
              <span className="leading-tight">
                + Add
                <br />
                Single
              </span>
            </Button>
            <Button
              size="sm"
              variant="danger"
              leftIcon={<Plus className="h-3.5 w-3.5" />}
              className="h-12 rounded-none px-5 text-[15px] font-bold text-white"
            >
              <span className="leading-tight">
                +Add
                <br />
                Multiple
              </span>
            </Button>
          </div>
        </div>

        <div className="bg-[#7f7a7b] px-4 py-1.5 text-center text-[18px] font-bold uppercase tracking-wide text-white">
          Active Agreements
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-[14px]">
            <thead>
              <tr className="border-b border-[#8f8f8f] bg-white text-left">
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black w-8">
                  #
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Lodge Date
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Agreement No.
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Purchaser
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Asset Make
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Reg/Serial No.
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Currency
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black text-right">
                  Purchase Amount
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  Start Date
                </th>
                <th className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-black">
                  End Date
                </th>
                <th className="px-3 py-2.5 font-bold text-black"></th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <TableSkeleton rows={5} cols={11} />
              ) : !recordsData?.length ? (
                <EmptyState message="No hire purchase agreements found." />
              ) : (
                recordsData.map((rec, idx) => (
                  <tr
                    key={rec.id}
                    className={cn(
                      'border-b border-[#8f8f8f] transition-colors hover:bg-[#f5f5f5]',
                      idx % 2 === 0 ? 'bg-white' : 'bg-[#fafafa]',
                    )}
                  >
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {idx + 1}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {formatDate(rec.lodge_date)}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle font-medium text-[#196A86]">
                      {rec.agreement_number}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {rec.purchaser_name}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {rec.asset_make} {rec.asset_model}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {rec.reg_serial_number}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      <span className="inline-flex rounded-sm bg-[#ededeb] px-2 py-0.5 text-[12px] font-semibold text-slate-800">
                        {rec.currency}
                      </span>
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-right font-medium text-black">
                      {formatCurrency(rec.purchase_amount)}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {formatDate(rec.start_date)}
                    </td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                      {formatDate(rec.end_date)}
                    </td>
                    <td className="px-3 py-2.5 align-middle">
                      <button
                        onClick={() => setViewRecord(rec)}
                        className="flex items-center gap-1 rounded-none bg-[#196A86] px-3 py-1.5 text-[12px] font-bold text-white transition-colors hover:bg-[#15586f]"
                      >
                        <Eye className="h-3 w-3" />
                        View
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── Add HP Modal ── */}
      <Modal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Hire Purchase Form"
        size="xl"
      >
        <HirePurchaseForm
          onSuccess={() => {
            setAddOpen(false);
            toast.success('Hire purchase record created successfully');
            queryClient.invalidateQueries({ queryKey: ['hp-dashboard'] });
            queryClient.invalidateQueries({ queryKey: ['hp-records'] });
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {/* ── View / Edit Modal ── */}
      {viewRecord && (
        <HirePurchaseViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null);
            queryClient.invalidateQueries({ queryKey: ['hp-dashboard'] });
            queryClient.invalidateQueries({ queryKey: ['hp-records'] });
          }}
        />
      )}
    </div>
  );
}
