import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { Plus, Eye } from 'lucide-react'
import { assetRegistryApi } from '@/api/assetRegistryApi'
import { StatCard } from '@/components/shared/StatCard'
import { TableSkeleton } from '@/components/shared/TableSkeleton'
import { EmptyState } from '@/components/shared/EmptyState'
import { Button } from '@/components/ui/Button'
import { Modal } from '@/components/shared/Modal'
import { AssetRegistryForm } from '@/components/registry/AssetRegistryForm'
import { AssetViewModal } from '@/components/registry/AssetViewModal'
import { cn, formatCurrency, formatDate } from '@/lib/utils'
import type { AssetRecord, AssetType } from '@/types'
import { ASSET_TYPES } from '@/types'

const DEMO_DATA = {
  total_assets: 8785,
  total_estimate_value: 2513458,
  records: [
    {
      id: 1,
      lodge_date: '2021-01-23',
      registration_number: 'AR000001',
      owner_name: 'Fincheck',
      owner_type: 'company' as const,
      owner_id: 1,
      owner_asset_number: '',
      asset_description: 'Toyota Hilux',
      asset_type: 'Vehicles' as const,
      asset_make: 'Toyota',
      asset_model: 'Hilux',
      year_of_make: 2020,
      condition: 'new' as const,
      mv_registration_no: 'ADE1234',
      chassis_number: '',
      engine_number: '',
      serial_number: 'ADE1234',
      currency: 'USD' as const,
      estimated_value: 55000,
      location_address: '123 Main St, Harare',
      subscription_start_date: '2021-01-01',
      subscription_end_date: '2023-12-31',
      status: 'active' as const,
    },
    {
      id: 2,
      lodge_date: '2023-07-01',
      registration_number: 'AR000326',
      owner_name: 'Joe Maka',
      owner_type: 'individual' as const,
      owner_id: 3,
      owner_asset_number: '',
      asset_description: 'Petrux Generator',
      asset_type: 'Machinery' as const,
      asset_make: 'Petrux',
      asset_model: 'Generator',
      year_of_make: 2019,
      condition: 'second_hand' as const,
      mv_registration_no: '',
      chassis_number: '',
      engine_number: '',
      serial_number: '155655L',
      currency: 'ZWL' as const,
      estimated_value: 2500000,
      location_address: '45 Industrial Ave, Bulawayo',
      subscription_start_date: '2022-06-15',
      subscription_end_date: '2023-06-14',
      status: 'active' as const,
    },
  ],
}

export default function AssetRegistryPage() {
  const queryClient = useQueryClient()
  const [filterAssetType, setFilterAssetType] = useState<AssetType | ''>('')
  const [addOpen, setAddOpen] = useState(false)
  const [viewRecord, setViewRecord] = useState<AssetRecord | null>(null)

  const { data, isLoading } = useQuery({
    queryKey: ['registry-dashboard', filterAssetType],
    queryFn: () =>
      assetRegistryApi.getDashboard(filterAssetType ? { asset_type: filterAssetType } : undefined),
    placeholderData: DEMO_DATA,
  })

  return (
    <div className="space-y-4">
      {/* Stats */}
      <div className="flex flex-wrap gap-4">
        <StatCard
          label="Total Assets"
          value={data?.total_assets?.toLocaleString() ?? '0'}
        />
        <StatCard
          label="Total Estimate Value"
          value={`US$${data?.total_estimate_value ? formatCurrency(data.total_estimate_value) : '0.00'}`}
        />
      </div>

      {/* Main card */}
      <div className="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
        <div className="flex items-center justify-between bg-[#0d1f3c] px-4 py-2.5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-white">Asset Registry</h2>
        </div>

        {/* Toolbar */}
        <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2.5">
          <div className="flex items-center gap-2 flex-1">
            <select
              value={filterAssetType}
              onChange={(e) => setFilterAssetType(e.target.value as AssetType | '')}
              className="h-8 rounded border border-slate-300 bg-white px-2 text-xs text-slate-700 focus:outline-none focus:border-[#0f7d8e]"
            >
              <option value="">Search Criteria — All</option>
              {ASSET_TYPES.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
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
                <th className="px-3 py-2.5 font-semibold text-slate-500">Lodge Date</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Regist. No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Owner</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Asset Description</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Reg/Serial No.</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Currency</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500 text-right">Estimate Value</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Sub. Start</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500">Sub. End</th>
                <th className="px-3 py-2.5 font-semibold text-slate-500"></th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <TableSkeleton rows={5} cols={10} />
              ) : !data?.records?.length ? (
                <EmptyState message="No assets found." />
              ) : (
                data.records.map((rec, idx) => (
                  <tr
                    key={rec.id}
                    className={cn(
                      'border-b border-slate-100 hover:bg-slate-50 transition-colors',
                      idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/40',
                    )}
                  >
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.lodge_date)}</td>
                    <td className="px-3 py-2.5 font-medium text-[#0f7d8e]">{rec.registration_number}</td>
                    <td className="px-3 py-2.5 text-slate-700">{rec.owner_name}</td>
                    <td className="px-3 py-2.5 text-slate-700">{rec.asset_description}</td>
                    <td className="px-3 py-2.5 text-slate-600">{rec.serial_number || rec.mv_registration_no}</td>
                    <td className="px-3 py-2.5">
                      <span className="inline-flex rounded bg-slate-100 px-1.5 py-0.5 text-xs font-medium text-slate-600">
                        {rec.currency}
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-right font-medium text-slate-800">
                      {formatCurrency(rec.estimated_value)}
                    </td>
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.subscription_start_date)}</td>
                    <td className="px-3 py-2.5 text-slate-600">{formatDate(rec.subscription_end_date)}</td>
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

      {/* Add Modal */}
      <Modal open={addOpen} onClose={() => setAddOpen(false)} title="New Asset Registration" size="xl">
        <AssetRegistryForm
          onSuccess={() => {
            setAddOpen(false)
            toast.success('Asset registered successfully')
            queryClient.invalidateQueries({ queryKey: ['registry-dashboard'] })
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {/* View Modal */}
      {viewRecord && (
        <AssetViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null)
            queryClient.invalidateQueries({ queryKey: ['registry-dashboard'] })
          }}
        />
      )}
    </div>
  )
}
