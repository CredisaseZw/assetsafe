import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DeleteRecordButtonProps {
  label?: string;
  onDelete: () => Promise<void>;
  onDeleted: () => void;
}

export function DeleteRecordButton({
  label = 'Delete',
  onDelete,
  onDeleted,
}: DeleteRecordButtonProps) {
  const [confirming, setConfirming] = useState(false);

  const { mutate, isPending } = useMutation({
    mutationFn: onDelete,
    onSuccess: () => {
      toast.success('Record deleted');
      onDeleted();
    },
    onError: (err: any) => {
      toast.error(err?.response?.data?.message ?? 'Failed to delete record');
      setConfirming(false);
    },
  });

  if (confirming) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-xs text-red-600">Delete this record?</span>
        <Button
          type="button"
          size="sm"
          variant="danger"
          loading={isPending}
          onClick={() => mutate()}
        >
          Confirm
        </Button>
        <Button
          type="button"
          size="sm"
          variant="ghost"
          onClick={() => setConfirming(false)}
        >
          Cancel
        </Button>
      </div>
    );
  }

  return (
    <Button
      type="button"
      size="sm"
      variant="danger"
      leftIcon={<Trash2 className="h-3.5 w-3.5" />}
      onClick={() => setConfirming(true)}
    >
      {label}
    </Button>
  );
}
