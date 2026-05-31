import { useForm, useFormState } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { companiesApi } from '@/api/companiesApi';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const schema = z.object({
  registration_number: z.string().min(1, 'Required'),
  registration_name: z.string().min(1, 'Required'),
  trading_name: z.string().min(1, 'Required'),
  legal_status: z.string().optional(),
  industry: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

interface CompanyCreateFormProps {
  onSuccess: (result: { id: number; name: string }) => void;
  onCancel: () => void;
}

export function CompanyCreateForm({
  onSuccess,
  onCancel,
}: CompanyCreateFormProps) {
  const { register, handleSubmit, setError, control } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: 'onSubmit',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: { legal_status: 'private' },
  });

  const { errors } = useFormState({ control });

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (values: FormValues) => companiesApi.createCompany(values),
    onSuccess: (result) => {
      toast.success('Company created');
      onSuccess(result);
    },
    onError: (err: unknown) => {
      if (!applyApiValidationErrors(setError, err)) {
        const data = (err as { response?: { data?: { message?: string; error?: string } } })
          ?.response?.data;
        toast.error(
          data?.message ?? data?.error ?? 'Failed to create company',
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
          label="Registration Number"
          {...register('registration_number')}
          error={errors.registration_number?.message}
          required
        />
        <Input
          label="Registration Name"
          {...register('registration_name')}
          error={errors.registration_name?.message}
          required
        />
        <Input
          label="Trading Name"
          {...register('trading_name')}
          error={errors.trading_name?.message}
          required
          className="col-span-2"
        />
        <Input label="Legal Status" {...register('legal_status')} />
        <Input label="Industry" {...register('industry')} />
      </div>
      <div className="flex justify-end gap-2 border-t border-slate-200 pt-3">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" loading={isPending}>
          Create Company
        </Button>
      </div>
    </form>
  );
}
