import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { Plus, Search, Eye, Building2 } from 'lucide-react'
import { hirePurchaseApi } from '@/api/hirePurchaseApi'
import { StatCard } from '@/components/shared/StatCard'
import { TableSkeleton } from '@/components/shared/TableSkeleton'
import { EmptyState } from '@/components/shared/EmptyState'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/shared/Modal'
import { HirePurchaseForm } from '@/components/hire-purchase/HirePurchaseForm'
import { HirePurchaseViewModal } from '@/components/hire-purchase/HirePurchaseViewModal'
import { cn, formatCurrency, formatDate } from '@/lib/utils'
import type { HirePurchaseRecord } from '@/types'

// Demo data matching PDF
const DEMO_DATA = {
  number_of_financiers: 3,
  active_agreements: 2,
  pending_closure_confirmation: 1,
  records: [
    {
      id: 1,
      lodge_date: '2021-01-23',
      agreement_number: 'D27385GUT',
      purchaser_name: 'Fincheck',
      purchaser_type: 'company' as const,
      purchaser_id: 1,
      asset_make: 'Toyota',
      asset_model: 'Hilux',
      asset_type: 'Vehicles' as const,
      asset_year: 2020,
      asset_condition: 'new' as const,
      reg_serial_number: 'ADE1234',
      chassis_number: '',
      engine_number: '',
      currency: 'USD' as const,
      purchase_amount: 55000,
      instalment_amount: 2000,
      instalment_date: 1,
      total_paid_to_date: 10000,
      balance: 45000,
      start_date: '2021-01-01',
      end_date: '2023-12-31',
      financier_name: 'ABC Money Lenders (PVT) Ltd',
      financier_id: 2,
      data_date: '2021-01-23',
      status: 'active' as const,
    },
    {
      id: 2,
      lodge_date: '2023-07-01',
      agreement_number: 'E373703RTS',
      purchaser_name: 'Lorn Mine',
      purchaser_type: 'company' as const,
      purchaser_id: 3,
      asset_make: 'Petrux',
      asset_model: 'Generator',
      asset_type: 'Machinery' as const,
      asset_year: 2019,
      asset_condition: 'second_hand' as const,
      reg_serial_number: '155655L',
      chassis_number: '',
      engine_number: '',
      currency: 'ZWL' as const,
      purchase_amount: 2500000,
      instalment_amount: 100000,
      instalment_date: 15,
      total_paid_to_date: 500000,
      balance: 2000000,
      start_date: '2022-06-15',
      end_date: '2023-06-14',
      financier_name: 'CBZ Bank',
      financier_id: 4,
      data_date: '2023-07-01',
      status: 'active' as const,
    },
  ],
}

export default function HirePurchasePage() {
  const queryClient = useQueryClient()
  const [selectedFinancier, setSelectedFinancier] = useState('')
  const [addOpen, setAddOpen] = useState(false)
  const [viewRecord, setViewRecord] = useState<HirePurchaseRecord | null>(null)

  const { data, isLoading } = useQuery({
    queryKey: ['hp-dashboard', selectedFinancier],
    queryFn: () =>
      hirePurchaseApi.getDashboard(
        selectedFinancier ? { financier_id: Number(selectedFinancier) } : undefined,
      ),
    placeholderData: DEMO_DATA,
  })

  return (
    <div className="space-y-4">
      {/* ── Stats row ── */}
      <div className="flex flex-wrap gap-4">
        <StatCard label="Number of Financiers" value={data?.number_of_financiers ?? 0} />
        <StatCard label="Active Agreements" value={data?.active_agreements ?? 0} />
        <StatCard
          label="Pending Closure Confirmation"
          value={data?.pending_closure_confirmation ?? 0}
          className="border-l-4 border-l-amber-400"
        />
      </div>

      {/* ── Main card ── */}
      <div className="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
        <div className="flex items-center justify-between bg-[#0d1f3c] px-4 py-2.5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-white">
            Hire Purchase Registry
          </h2>
        </div>

        {/* Toolbar */}
        <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2.5">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <Building2 className="h-4 w-4 text-slate-400" />
            <select
              value={selectedFinancier}
              onChange={(e) => setSelectedFinancier(e.target.value)}
              className="h-8 flex-1 max-w-xs rounded border border-slate-300 bg-white px-2 text-xs text-slate-700 focus:outline-none focus:border-[#0f7d8e]"
            >
              <option value="">Search Financier</option>
              <option value="2">ABC Money Lenders (PVT) Ltd</option>
              <option value="4">CBZ Bank</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <Button size="sm" variant="primary" leftIcon={<Plus className="h-3 w-3" />} onClick={() => setAddOpen(true)}>
              Add Single
            </Button>
            <Button size="sm" variant="secondary" leftIcon={<Plus className="h-3 w-3" />}>
              Add Multiple
            </Button>
          </div>
        </div>

        {/* Sub-section label */}
        <div className="px-4 py-1.5 bg-slate-50 border-b border-slate-200">
          <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">Active Agreements</span>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-left">
                <th className="px-3 py-2.5 font-semibold text-slate-500 w-8">#</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Lodge Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Agreement No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Purchaser</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Asset Make</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Reg/Serial No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Currency</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500 text-right">Purchase Amount</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Start Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">End Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500"></th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <TableSkeleton rows={5} cols={11} />
              ) : !data?.records?.length ? (
                <EmptyState message="No hire purchase agreements found." />
              ) : (
                data.records.map((rec, idx) => (
                  <tr
                    key={rec.id}
                    className={cn(
                      'border-b border-slate-100 hover:bg-slate-50 transition-colors',
                      idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/40',
                    )}
                  >
                    <td className="px-3 py-2.5 text-slate-400">{idx + 1}</td>
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.lodge_date)}</td>
                    <td className="px-3 py-2.5 font-medium text-[#0f7d8e]">{rec.agreement_number}</td>
                    <td className="px-3 py-2.5 text-slate-700">{rec.purchaser_name}</td>
                    <td className="px-3 py-2.5 text-slate-700">{rec.asset_make} {rec.asset_model}</td>
                    <td className="px-3 py-2.5 text-slate-600">{rec.reg_serial_number}</td>
                    <td className="px-3 py-2.5">
                      <span className="inline-flex rounded bg-slate-100 px-1.5 py-0.5 text-xs font-medium text-slate-600">
                        {rec.currency}
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-right font-medium text-slate-800">
                      {formatCurrency(rec.purchase_amount)}
                    </td>
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.start_date)}</td>
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.end_date)}</td>
                    <td className="px-3 py-2.5">
                      <button
                        onClick={() => setViewRecord(rec)}
                        className="flex items-center gap-1 rounded bg-[#0f7d8e] px-2.5 py-1 text-xs font-medium text-white hover:bg-[#0d6e7e] transition-colors"
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
      <Modal open={addOpen} onClose={() => setAddOpen(false)} title="Hire Purchase Form" size="xl">
        <HirePurchaseForm
          onSuccess={() => {
            setAddOpen(false)
            toast.success('Hire purchase record created successfully')
            queryClient.invalidateQueries({ queryKey: ['hp-dashboard'] })
          }}
          onSaveAndAdd={() => {
            toast.success('Record saved — ready for next entry')
            queryClient.invalidateQueries({ queryKey: ['hp-dashboard'] })
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {/* ── View Modal ── */}
      {viewRecord && (
        <HirePurchaseViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null)
            queryClient.invalidateQueries({ queryKey: ['hp-dashboard'] })
          }}
        />
      )}
    </div>
  )
}
