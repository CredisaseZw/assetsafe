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

  const { data: statsData } = useQuery({
    queryKey: ['collateral-dashboard', appliedSearch],
    queryFn: () =>
      collateralApi.getDashboard(
        appliedSearch.value
          ? { search_field: appliedSearch.field, search_value: appliedSearch.value }
          : undefined,
      ),
  })

  const { data: recordsData, isLoading, isError } = useQuery({
    queryKey: ['collateral-records', appliedSearch],
    queryFn: () =>
      collateralApi.getRecords(
        appliedSearch.value ? { search: appliedSearch.value } : undefined,
      ),
  })

  const handleSearch = () => {
    setAppliedSearch({ field: searchField, value: searchValue })
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center gap-x-16 gap-y-4">
        <StatCard label="Active Agreements" value={statsData?.active_agreements ?? 0} />
        <StatCard
          label="Pending Discharge Confirmation"
          value={statsData?.pending_discharge_confirmation ?? 0}
        />
      </div>

      <div className="space-y-0 border border-[#8f8f8f] bg-white">
        <div className="bg-[#7f7a7b] px-4 py-2.5 text-center text-[18px] font-bold uppercase tracking-wide text-white">
          Collateral Registry
        </div>

        <div className="flex flex-wrap items-end justify-between gap-6 px-4 py-8">
          <div className="flex flex-wrap items-end gap-4">
            <div className="flex items-center gap-3">
              <span className="text-[18px] font-bold text-black">Search</span>
              <select
                value={searchField}
                onChange={(e) => setSearchField(e.target.value as CollateralSearchField)}
                className="h-9 min-w-[180px] rounded-none border-2 border-black bg-white px-3 text-sm text-black focus:outline-none"
              >
                {SEARCH_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
              <input
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Agreement Number"
                className="h-9 w-64 rounded-none border-2 border-black bg-white px-3 text-sm text-black placeholder:text-slate-500 focus:outline-none"
              />
              <Button size="sm" variant="primary" leftIcon={<Search className="h-3.5 w-3.5" />} onClick={handleSearch}>
                Search
              </Button>
            </div>
          </div>

          <div className="flex items-center gap-0 self-end">
            <Button
              size="sm"
              variant="success"
              leftIcon={<Plus className="h-3.5 w-3.5" />}
              onClick={() => setAddOpen(true)}
              className="min-w-[110px] rounded-none border-r-0 text-[15px] font-bold"
            >
              + Add Single
            </Button>
            <Button
              size="sm"
              variant="danger"
              leftIcon={<Plus className="h-3.5 w-3.5" />}
              className="min-w-[120px] rounded-none text-[15px] font-bold"
            >
              + Add Multiple
            </Button>
          </div>
        </div>

        <div className="border-t border-[#8f8f8f] bg-[#7f7a7b] px-4 py-2 text-center text-[16px] font-bold uppercase text-white">
          Active Debts
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b border-[#8f8f8f] bg-white text-left">
                <th className="w-8 border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">#</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Lodge Date</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Agreement No.</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Debtor</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Asset Description</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Reg/Serial No.</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Currency</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 text-right font-bold text-black">Loan Amount</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">Start Date</th>
                <th className="border-r border-[#8f8f8f] px-3 py-3 font-bold text-black">End Date</th>
                <th className="px-3 py-3 font-bold text-black"></th>
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
              ) : !recordsData?.length ? (
                <EmptyState message="No collateral agreements found." />
              ) : (
                recordsData.map((rec, idx) => (
                  <tr key={rec.id} className={cn('border-b border-[#8f8f8f]', idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]')}>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-center text-slate-700">{idx + 1}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-700">{formatDate(rec.lodge_date)}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 font-bold text-[#0f7d8e]">{rec.agreement_number}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-800">{rec.debtor_name}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-800">{rec.asset_description}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-700">{rec.serial_number || rec.asset_registration_no}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-center text-slate-700">{rec.currency}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-right text-slate-800">{formatCurrency(rec.loan_amount)}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-700">{formatDate(rec.start_date)}</td>
                    <td className="border-r border-[#8f8f8f] px-3 py-2.5 text-slate-700">{formatDate(rec.end_date)}</td>
                    <td className="px-3 py-2.5">
                      <button
                        onClick={() => setViewRecord(rec)}
                        className="min-w-[72px] rounded-none bg-[#1278bf] px-3 py-2 text-sm font-bold text-white transition-colors hover:bg-[#0f639d]"
                      >
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
            queryClient.invalidateQueries({ queryKey: ['collateral-records'] })
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
            queryClient.invalidateQueries({ queryKey: ['collateral-records'] })
          }}
        />
      )}
    </div>
  )
}
