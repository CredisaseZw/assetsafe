import { FileSearch } from 'lucide-react'

interface EmptyStateProps {
  message?: string
}

export function EmptyState({ message = 'No records found.' }: EmptyStateProps) {
  return (
    <tr>
      <td colSpan={100} className="py-14 text-center">
        <div className="flex flex-col items-center gap-2 text-slate-400">
          <FileSearch className="h-8 w-8" />
          <p className="text-sm">{message}</p>
        </div>
      </td>
    </tr>
  )
}
