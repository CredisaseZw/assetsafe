import { useEffect, useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import {
  ArrowDown,
  ArrowUp,
  ArrowUpDown,
  Building2,
  Eye,
  Plus,
  Search,
} from 'lucide-react';
import { hirePurchaseApi } from '@/api/hirePurchaseApi';
import { clientsApi } from '@/api/clientsApi';
import { InlineStat } from '@/components/shared/InlineStat';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { HirePurchaseForm } from '@/components/hire-purchase/HirePurchaseForm';
import { HirePurchaseViewModal } from '@/components/hire-purchase/HirePurchaseViewModal';
import { NumberedPaginationFooter } from '@/components/shared/NumberedPaginationFooter';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import { invalidateRegistryQueries } from '@/lib/registryCache';
import type { HirePurchaseRecord } from '@/types';

const PAGE_SIZE = 16;

type HirePurchaseSortOption =
  | 'date-desc'
  | 'date-asc'
  | 'name-asc'
  | 'name-desc';

export default function HirePurchasePage() {
  const queryClient = useQueryClient();
  const [financierQuery, setFinancierQuery] = useState('');
  const [selectedFinancier, setSelectedFinancier] = useState('');
  const [selectedFinancierLabel, setSelectedFinancierLabel] = useState('');
  const [sortOption, setSortOption] =
    useState<HirePurchaseSortOption>('date-desc');
  const [currentPage, setCurrentPage] = useState(1);
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
    queryKey: ['hp-records', selectedFinancier, currentPage],
    queryFn: () =>
      hirePurchaseApi.getRecords({
        ...(selectedFinancier
          ? { financier_id: Number(selectedFinancier) }
          : {}),
        page: currentPage,
        page_size: PAGE_SIZE,
      }),
  });

  const handleFinancierSearch = async () => {
    const q = financierQuery.trim();
    if (!q) {
      setSelectedFinancier('');
      setSelectedFinancierLabel('');
      setCurrentPage(1);
      return;
    }
    const results = await clientsApi.searchClients(q);
    if (results.length === 1) {
      const client = results[0];
      setSelectedFinancier(String(client.id));
      setSelectedFinancierLabel(
        client.name ?? client.trading_name ?? String(client.id),
      );
      setCurrentPage(1);
      return;
    }
    if (results.length > 1) {
      const first = results[0];
      setSelectedFinancier(String(first.id));
      setSelectedFinancierLabel(first.name ?? first.trading_name ?? '');
      setCurrentPage(1);
      toast.message(`Showing results for ${first.name ?? 'first match'}`);
      return;
    }
    toast.error('No financier found');
  };

  const refreshList = (clearFilters = false) => {
    if (clearFilters) {
      setFinancierQuery('');
      setSelectedFinancier('');
      setSelectedFinancierLabel('');
    }
    setCurrentPage(1);
    invalidateRegistryQueries(queryClient, 'hp');
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
        return `${field}-${currentDirection === 'asc' ? 'desc' : 'asc'}` as HirePurchaseSortOption;
      }

      return field === 'date' ? 'date-desc' : 'name-asc';
    });
    setCurrentPage(1);
  };

  const sortedRecords = useMemo(() => {
    if (!recordsData?.records) {
      return [] as HirePurchaseRecord[];
    }

    const compareDate = (left: HirePurchaseRecord, right: HirePurchaseRecord) => {
      const leftTime = new Date(left.lodge_date ?? '').getTime();
      const rightTime = new Date(right.lodge_date ?? '').getTime();
      return leftTime - rightTime;
    };

    const compareName = (left: HirePurchaseRecord, right: HirePurchaseRecord) =>
      (left.purchaser_name ?? '').localeCompare(right.purchaser_name ?? '', undefined, {
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
        <div className="bg-[#7f7a7b] px-3 py-1.5 text-center text-[15px] font-bold uppercase tracking-wide text-white">
          Hire Purchase Registry
        </div>

        <div className="flex flex-wrap items-center gap-3 border-b border-[#8f8f8f] bg-[#f8f7f2] px-3 py-2">
          <InlineStat
            label="Financiers"
            value={statsData?.number_of_financiers ?? 0}
          />
          <InlineStat
            label="Active"
            value={statsData?.active_agreements ?? 0}
          />
          <InlineStat
            label="Pending Closure"
            value={statsData?.pending_closure_confirmation ?? 0}
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#8f8f8f] px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[12px] font-bold text-black">Search</span>
            <Building2 className="h-3 w-3" />
            <input
              value={financierQuery}
              onChange={(e) => setFinancierQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && void handleFinancierSearch()}
              placeholder={
                selectedFinancierLabel || 'Financier name...'
              }
              className="h-7 w-52 border border-black bg-white px-2 text-[12px] focus:outline-none"
            />
            <Button
              size="sm"
              variant="primary"
              leftIcon={<Search className="h-3 w-3" />}
              onClick={() => void handleFinancierSearch()}
              className="h-7 px-2 text-[12px]"
            >
              Search
            </Button>
            {selectedFinancier ? (
              <button
                type="button"
                className="text-[11px] text-[#196A86] underline"
                onClick={() => {
                  setSelectedFinancier('');
                  setSelectedFinancierLabel('');
                  setFinancierQuery('');
                  setCurrentPage(1);
                }}
              >
                Clear filter
              </button>
            ) : null}
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
          Active Agreements
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
                  <th className="px-2 py-2 font-bold">Agreement</th>
                  <th className="px-2 py-2 font-bold">
                    <button
                      type="button"
                      onClick={() => toggleSort('name')}
                      className="flex items-center gap-1"
                    >
                      Purchaser
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
                  <th className="px-2 py-2 font-bold text-right">Amount</th>
                  <th className="px-2 py-2 font-bold">Start</th>
                  <th className="px-2 py-2 font-bold">End</th>
                  <th className="px-2 py-2 font-bold" />
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <TableSkeleton rows={8} cols={11} />
                ) : !sortedRecords.length ? (
                  <EmptyState message="No hire purchase agreements found." />
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
                        {(activePage - 1) * PAGE_SIZE + idx + 1}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {formatDate(rec.lodge_date)}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 font-medium text-[#196A86]">
                        {rec.agreement_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.purchaser_name}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.asset_make} {rec.asset_model}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.reg_serial_number}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2">
                        {rec.currency}
                      </td>
                      <td className="border-r border-[#8f8f8f] px-2 py-2 text-right">
                        {formatCurrency(rec.purchase_amount)}
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
                          className="flex items-center gap-1 bg-[#196A86] px-2 py-1 text-[11px] font-bold text-white hover:bg-[#15586f]"
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
        title="Hire Purchase Form"
        size="xl"
      >
        <HirePurchaseForm
          onSuccess={() => {
            setAddOpen(false);
            toast.success('Hire purchase record created successfully');
            refreshList(true);
          }}
          onCancel={() => setAddOpen(false)}
        />
      </Modal>

      {viewRecord && (
        <HirePurchaseViewModal
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
