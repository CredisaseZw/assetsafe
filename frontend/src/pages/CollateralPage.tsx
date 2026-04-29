import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { Plus, Search, Eye } from 'lucide-react'
import { collateralApi } from '@/api/collateralApi'
import { StatCard } from '@/components/shared/StatCard'
import { TableSkeleton } from '@/components/shared/TableSkeleton'
import { EmptyState } from '@/components/shared/EmptyState'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/shared/Modal'
import { CollateralForm } from '@/components/collateral/CollateralForm'
import { CollateralViewModal } from '@/components/collateral/CollateralViewModal'
import { cn, formatCurrency, formatDate } from '@/lib/utils'
import type { CollateralRecord, CollateralSearchField } from '@/types'

const SEARCH_OPTIONS: { value: CollateralSearchField; label: string }[] = [
  { value: 'agreement_number', label: 'Agreement Number' },
  { value: 'debtor', label: 'Debtor' },
  { value: 'reg_serial_number', label: 'Reg/Serial Number' },
  { value: 'financier', label: 'Financier' },
]

export default function CollateralPage() {
  const queryClient = useQueryClient()
  const [searchField, setSearchField] = useState<CollateralSearchField>('agreement_number')
  const [searchValue, setSearchValue] = useState('')
  const [appliedSearch, setAppliedSearch] = useState<{ field?: string; value?: string }>({})
  const [addOpen, setAddOpen] = useState(false)
  const [viewRecord, setViewRecord] = useState<CollateralRecord | null>(null)

  const { data, isLoading, isError } = useQuery({
    queryKey: ['collateral-dashboard', appliedSearch],
    queryFn: () =>
      collateralApi.getDashboard(
        appliedSearch.value
          ? { search_field: appliedSearch.field, search_value: appliedSearch.value }
          : undefined,
      ),
    // Use mock data when backend is unavailable
    placeholderData: {
      active_agreements: 78,
      pending_discharge_confirmation: 12,
      records: [
        {
          id: 1,
          lodge_date: '2021-01-23',
          agreement_number: 'D27385GUT',
          debtor_name: 'Fincheck',
          debtor_type: 'company' as const,
          debtor_id: 1,
          asset_description: 'Toyota Hilux',
          asset_type: 'Vehicles' as const,
          asset_make: 'Toyota',
          asset_model: 'Hilux',
          asset_year: 2020,
          asset_condition: 'new' as const,
          asset_registration_no: 'ADE1234',
          chassis_number: '',
          engine_number: '',
          serial_number: 'ADE1234',
          currency: 'USD' as const,
          loan_amount: 55000,
          instalment_amount: 2000,
          instalment_date: 1,
          total_paid_to_date: 10000,
          balance: 45000,
          start_date: '2021-01-01',
          end_date: '2023-12-31',
          financier_name: 'ABC Bank',
          financier_type: 'company' as const,
          financier_id: 2,
          data_source_name: 'John Doe',
          data_source_position: 'Manager',
          data_date: '2021-01-23',
          status: 'active' as const,
        },
        {
          id: 2,
          lodge_date: '2023-07-01',
          agreement_number: 'E373703RTS',
          debtor_name: 'Lorn Mine',
          debtor_type: 'company' as const,
          debtor_id: 3,
          asset_description: 'Petrux Generator',
          asset_type: 'Machinery' as const,
          asset_make: 'Petrux',
          asset_model: 'Generator',
          asset_year: 2019,
          asset_condition: 'second_hand' as const,
          asset_registration_no: '',
          chassis_number: '',
          engine_number: '',
          serial_number: '155655L',
          currency: 'ZWL' as const,
          loan_amount: 2500000,
          instalment_amount: 100000,
          instalment_date: 15,
          total_paid_to_date: 500000,
          balance: 2000000,
          start_date: '2022-06-15',
          end_date: '2023-06-14',
          financier_name: 'CBZ Bank',
          financier_type: 'company' as const,
          financier_id: 4,
          data_source_name: 'Jane Smith',
          data_source_position: 'Director',
          data_date: '2023-07-01',
          status: 'active' as const,
        },
      ],
    },
  })

  const handleSearch = () => {
    setAppliedSearch({ field: searchField, value: searchValue })
  }

  return (
    <div className="space-y-4">
      {/* ── Stats row ── */}
      <div className="flex flex-wrap gap-4">
        <StatCard
          label="Active Agreements"
          value={data?.active_agreements ?? 0}
        />
        <StatCard
          label="Pending Discharge Confirmation"
          value={data?.pending_discharge_confirmation ?? 0}
          className="border-l-4 border-l-amber-400"
        />
      </div>

      {/* ── Main card ── */}
      <div className="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
        {/* Card header bar */}
        <div className="flex items-center justify-between bg-[#0d1f3c] px-4 py-2.5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-white">
            Collateral Registry
          </h2>
        </div>

        {/* Toolbar */}
        <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2.5">
          {/* Search */}
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <select
              value={searchField}
              onChange={(e) => setSearchField(e.target.value as CollateralSearchField)}
              className="h-8 rounded border border-slate-300 bg-white px-2 text-xs text-slate-700 focus:outline-none focus:border-[#0f7d8e]"
            >
              {SEARCH_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
            <input
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search..."
              className="h-8 w-48 rounded border border-slate-300 bg-white px-2.5 text-xs placeholder:text-slate-400 focus:outline-none focus:border-[#0f7d8e]"
            />
            <Button size="sm" variant="primary" leftIcon={<Search className="h-3 w-3" />} onClick={handleSearch}>
              Search
            </Button>
          </div>

          {/* Actions */}
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
          <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">Active Debts</span>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-left">
                <th className="px-3 py-2.5 font-semibold text-slate-500 w-8">#</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Lodge Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Agreement No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Debtor</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Asset Description</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Reg/Serial No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Currency</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500 text-right">Loan Amount</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Start Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">End Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500"></th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <TableSkeleton rows={5} cols={11} />
              ) : isError ? (
                <tr>
                  <td colSpan={11} className="py-8 text-center text-sm text-red-500">
                    Failed to load records. Please try again.
                  </td>
                </tr>
              ) : !data?.records?.length ? (
                <EmptyState message="No collateral agreements found." />
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
                    <td className="px-3 py-2.5 text-slate-700">{rec.debtor_name}</td>
                    <td className="px-3 py-2.5 text-slate-700">{rec.asset_description}</td>
                    <td className="px-3 py-2.5 text-slate-600">{rec.serial_number || rec.asset_registration_no}</td>
                    <td className="px-3 py-2.5">
                      <span className="inline-flex rounded bg-slate-100 px-1.5 py-0.5 text-xs font-medium text-slate-600">
                        {rec.currency}
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-right font-medium text-slate-800">
                      {formatCurrency(rec.loan_amount)}
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

      {/* ── Add Collateral Modal ── */}
      <Modal open={addOpen} onClose={() => setAddOpen(false)} title="New Collateral Registration" size="xl">
        <CollateralForm
          onSuccess={() => {
            setAddOpen(false)
            toast.success('Collateral record created successfully')
            queryClient.invalidateQueries({ queryKey: ['collateral-dashboard'] })
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {/* ── View / Edit Modal ── */}
      {viewRecord && (
        <CollateralViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null)
            queryClient.invalidateQueries({ queryKey: ['collateral-dashboard'] })
          }}
        />
      )}
    </div>
  )
}
