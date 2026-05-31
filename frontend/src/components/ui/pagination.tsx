import * as React from 'react';
import { ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';

const Pagination = ({ className, ...props }: React.ComponentProps<'nav'>) => (
  <nav
    role="navigation"
    aria-label="pagination"
    className={cn('mx-auto flex w-full justify-center', className)}
    {...props}
  />
);
Pagination.displayName = 'Pagination';

const PaginationContent = React.forwardRef<
  HTMLUListElement,
  React.ComponentProps<'ul'>
>(({ className, ...props }, ref) => (
  <ul
    ref={ref}
    className={cn('flex flex-wrap items-center gap-1.5', className)}
    {...props}
  />
));
PaginationContent.displayName = 'PaginationContent';

const PaginationItem = React.forwardRef<
  HTMLLIElement,
  React.ComponentProps<'li'>
>(({ className, ...props }, ref) => (
  <li ref={ref} className={cn('', className)} {...props} />
));
PaginationItem.displayName = 'PaginationItem';

type PaginationLinkProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  isActive?: boolean;
};

const PaginationLink = React.forwardRef<HTMLButtonElement, PaginationLinkProps>(
  ({ className, isActive, ...props }, ref) => (
    <button
      ref={ref}
      type="button"
      aria-current={isActive ? 'page' : undefined}
      className={cn(
        'inline-flex h-8 min-w-8 items-center justify-center rounded-sm border px-2.5 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50',
        isActive
          ? 'border-[#196A86] bg-[#196A86] text-white'
          : 'border-[#8f8f8f] bg-white text-black hover:bg-[#f1f1f1]',
        className,
      )}
      {...props}
    />
  ),
);
PaginationLink.displayName = 'PaginationLink';

type PaginationButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

const PaginationPrevious = React.forwardRef<
  HTMLButtonElement,
  PaginationButtonProps
>(({ className, ...props }, ref) => (
  <PaginationLink
    ref={ref}
    className={cn('gap-1.5 px-3', className)}
    aria-label="Go to previous page"
    {...props}
  >
    <ChevronLeft className="h-4 w-4" />
    <span>Prev</span>
  </PaginationLink>
));
PaginationPrevious.displayName = 'PaginationPrevious';

const PaginationNext = React.forwardRef<
  HTMLButtonElement,
  PaginationButtonProps
>(({ className, ...props }, ref) => (
  <PaginationLink
    ref={ref}
    className={cn('gap-1.5 px-3', className)}
    aria-label="Go to next page"
    {...props}
  >
    <span>Next</span>
    <ChevronRight className="h-4 w-4" />
  </PaginationLink>
));
PaginationNext.displayName = 'PaginationNext';

const PaginationEllipsis = ({
  className,
  ...props
}: React.ComponentProps<'span'>) => (
  <span
    aria-hidden="true"
    className={cn('inline-flex h-8 w-8 items-center justify-center', className)}
    {...props}
  >
    <MoreHorizontal className="h-4 w-4" />
    <span className="sr-only">More pages</span>
  </span>
);
PaginationEllipsis.displayName = 'PaginationEllipsis';

export {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
};
