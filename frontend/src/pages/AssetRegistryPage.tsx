import { useEffect, useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { ArrowDown, ArrowUp, ArrowUpDown, Plus, Search } from 'lucide-react';
import { assetRegistryApi } from '@/api/assetRegistryApi';
import { InlineStat } from '@/components/shared/InlineStat';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { AssetRegistryForm } from '@/components/registry/AssetRegistryForm';
import { AssetViewModal } from '@/components/registry/AssetViewModal';
import { NumberedPaginationFooter } from '@/components/shared/NumberedPaginationFooter';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import { invalidateRegistryQueries } from '@/lib/registryCache';
import { ASSET_TYPE_OPTIONS } from '@/types';
import type { AssetRecord, AssetType } from '@/types';

const PAGE_SIZE = 16;

type AssetSortOption = 'date-desc' | 'date-asc' | 'name-asc' | 'name-desc';

export default function AssetRegistryPage() {
  const queryClient = useQueryClient();
  const [filterAssetType, setFilterAssetType] = useState<AssetType | ''>('');
  const [searchText, setSearchText] = useState('');
  const [appliedSearch, setAppliedSearch] = useState('');
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
    queryKey: ['registry-records', filterAssetType, appliedSearch, currentPage],
    queryFn: () =>
      assetRegistryApi.getRecords({
        ...(filterAssetType ? { asset_type: filterAssetType } : {}),
        ...(appliedSearch ? { search: appliedSearch } : {}),
        page: currentPage,
        page_size: PAGE_SIZE,
      }),
  });

  const handleSearch = () => {
    setAppliedSearch(searchText.trim());
    setCurrentPage(1);
  };

  const refreshList = (clearFilters = false) => {
    if (clearFilters) {
      setFilterAssetType('');
      setSearchText('');
      setAppliedSearch('');
    }
    setCurrentPage(1);
    invalidateRegistryQueries(queryClient, 'asset');
  };

  const totalRecords = recordsData?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalRecords / PAGE_SIZE));
  const activePage = Math.min(currentPage, totalPages);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

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
    if (!recordsData?.records) {
      return [] as AssetRecord[];
    }

    const compareDate = (left: AssetRecord, right: AssetRecord) => {
      const leftTime = new Date(left.lodge_date ?? '').getTime();
      const rightTime = new Date(right.lodge_date ?? '').getTime();
      return leftTime - rightTime;
    };

    const compareName = (left: AssetRecord, right: AssetRecord) =>
      (left.owner_name ?? '').localeCompare(right.owner_name ?? '', undefined, {
        sensitivity: 'base',
      });

    const sorted = [...recordsData.records];

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

  const startItem = totalRecords === 0 ? 0 : (activePage - 1) * PAGE_SIZE + 1;
  const endItem = Math.min(activePage * PAGE_SIZE, totalRecords);

  return (
    <div className="flex h-full min-h-0 flex-col overflow-hidden">
      <div className="flex h-full min-h-0 flex-1 flex-col overflow-hidden border border-[#8f8f8f] bg-white">
        <div className="shrink-0 bg-[#7f7a7b] px-3 py-1.5 text-center text-[15px] font-bold uppercase tracking-wide text-white">
          Asset Registry
        </div>

        <div className="flex shrink-0 flex-wrap items-center gap-3 border-b border-[#8f8f8f] bg-[#f8f7f2] px-3 py-2">
          <InlineStat
            label="Total Assets"
            value={statsData?.total_assets?.toLocaleString() ?? '0'}
          />
          <InlineStat
            label="Est. Value"
            value={`US$${statsData?.total_estimate_value ? formatCurrency(statsData.total_estimate_value) : '0.00'}`}
          />
        </div>

        <div className="flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-[#8f8f8f] px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[12px] font-bold text-black">Search</span>
            <select
              value={filterAssetType}
              onChange={(e) => {
                setFilterAssetType(e.target.value as AssetType | '');
                setCurrentPage(1);
              }}
              className="h-7 min-w-[120px] rounded-none border border-black bg-white px-2 text-[12px]"
            >
              <option value="">All types</option>
              {ASSET_TYPE_OPTIONS.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
            <input
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Owner, reg no..."
              className="h-7 w-44 border border-black bg-white px-2 text-[12px] focus:outline-none"
            />
            <Button
              size="sm"
              variant="primary"
              leftIcon={<Search className="h-3 w-3" />}
              onClick={handleSearch}
              className="h-7 px-2 text-[12px]"
            >
              Search
            </Button>
          </div>

          <Button
            size="sm"
            variant="success"
            leftIcon={<Plus className="h-3.5 w-3.5" />}
            onClick={() => setAddOpen(true)}
            className="h-7 rounded-none px-3 text-[12px] font-bold"
          >
            Add Single
          </Button>
        </div>

        <div className="shrink-0 bg-[#7f7a7b] px-3 py-1 text-center text-[14px] font-bold uppercase text-white">
          Active Agreements
        </div>

        <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <div className="min-h-0 flex-1 overflow-auto">
            <table className="w-full border-collapse text-[13px]">
              <thead>
                <tr className="sticky top-0 z-10 border-b border-[#8f8f8f] bg-white text-left divide-x divide-[#8f8f8f]">
                  <th className="px-2 py-2 font-bold text-black">
                    <button
                      type="button"
                      onClick={() => toggleSort('date')}
                      className="flex items-center gap-1"
                    >
                      Lodge Date
                      {activeSortField === 'date' ? (
                        activeSortDirection === 'asc' ? (
                          <ArrowUp className="h-3 w-3" />
                        ) : (
                          <ArrowDown className="h-3 w-3" />
                        )
                      ) : (
                        <ArrowUpDown className="h-3 w-3" />
                      )}
                    </button>
                  </th>
                  <th className="px-2 py-2 font-bold text-black">Regist. No.</th>
                  <th className="px-2 py-2 font-bold text-black">
                    <button
                      type="button"
                      onClick={() => toggleSort('name')}
                      className="flex items-center gap-1"
                    >
                      Owner
                      {activeSortField === 'name' ? (
                        activeSortDirection === 'asc' ? (
                          <ArrowUp className="h-3 w-3" />
                        ) : (
                          <ArrowDown className="h-3 w-3" />
                        )
                      ) : (
                        <ArrowUpDown className="h-3 w-3" />
                      )}
                    </button>
                  </th>
                  <th className="px-2 py-2 font-bold text-black">Description</th>
                  <th className="px-2 py-2 font-bold text-black">Reg/Serial</th>
                  <th className="px-2 py-2 font-bold text-black">Currency</th>
                  <th className="px-2 py-2 font-bold text-black text-right">
                    Est. Value
                  </th>
                  <th className="px-2 py-2 font-bold text-black">Sub. Start</th>
                  <th className="px-2 py-2 font-bold text-black">Sub. End</th>
                  <th className="px-2 py-2 font-bold text-black" />
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <TableSkeleton rows={8} cols={10} />
                ) : !sortedRecords.length ? (
                  <EmptyState message="No assets found." />
                ) : (
                  sortedRecords.map((rec, idx) => (
                    <tr
                      key={rec.id}
                      className={cn(
                        'border-b border-[#8f8f8f]',
                        idx % 2 === 0 ? 'bg-white' : 'bg-[#fafafa]',
                      )}
                    >
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.lodge_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 font-medium text-[#196A86]">
                        {rec.registration_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.owner_name}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.asset_description}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.serial_number || rec.mv_registration_no}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.currency}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 text-right">
                        {formatCurrency(rec.estimated_value)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.subscription_start_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.subscription_end_date)}
                      </td>
                      <td className="px-2 py-2">
                        <button
                          type="button"
                          onClick={() => setViewRecord(rec)}
                          className="bg-[#196A86] px-2 py-1 text-[11px] font-bold text-white hover:bg-[#15586f]"
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

          <NumberedPaginationFooter
            startItem={startItem}
            endItem={endItem}
            totalRecords={totalRecords}
            activePage={activePage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      </div>

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
            refreshList(true);
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {viewRecord && (
        <AssetViewModal
          record={viewRecord}
          onClose={() => setViewRecord(null)}
          onSaved={() => {
            setViewRecord(null);
            refreshList(false);
          }}
          onDeleted={() => {
            setViewRecord(null);
            refreshList(false);
          }}
        />
      )}
    </div>
  );
}
