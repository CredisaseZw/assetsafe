import { useForm, useFormState } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation, useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';
import { individualsApi } from '@/api/individualsApi';
import { locationsApi } from '@/api/locationsApi';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FieldError } from '@/components/shared/FieldError';

const schema = z.object({
  first_name: z.string().min(1, 'Required'),
  last_name: z.string().min(1, 'Required'),
  identification_type: z.enum(['national_id', 'passport']),
  identification_number: z.string().min(1, 'Required'),
  email: z.string().email().optional().or(z.literal('')),
  phone: z.string().min(1, 'Phone is required'),
  street_address: z.string().min(1, 'Street address is required'),
  suburb_id: z.coerce.number().min(1, 'Suburb is required'),
});

type FormValues = z.infer<typeof schema>;

interface IndividualCreateFormProps {
  onSuccess: (result: { id: number; name: string }) => void;
  onCancel: () => void;
}

export function IndividualCreateForm({
  onSuccess,
  onCancel,
}: IndividualCreateFormProps) {
  const { register, handleSubmit, setError, control } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: 'onSubmit',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      identification_type: 'national_id',
    },
  });

  const { errors } = useFormState({ control });

  const { data: suburbs = [] } = useQuery({
    queryKey: ['suburbs'],
    queryFn: () => locationsApi.searchSuburbs(),
    staleTime: 1000 * 60 * 10,
  });

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (values: FormValues) =>
      individualsApi.createIndividual({
        first_name: values.first_name,
        last_name: values.last_name,
        identification_type: values.identification_type,
        identification_number: values.identification_number,
        email: values.email || undefined,
        contact_details: [{ type: 'mobile', phone_number: values.phone }],
        addresses: [
          {
            address_type: 'residential',
            is_primary: true,
            street_address: values.street_address,
            suburb_id: values.suburb_id,
          },
        ],
      }),
    onSuccess: (result) => {
      toast.success('Individual created');
      onSuccess(result);
    },
    onError: (err: unknown) => {
      if (!applyApiValidationErrors(setError, err)) {
        const data = (err as { response?: { data?: { message?: string; error?: string } } })
          ?.response?.data;
        toast.error(
          data?.message ?? data?.error ?? 'Failed to create individual',
        );
      } else {
        toast.error('Please fix the highlighted fields');
      }
    },
  });

  return (
    <form
      onSubmit={handleSubmit(
        (d) => submit(d),
        () => toast.error('Please fix the highlighted fields'),
      )}
      className="space-y-4 p-4"
      noValidate
    >
      <div className="grid grid-cols-2 gap-3">
        <Input
          label="First Name"
          {...register('first_name')}
          error={errors.first_name?.message}
          required
        />
        <Input
          label="Last Name"
          {...register('last_name')}
          error={errors.last_name?.message}
          required
        />
        <div>
          <label className="text-xs font-medium text-slate-600">ID Type</label>
          <select
            {...register('identification_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm"
          >
            <option value="national_id">National ID</option>
            <option value="passport">Passport</option>
          </select>
        </div>
        <Input
          label="ID Number"
          {...register('identification_number')}
          error={errors.identification_number?.message}
          required
        />
        <Input label="Email" type="email" {...register('email')} />
        <Input
          label="Mobile Phone"
          {...register('phone')}
          error={errors.phone?.message}
          required
        />
        <Input
          label="Street Address"
          {...register('street_address')}
          error={errors.street_address?.message}
          required
          className="col-span-2"
        />
        <div className="col-span-2">
          <label className="text-xs font-medium text-slate-600">Suburb</label>
          <select
            {...register('suburb_id')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm"
          >
            <option value="">Select suburb...</option>
            {suburbs.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
          <FieldError message={errors.suburb_id?.message} />
        </div>
      </div>
      <div className="flex justify-end gap-2 border-t border-slate-200 pt-3">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" loading={isPending}>
          Create Individual
        </Button>
      </div>
    </form>
  );
}
