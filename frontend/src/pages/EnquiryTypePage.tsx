import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { enquiryApi } from '@/api/enquiryApi';
import { useIsStaff } from '@/hooks/useIsStaff';
import { useEffect } from 'react';

/**
 * Internal vs external enquiry gate (staff only).
 * Client-portal users skip this and land on the search panel directly.
 */
export default function EnquiryTypePage() {
  const isStaff = useIsStaff();
  const navigate = useNavigate();

  const { mutate: startInternal, isPending } = useMutation({
    mutationFn: () => enquiryApi.createLog({ kind: 'internal' }),
    onSuccess: (log) => {
      navigate(`/enquiries/assets/search?log=${log.id}&kind=internal`, {
        replace: true,
      });
    },
    onError: () => toast.error('Could not start enquiry session'),
  });

  useEffect(() => {
    if (!isStaff) {
      navigate('/enquiries/assets/search?kind=internal', { replace: true });
    }
  }, [isStaff, navigate]);

  if (!isStaff) {
    return null;
  }

  return (
    <div className="flex min-h-0 flex-1 flex-col items-center overflow-auto px-6 py-10">
      <p className="mb-6 text-center text-[15px] text-slate-800">
        Please choose the type of enquiry:
      </p>
      <div className="flex w-full max-w-md gap-4">
        <button
          type="button"
          disabled={isPending}
          onClick={() => startInternal()}
          className="flex-1 rounded-md bg-[#2e7d32] px-6 py-4 text-center text-lg font-semibold text-white shadow hover:bg-[#256628] disabled:opacity-60"
        >
          internal
        </button>
        <Link
          to="/enquiries/assets/external"
          className="flex-1 rounded-md bg-[#c62828] px-6 py-4 text-center text-lg font-semibold text-white shadow hover:bg-[#b71c1c]"
        >
          external
        </Link>
      </div>
      <div className="mt-8 w-full max-w-lg border-t border-[#8f8f8f]" />
    </div>
  );
}
