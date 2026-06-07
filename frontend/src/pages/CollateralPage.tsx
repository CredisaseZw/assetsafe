import { useEffect, useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { ArrowDown, ArrowUp, ArrowUpDown, Plus, Search } from 'lucide-react';
import { collateralApi } from '@/api/collateralApi';
import { InlineStat } from '@/components/shared/InlineStat';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { CollateralForm } from '@/components/collateral/CollateralForm';
import { CollateralViewModal } from '@/components/collateral/CollateralViewModal';
import { NumberedPaginationFooter } from '@/components/shared/NumberedPaginationFooter';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import { invalidateRegistryQueries } from '@/lib/registryCache';
import { registryQueryOptions } from '@/lib/registryQueryOptions';
import { useAuthStore } from '@/store';
import type { CollateralRecord } from '@/types';

const PAGE_SIZE = 20;

type CollateralSortOption = 'date-desc' | 'date-asc' | 'name-asc' | 'name-desc';

export default function CollateralPage() {
  const queryClient = useQueryClient();
  const authReady = useAuthStore((s) => s.authReady);
  const [searchValue, setSearchValue] = useState('');
  const [sortOption, setSortOption] =
    useState<CollateralSortOption>('date-desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [appliedSearch, setAppliedSearch] = useState('');
  const [addOpen, setAddOpen] = useState(false);
  const [viewRecord, setViewRecord] = useState<CollateralRecord | null>(null);

  const { data: statsData } = useQuery({
    queryKey: ['collateral-dashboard'],
    queryFn: () => collateralApi.getDashboard(),
    enabled: authReady,
    ...registryQueryOptions,
  });

  const {
    data: recordsData,
    isLoading,
    isError,
    isFetching,
  } = useQuery({
    queryKey: ['collateral-records', appliedSearch, currentPage],
    queryFn: () =>
      collateralApi.getRecords({
        ...(appliedSearch ? { search: appliedSearch } : {}),
        page: currentPage,
        page_size: PAGE_SIZE,
      }),
    enabled: authReady,
    ...registryQueryOptions,
  });

  const loadingRecords = !authReady || isLoading || isFetching;

  const handleSearch = () => {
    setAppliedSearch(searchValue.trim());
    setCurrentPage(1);
  };

  const refreshList = (clearFilters = false) => {
    if (clearFilters) {
      setSearchValue('');
      setAppliedSearch('');
    }
    setCurrentPage(1);
    invalidateRegistryQueries(queryClient, 'collateral');
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
        return `${field}-${currentDirection === 'asc' ? 'desc' : 'asc'}` as CollateralSortOption;
      }

      return field === 'date' ? 'date-desc' : 'name-asc';
    });
    setCurrentPage(1);
  };

  const sortedRecords = useMemo(() => {
    const rows = [...(recordsData?.records ?? [])];

    rows.sort((left, right) => {
      if (activeSortField === 'date') {
        const leftTime = new Date(left.lodge_date ?? '').getTime();
        const rightTime = new Date(right.lodge_date ?? '').getTime();
        return activeSortDirection === 'asc'
          ? leftTime - rightTime
          : rightTime - leftTime;
      }

      const leftName = (left.debtor_name ?? '').toLowerCase();
      const rightName = (right.debtor_name ?? '').toLowerCase();
      return activeSortDirection === 'asc'
        ? leftName.localeCompare(rightName)
        : rightName.localeCompare(leftName);
    });

    return rows;
  }, [activeSortDirection, activeSortField, recordsData]);

  const startItem = totalRecords === 0 ? 0 : (activePage - 1) * PAGE_SIZE + 1;
  const endItem = Math.min(activePage * PAGE_SIZE, totalRecords);

  return (
    <div className="flex h-full min-h-0 flex-col overflow-hidden">
      <div className="flex h-full min-h-0 flex-1 flex-col overflow-hidden border border-[#8f8f8f] bg-white">
        <div className="bg-[#7f7a7b] px-3 py-1.5 text-center text-[15px] font-bold uppercase tracking-wide text-white">
          Collateral Registry
        </div>

        <div className="flex flex-wrap items-center gap-4 border-b border-[#8f8f8f] bg-[#f8f7f2] px-3 py-2">
          <InlineStat
            label="Active Agreements"
            value={statsData?.active_agreements ?? 0}
          />
          <InlineStat
            label="Pending Discharge"
            value={statsData?.pending_discharge_confirmation ?? 0}
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#8f8f8f] px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[12px] font-bold text-black">Search</span>
            <input
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Agreement, debtor, reg..."
              className="h-7 w-56 border border-black bg-white px-2 text-[12px] focus:outline-none"
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

        <div className="bg-[#7f7a7b] px-3 py-1 text-center text-[14px] font-bold uppercase text-white">
          Active Debts
        </div>

        <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
          <div className="min-h-0 flex-1 overflow-auto">
            <table className="w-full border-collapse text-[13px]">
              <thead>
                <tr className="sticky top-0 z-10 border-b border-[#8f8f8f] bg-white text-left divide-x divide-[#8f8f8f]">
                  <th className="w-8 px-2 py-2 font-bold">#</th>
                  <th className="px-2 py-2 font-bold">
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
                  <th className="px-2 py-2 font-bold">Agreement No.</th>
                  <th className="px-2 py-2 font-bold">
                    <button
                      type="button"
                      onClick={() => toggleSort('name')}
                      className="flex items-center gap-1"
                    >
                      Debtor
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
                  <th className="px-2 py-2 font-bold">Asset</th>
                  <th className="px-2 py-2 font-bold">Reg/Serial</th>
                  <th className="px-2 py-2 font-bold">Currency</th>
                  <th className="px-2 py-2 font-bold text-right">Loan</th>
                  <th className="px-2 py-2 font-bold">Start</th>
                  <th className="px-2 py-2 font-bold">End</th>
                  <th className="px-2 py-2 font-bold" />
                </tr>
              </thead>
              <tbody>
                {loadingRecords ? (
                  <TableSkeleton rows={8} cols={11} />
                ) : isError ? (
                  <tr>
                    <td colSpan={11} className="py-6 text-center text-red-500">
                      Failed to load records.
                    </td>
                  </tr>
                ) : !sortedRecords.length ? (
                  <EmptyState message="No collateral agreements found." />
                ) : (
                  sortedRecords.map((rec, idx) => (
                    <tr
                      key={rec.id}
                      className={cn(
                        'border-b border-[#8f8f8f]',
                        idx % 2 === 0 ? 'bg-white' : 'bg-[#f7f7f7]',
                      )}
                    >
                      <td className="border-r border-[#8f8f8f] px-2 py-2 text-center">
                        {(activePage - 1) * PAGE_SIZE + idx + 1}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.lodge_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 font-bold text-[#196A86]">
                        {rec.agreement_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.debtor_name}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.asset_description}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.serial_number || rec.asset_registration_no}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 text-center">
                        {rec.currency}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 text-right">
                        {formatCurrency(rec.loan_amount)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.start_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.end_date)}
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
        title="New Collateral Registration"
        size="xl"
      >
        <CollateralForm
          onSuccess={() => {
            setAddOpen(false);
            toast.success('Collateral record created successfully');
            refreshList(true);
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {viewRecord && (
        <CollateralViewModal
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
