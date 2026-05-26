import { useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { ArrowDown, ArrowUp, ArrowUpDown, Plus } from 'lucide-react';
import { assetRegistryApi } from '@/api/assetRegistryApi';
import { StatCard } from '@/components/shared/StatCard';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { AssetRegistryForm } from '@/components/registry/AssetRegistryForm';
import { AssetViewModal } from '@/components/registry/AssetViewModal';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import type { AssetRecord, AssetType } from '@/types';
import { ASSET_TYPES } from '@/types';

const PAGE_SIZE = 8;

type AssetSortOption = 'date-desc' | 'date-asc' | 'name-asc' | 'name-desc';

export default function AssetRegistryPage() {
  const queryClient = useQueryClient();
  const [filterAssetType, setFilterAssetType] = useState<AssetType | ''>('');
  const [sortOption, setSortOption] = useState<AssetSortOption>('date-desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [addOpen, setAddOpen] = useState(false);
  const [viewRecord, setViewRecord] = useState<AssetRecord | null>(null);

  const { data: statsData } = useQuery({
    queryKey: ['registry-dashboard', filterAssetType],
    queryFn: () =>
      assetRegistryApi.getDashboard(
        filterAssetType ? { asset_type: filterAssetType } : undefined,
      ),
  });

  const { data: recordsData, isLoading } = useQuery({
    queryKey: ['registry-records', filterAssetType],
    queryFn: () =>
      assetRegistryApi.getRecords(
        filterAssetType ? { asset_type: filterAssetType } : undefined,
      ),
  });

  const totalRecords = recordsData?.length ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalRecords / PAGE_SIZE));
  const activePage = Math.min(currentPage, totalPages);
  const activeSortField = sortOption.startsWith('date') ? 'date' : 'name';
  const activeSortDirection = sortOption.endsWith('asc') ? 'asc' : 'desc';

  const toggleSort = (field: 'date' | 'name') => {
    setSortOption((current) => {
      const currentField = current.startsWith('date') ? 'date' : 'name';
      const currentDirection = current.endsWith('asc') ? 'asc' : 'desc';

      if (currentField === field) {
        return `${field}-${currentDirection === 'asc' ? 'desc' : 'asc'}` as AssetSortOption;
      }

      return field === 'date' ? 'date-desc' : 'name-asc';
    });
    setCurrentPage(1);
  };

  const sortedRecords = useMemo(() => {
    if (!recordsData) {
      return [] as AssetRecord[];
    }

    const compareDate = (left: AssetRecord, right: AssetRecord) => {
      const leftTime = new Date(left.lodge_date ?? '').getTime();
      const rightTime = new Date(right.lodge_date ?? '').getTime();
      return leftTime - rightTime;
    };

    const compareName = (left: AssetRecord, right: AssetRecord) => {
      return (left.owner_name ?? '').localeCompare(
        right.owner_name ?? '',
        undefined,
        {
          sensitivity: 'base',
        },
      );
    };

    const sorted = [...recordsData];

    sorted.sort((left, right) => {
      switch (sortOption) {
        case 'date-asc':
          return compareDate(left, right);
        case 'date-desc':
          return compareDate(right, left);
        case 'name-asc':
          return compareName(left, right);
        case 'name-desc':
          return compareName(right, left);
        default:
          return 0;
      }
    });

    return sorted;
  }, [recordsData, sortOption]);

  const pagedRecords = useMemo(() => {
    if (!sortedRecords) {
      return [] as AssetRecord[];
    }

    const start = (activePage - 1) * PAGE_SIZE;
    return sortedRecords.slice(start, start + PAGE_SIZE);
  }, [sortedRecords, activePage]);

  const startItem = totalRecords === 0 ? 0 : (activePage - 1) * PAGE_SIZE + 1;
  const endItem = Math.min(activePage * PAGE_SIZE, totalRecords);

  return (
    <div className="flex h-full min-h-0 flex-col gap-8 overflow-hidden">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <StatCard
          label="Total Assets"
          value={statsData?.total_assets?.toLocaleString() ?? '0'}
        />
        <StatCard
          label="Total Estimate Value"
          value={`US$${statsData?.total_estimate_value ? formatCurrency(statsData.total_estimate_value) : '0.00'}`}
        />
      </div>

      <div className="flex min-h-0 flex-1 flex-col overflow-hidden border border-[#8f8f8f] bg-white">
        <div className="bg-[#7f7a7b] px-4 py-2.5 text-center text-[18px] font-bold uppercase tracking-wide text-white">
          Asset Registry
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#8f8f8f] px-4 py-6 lg:px-10">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-[18px] font-bold text-black">Search</span>
            <select
              value={filterAssetType}
              onChange={(e) => {
                setFilterAssetType(e.target.value as AssetType | '');
                setCurrentPage(1);
              }}
              className="h-10 rounded-sm border border-black bg-white px-3 text-[14px] text-black focus:outline-none"
            >
              <option value="">Criteria</option>
              {ASSET_TYPES.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
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

        <div className="min-h-0 flex-1 overflow-hidden">
          <div className="h-full min-h-0 overflow-auto">
            <table className="w-full border-collapse text-[14px]">
              <thead>
                <tr className="sticky top-0 z-10 border-b border-[#8f8f8f] bg-white text-left divide-x divide-[#8f8f8f]">
                  <th className="px-3 py-2.5 font-bold text-black">
                    <button
                      type="button"
                      onClick={() => toggleSort('date')}
                      className="flex items-center gap-1"
                      title="Sort by lodge date"
                    >
                      <span>Lodge Date</span>
                      {activeSortField === 'date' ? (
                        activeSortDirection === 'asc' ? (
                          <ArrowUp className="h-3.5 w-3.5" />
                        ) : (
                          <ArrowDown className="h-3.5 w-3.5" />
                        )
                      ) : (
                        <ArrowUpDown className="h-3.5 w-3.5" />
                      )}
                    </button>
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">
                    Regist. No.
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">
                    <button
                      type="button"
                      onClick={() => toggleSort('name')}
                      className="flex items-center gap-1"
                      title="Sort by owner name"
                    >
                      <span>Owner</span>
                      {activeSortField === 'name' ? (
                        activeSortDirection === 'asc' ? (
                          <ArrowUp className="h-3.5 w-3.5" />
                        ) : (
                          <ArrowDown className="h-3.5 w-3.5" />
                        )
                      ) : (
                        <ArrowUpDown className="h-3.5 w-3.5" />
                      )}
                    </button>
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">
                    Asset Description
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">
                    Reg/Serial No.
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">Currency</th>
                  <th className="px-3 py-2.5 font-bold text-black text-right">
                    Estimate Value
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">
                    Sub. Start
                  </th>
                  <th className="px-3 py-2.5 font-bold text-black">Sub. End</th>
                  <th className="px-3 py-2.5 font-bold text-black"></th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <TableSkeleton rows={5} cols={10} />
                ) : !pagedRecords.length ? (
                  <EmptyState message="No assets found." />
                ) : (
                  pagedRecords.map((rec, idx) => (
                    <tr
                      key={rec.id}
                      className={cn(
                        'border-b border-[#8f8f8f] transition-colors hover:bg-[#f5f5f5]',
                        ((activePage - 1) * PAGE_SIZE + idx) % 2 === 0
                          ? 'bg-white'
                          : 'bg-[#fafafa]',
                      )}
                    >
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {formatDate(rec.lodge_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle font-medium text-[#196A86]">
                        {rec.registration_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {rec.owner_name}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {rec.asset_description}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {rec.serial_number || rec.mv_registration_no}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        <span className="inline-flex rounded-sm bg-[#ededeb] px-2 py-0.5 text-[12px] font-semibold text-slate-800">
                          {rec.currency}
                        </span>
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-right font-medium text-black">
                        {formatCurrency(rec.estimated_value)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {formatDate(rec.subscription_start_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-black">
                        {formatDate(rec.subscription_end_date)}
                      </td>
                      <td className="px-3 py-2.5 align-middle">
                        <button
                          onClick={() => setViewRecord(rec)}
                          className="rounded-none bg-[#196A86] px-3 py-1.5 text-[12px] font-bold text-white transition-colors hover:bg-[#15586f]"
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

          <div className="flex shrink-0 flex-wrap items-center justify-between gap-3 border-t border-[#8f8f8f] bg-[#f8f7f2] px-4 py-3 text-sm text-slate-700">
            <div>
              Showing {startItem} to {endItem} of {totalRecords} entries
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setCurrentPage((page) => Math.max(1, page - 1))}
                disabled={activePage === 1}
                className="border border-[#8f8f8f] bg-white px-3 py-1.5 text-sm font-medium text-black disabled:cursor-not-allowed disabled:opacity-50"
              >
                Prev
              </button>
              <div className="flex items-center gap-1">
                {Array.from({ length: totalPages }).map((_, index) => {
                  const page = index + 1;
                  return (
                    <button
                      key={page}
                      type="button"
                      onClick={() => setCurrentPage(page)}
                      className={cn(
                        'min-w-9 border px-3 py-1.5 text-sm font-medium',
                        page === activePage
                          ? 'border-[#196A86] bg-[#196A86] text-white'
                          : 'border-[#8f8f8f] bg-white text-black hover:bg-[#f1f1f1]',
                      )}
                    >
                      {page}
                    </button>
                  );
                })}
              </div>
              <button
                type="button"
                onClick={() =>
                  setCurrentPage((page) => Math.min(totalPages, page + 1))
                }
                disabled={activePage === totalPages}
                className="border border-[#8f8f8f] bg-white px-3 py-1.5 text-sm font-medium text-black disabled:cursor-not-allowed disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ── Add Asset Modal ── */}
      <Modal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="New Asset Registration"
        size="xl"
      >
        <AssetRegistryForm
          onSuccess={() => {
            setAddOpen(false);
            toast.success('Asset record created successfully');
            queryClient.invalidateQueries({ queryKey: ['registry-dashboard'] });
            queryClient.invalidateQueries({ queryKey: ['registry-records'] });
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {/* ── View / Edit Modal ── */}
      {viewRecord && (
        <AssetViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null);
            queryClient.invalidateQueries({ queryKey: ['registry-dashboard'] });
            queryClient.invalidateQueries({ queryKey: ['registry-records'] });
          }}
        />
      )}
    </div>
  );
}
