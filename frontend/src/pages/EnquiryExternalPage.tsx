import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { enquiryApi, type RequesterOption } from '@/api/enquiryApi';
import AutocompleteInput from '@/components/shared/AutocompleteInput';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import type { SearchOption } from '@/lib/searchResults';

export default function EnquiryExternalPage() {
  const navigate = useNavigate();
  const requesterCache = useRef<Map<number, RequesterOption>>(new Map());
  const [requesterId, setRequesterId] = useState<number | undefined>();
  const [requesterLabel, setRequesterLabel] = useState('');
  const [clientId, setClientId] = useState<number | null>(null);
  const [clientName, setClientName] = useState('');
  const [branchLabel, setBranchLabel] = useState('');

  const { mutate: submit, isPending } = useMutation({
    mutationFn: () =>
      enquiryApi.createLog({
        kind: 'external',
        requester_id: requesterId,
        client_id: clientId,
        client_name: clientName,
        branch_label: branchLabel,
      }),
    onSuccess: (log) => {
      navigate(`/enquiries/assets/search?log=${log.id}&kind=external`, {
        replace: true,
      });
    },
    onError: () => toast.error('Could not log external enquiry'),
  });

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!requesterId) {
      toast.error('Select a requester');
      return;
    }
    submit();
  };

  return (
    <div className="flex min-h-0 flex-1 flex-col items-center overflow-auto px-6 py-10">
      <p className="mb-4 text-center text-[15px] text-slate-800">
        Please choose the type of enquiry:
      </p>
      <div className="mb-6 flex w-full max-w-md gap-4">
        <button
          type="button"
          className="flex-1 rounded-md bg-[#9e9e9e] px-6 py-3 text-lg font-semibold text-white"
          onClick={() => navigate('/enquiries/assets/type')}
        >
          internal
        </button>
        <button
          type="button"
          className="flex-1 rounded-md bg-[#c62828] px-6 py-3 text-lg font-semibold text-white ring-2 ring-offset-2 ring-[#c62828]"
        >
          external
        </button>
      </div>
      <div className="mb-6 w-full max-w-lg border-t border-[#8f8f8f]" />

      <form onSubmit={onSubmit} className="w-full max-w-lg space-y-4">
        <AutocompleteInput
          label="Requester"
          placeholder="Start typing to search users..."
          queryKey="enquiry-requester"
          displayLabel={requesterLabel}
          value={requesterId}
          fetchFn={async (q): Promise<SearchOption[]> => {
            const rows = await enquiryApi.searchRequesters(q);
            rows.forEach((r) => requesterCache.current.set(r.id, r));
            return rows.map((r) => ({
              id: r.id,
              name: r.label,
              subtitle: r.client_name || undefined,
            }));
          }}
          onChange={(id) => {
            if (!id) {
              setRequesterId(undefined);
              setRequesterLabel('');
              setClientId(null);
              setClientName('');
              setBranchLabel('');
              return;
            }
            const meta = requesterCache.current.get(id);
            setRequesterId(id);
            setRequesterLabel(meta?.label ?? '');
            setClientId(meta?.client_id ?? null);
            setClientName(meta?.client_name ?? '');
            setBranchLabel(meta?.branch_label ?? '');
          }}
        />
        <Input
          label="Client Name"
          value={clientName}
          readOnly
          className="bg-slate-50"
        />
        <Input
          label="Branch"
          value={branchLabel}
          readOnly
          className="bg-slate-50"
        />
        <div className="flex justify-center pt-2">
          <Button type="submit" loading={isPending} variant="secondary">
            submit
          </Button>
        </div>
      </form>
    </div>
  );
}
