import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { buildPaginationItems } from '@/lib/pagination';

interface NumberedPaginationFooterProps {
  startItem: number;
  endItem: number;
  totalRecords: number;
  activePage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function NumberedPaginationFooter({
  startItem,
  endItem,
  totalRecords,
  activePage,
  totalPages,
  onPageChange,
}: NumberedPaginationFooterProps) {
  const paginationItems = buildPaginationItems(activePage, totalPages);

  return (
    <div className="relative z-10 flex shrink-0 flex-wrap items-center justify-between gap-3 border-t-2 border-[#8f8f8f] bg-[#ebe8e2] px-4 py-3 text-sm font-medium text-slate-800 shadow-[0_-2px_8px_rgba(0,0,0,0.06)]">
      <div className="flex flex-col gap-0.5 sm:flex-row sm:items-center sm:gap-3">
        <span>
          Page {activePage} of {totalPages}
        </span>
        {totalRecords > 0 ? (
          <span className="text-slate-600">
            Showing {startItem} to {endItem} of {totalRecords} entries
          </span>
        ) : null}
      </div>
      <Pagination className="mx-0 w-auto justify-end">
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious
              disabled={activePage === 1}
              onClick={() => onPageChange(Math.max(1, activePage - 1))}
            />
          </PaginationItem>
          {paginationItems.map((item, index) => (
            <PaginationItem
              key={item === 'ellipsis' ? `ellipsis-${index}` : item}
            >
              {item === 'ellipsis' ? (
                <PaginationEllipsis />
              ) : (
                <PaginationLink
                  isActive={item === activePage}
                  onClick={() => onPageChange(item)}
                >
                  {item}
                </PaginationLink>
              )}
            </PaginationItem>
          ))}
          <PaginationItem>
            <PaginationNext
              disabled={activePage === totalPages}
              onClick={() => onPageChange(Math.min(totalPages, activePage + 1))}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
