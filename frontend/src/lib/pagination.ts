export type PaginationItemValue = number | 'ellipsis';

export function buildPaginationItems(
  currentPage: number,
  totalPages: number,
): PaginationItemValue[] {
  if (totalPages <= 7) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  if (currentPage <= 4) {
    return [1, 2, 3, 4, 5, 'ellipsis', totalPages];
  }

  if (currentPage >= totalPages - 3) {
    return [
      1,
      'ellipsis',
      totalPages - 4,
      totalPages - 3,
      totalPages - 2,
      totalPages - 1,
      totalPages,
    ];
  }

  return [
    1,
    'ellipsis',
    currentPage - 1,
    currentPage,
    currentPage + 1,
    'ellipsis',
    totalPages,
  ];
}

/**
 * Pages to keep warm for a paginated list: every page number currently rendered
 * by `buildPaginationItems`, plus the active page's immediate neighbours.
 * Always clamped to `1..totalPages` and de-duplicated.
 */
export function paginationPrefetchTargets(
  activePage: number,
  totalPages: number,
): number[] {
  if (totalPages <= 1) {
    return [];
  }

  const targets = new Set<number>();

  for (const item of buildPaginationItems(activePage, totalPages)) {
    if (item !== 'ellipsis') {
      targets.add(item);
    }
  }

  for (const neighbour of [activePage - 1, activePage + 1]) {
    if (neighbour >= 1 && neighbour <= totalPages) {
      targets.add(neighbour);
    }
  }

  return [...targets].sort((left, right) => left - right);
}
