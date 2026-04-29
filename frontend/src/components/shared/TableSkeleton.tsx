interface TableSkeletonProps {
  rows?: number
  cols?: number
}

export function TableSkeleton({ rows = 5, cols = 8 }: TableSkeletonProps) {
  return (
    <>
      {Array.from({ length: rows }).map((_, r) => (
        <tr key={r} className="animate-pulse border-b border-slate-100">
          {Array.from({ length: cols }).map((_, c) => (
            <td key={c} className="px-3 py-2.5">
              <div className="h-3.5 rounded bg-slate-200" style={{ width: `${60 + ((r * c) % 3) * 20}%` }} />
            </td>
          ))}
        </tr>
      ))}
    </>
  )
}
