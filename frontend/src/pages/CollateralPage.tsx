import { useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { ArrowDown, ArrowUp, ArrowUpDown, Plus, Search } from 'lucide-react';
import { collateralApi } from '@/api/collateralApi';
import { StatCard } from '@/components/shared/StatCard';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { CollateralForm } from '@/components/collateral/CollateralForm';
import { CollateralViewModal } from '@/components/collateral/CollateralViewModal';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import type { CollateralRecord, CollateralSearchField } from '@/types';

const PAGE_SIZE = 8;

type CollateralSortOption = 'date-desc' | 'date-asc' | 'name-asc' | 'name-desc';

const SEARCH_OPTIONS: { value: CollateralSearchField; label: string }[] = [
  { value: 'agreement_number', label: 'Agreement Number' },
  { value: 'debtor', label: 'Debtor' },
  { value: 'reg_serial_number', label: 'Reg/Serial Number' },
  { value: 'financier', label: 'Financier' },
];

export default function CollateralPage() {
  const queryClient = useQueryClient();
  const [searchField, setSearchField] =
    useState<CollateralSearchField>('agreement_number');
  const [searchValue, setSearchValue] = useState('');
  const [sortOption, setSortOption] =
    useState<CollateralSortOption>('date-desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [appliedSearch, setAppliedSearch] = useState<{
    field?: string;
    value?: string;
  }>({});
  const [addOpen, setAddOpen] = useState(false);
  const [viewRecord, setViewRecord] = useState<CollateralRecord | null>(null);

  const { data: statsData } = useQuery({
    queryKey: ['collateral-dashboard', appliedSearch],
    queryFn: () =>
      collateralApi.getDashboard(
        appliedSearch.value
          ? {
              search_field: appliedSearch.field,
              search_value: appliedSearch.value,
            }
          : undefined,
      ),
  });

  const {
    data: recordsData,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['collateral-records', appliedSearch],
    queryFn: () =>
      collateralApi.getRecords(
        appliedSearch.value ? { search: appliedSearch.value } : undefined,
      ),
  });

  const handleSearch = () => {
    setAppliedSearch({ field: searchField, value: searchValue });
    setCurrentPage(1);
  };

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
        return `${field}-${currentDirection === 'asc' ? 'desc' : 'asc'}` as CollateralSortOption;
      }

      return field === 'date' ? 'date-desc' : 'name-asc';
    });
    setCurrentPage(1);
  };

  const sortedRecords = useMemo(() => {
    const rows = [...(recordsData ?? [])];

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

  const pagedRecords = useMemo(() => {
    if (!sortedRecords) {
      return [] as CollateralRecord[];
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
          label="Active Agreements"
          value={statsData?.active_agreements ?? 0}
        />
        <StatCard
          label="Pending Discharge Confirmation"
          value={statsData?.pending_discharge_confirmation ?? 0}
        />
      </div>

      <div className="flex min-h-0 flex-1 flex-col overflow-hidden border border-[#8f8f8f] bg-white">
        <div className="bg-[#7f7a7b] px-4 py-2.5 text-center text-[18px] font-bold uppercase tracking-wide text-white">
          Collateral Registry
        </div>

        <div className="flex flex-wrap items-end justify-between gap-6 border-b border-[#8f8f8f] px-4 py-8">
          <div className="flex flex-wrap items-end gap-4">
            <div className="flex items-center gap-3">
              <span className="text-[18px] font-bold text-black">Search</span>
              <select
                value={searchField}
                onChange={(e) =>
                  setSearchField(e.target.value as CollateralSearchField)
                }
                className="h-9 min-w-[180px] rounded-none border-2 border-black bg-white px-3 text-sm text-black focus:outline-none"
              >
                {SEARCH_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>
                    {o.label}
                  </option>
                ))}
              </select>
              <input
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Agreement Number"
                className="h-9 w-64 rounded-none border-2 border-black bg-white px-3 text-sm text-black placeholder:text-slate-500 focus:outline-none"
              />
              <Button
                size="sm"
                variant="primary"
                leftIcon={<Search className="h-3.5 w-3.5" />}
                onClick={handleSearch}
              >
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
              className="min-w-[110px] rounded-none border-r-0 text-[15px] font-bold text-white"
            >
              + Add Single
            </Button>
            <Button
              size="sm"
              variant="danger"
              leftIcon={<Plus className="h-3.5 w-3.5" />}
              className="min-w-[120px] rounded-none text-[15px] font-bold text-white"
            >
              + Add Multiple
            </Button>
          </div>
        </div>

        <div className="border-t border-[#8f8f8f] bg-[#7f7a7b] px-4 py-2 text-center text-[16px] font-bold uppercase text-white">
          Active Debts
        </div>

        <div className="min-h-0 flex-1 overflow-hidden">
          <div className="h-full min-h-0 overflow-auto">
            <table className="w-full border-collapse text-[14px]">
              <thead>
                <tr className="sticky top-0 z-10 border-b border-[#8f8f8f] bg-white text-left divide-x divide-[#8f8f8f]">
                  <th className="w-8 px-3 py-3 font-bold text-black">#</th>
                  <th className="px-3 py-3 font-bold text-black">
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
                  <th className="px-3 py-3 font-bold text-black">
                    Agreement No.
                  </th>
                  <th className="px-3 py-3 font-bold text-black">
                    <button
                      type="button"
                      onClick={() => toggleSort('name')}
                      className="flex items-center gap-1"
                      title="Sort by debtor name"
                    >
                      <span>Debtor</span>
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
                  <th className="px-3 py-3 font-bold text-black">
                    Asset Description
                  </th>
                  <th className="px-3 py-3 font-bold text-black">
                    Reg/Serial No.
                  </th>
                  <th className="px-3 py-3 font-bold text-black">Currency</th>
                  <th className="px-3 py-3 text-right font-bold text-black">
                    Loan Amount
                  </th>
                  <th className="px-3 py-3 font-bold text-black">Start Date</th>
                  <th className="px-3 py-3 font-bold text-black">End Date</th>
                  <th className="px-3 py-3 font-bold text-black"></th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <TableSkeleton rows={5} cols={11} />
                ) : isError ? (
                  <tr>
                    <td
                      colSpan={11}
                      className="py-8 text-center text-sm text-red-500"
                    >
                      Failed to load records. Please try again.
                    </td>
                  </tr>
                ) : !pagedRecords.length ? (
                  <EmptyState message="No collateral agreements found." />
                ) : (
                  pagedRecords.map((rec, idx) => (
                    <tr
                      key={rec.id}
                      className={cn(
                        'border-b border-[#8f8f8f]',
                        ((currentPage - 1) * PAGE_SIZE + idx) % 2 === 0
                          ? 'bg-white'
                          : 'bg-[#f7f7f7]',
                      )}
                    >
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-center text-slate-700">
                        {idx + 1}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-700">
                        {formatDate(rec.lodge_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle font-bold text-[#196A86]">
                        {rec.agreement_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-800">
                        {rec.debtor_name}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-800">
                        {rec.asset_description}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-700">
                        {rec.serial_number || rec.asset_registration_no}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-center text-slate-700">
                        {rec.currency}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-right text-slate-800">
                        {formatCurrency(rec.loan_amount)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-700">
                        {formatDate(rec.start_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-3 py-2.5 align-middle text-slate-700">
                        {formatDate(rec.end_date)}
                      </td>
                      <td className="px-3 py-2.5 align-middle">
                        <button
                          onClick={() => setViewRecord(rec)}
                          className="min-w-[72px] rounded-none bg-[#196A86] px-3 py-2 text-sm font-bold text-white transition-colors hover:bg-[#15586f]"
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

      {/* ── Add Collateral Modal ── */}
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
            queryClient.invalidateQueries({
              queryKey: ['collateral-dashboard'],
            });
            queryClient.invalidateQueries({ queryKey: ['collateral-records'] });
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
            setViewRecord(null);
            queryClient.invalidateQueries({
              queryKey: ['collateral-dashboard'],
            });
            queryClient.invalidateQueries({ queryKey: ['collateral-records'] });
          }}
        />
      )}
    </div>
  );
}
