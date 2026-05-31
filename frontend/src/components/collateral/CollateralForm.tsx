import { useEffect, useState } from 'react';
import { useForm, useFormState, Controller } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { collateralApi } from '@/api/collateralApi';
import { individualsApi } from '@/api/individualsApi';
import { companiesApi } from '@/api/companiesApi';
import { clientsApi } from '@/api/clientsApi';
import { Input } from '@/components/ui/input';
import AutocompleteInput from '@/components/shared/AutocompleteInput';
import { Select } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { FormSectionHeader } from '@/components/shared/FormSectionHeader';
import { FieldError } from '@/components/shared/FieldError';
import {
  COLLATERAL_ASSET_TYPE_OPTIONS,
  COLLATERAL_ASSET_TYPE_VALUES,
  ASSET_CONDITIONS,
  CURRENCIES,
} from '@/types';

const schema = z.object({
  financier_type: z.enum(['individual', 'company']),
  financier_id: z
    .number({ error: 'Financier is required' })
    .min(1, 'Financier is required'),
  data_source_name: z.string().min(1, 'Required'),
  data_source_position: z.string().optional(),
  data_date: z.string().min(1, 'Required'),
  debtor_type: z.enum(['individual', 'company']),
  debtor_id: z
    .number({ error: 'Debtor is required' })
    .min(1, 'Debtor is required'),
  agreement_number: z.string().min(1, 'Required'),
  asset_type: z
    .string()
    .min(1, 'Select asset type')
    .refine(
      (v) => (COLLATERAL_ASSET_TYPE_VALUES as readonly string[]).includes(v),
      'Select asset type',
    ),
  asset_make: z.string().min(1, 'Required'),
  asset_model: z.string().min(1, 'Required'),
  asset_year: z.coerce.number().min(1900).max(2100),
  asset_condition: z.enum([
    'new',
    'second_hand',
    'reconditioned',
    'non_functioning',
  ]),
  asset_registration_no: z.string().optional(),
  chassis_number: z.string().optional(),
  engine_number: z.string().optional(),
  serial_number: z.string().optional(),
  currency: z.enum(['USD', 'ZWL', 'ZAR', 'GBP', 'EUR']),
  loan_amount: z.coerce.number().min(0),
  instalment_amount: z.coerce.number().min(0),
  instalment_date: z.coerce.number().min(1).max(31),
  total_paid_to_date: z.coerce.number().min(0),
  balance: z.coerce.number().min(0),
  start_date: z.string().min(1),
  end_date: z.string().min(1),
});

type FormValues = z.infer<typeof schema>;

interface CollateralFormProps {
  initial?: Partial<FormValues>;
  financierDisplayLabel?: string;
  debtorDisplayLabel?: string;
  onSuccess: () => void;
  onCancel: () => void;
  isEdit?: boolean;
  recordId?: number;
}

export function CollateralForm({
  initial,
  financierDisplayLabel,
  debtorDisplayLabel,
  onSuccess,
  onCancel,
  isEdit,
  recordId,
}: CollateralFormProps) {
  const [assetType, setAssetType] = useState(initial?.asset_type ?? '');

  const {
    register,
    handleSubmit,
    control,
    watch,
    setError,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: 'onSubmit',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      financier_type: 'company',
      debtor_type: 'individual',
      data_date: new Date().toISOString().split('T')[0],
      currency: 'USD',
      asset_year: new Date().getFullYear(),
      asset_condition: 'new',
      total_paid_to_date: 0,
      balance: 0,
      ...initial,
    },
  });

  const { errors } = useFormState({ control });

  const watchedAssetType = watch('asset_type');
  const isVehicle = watchedAssetType === 'vehicles';

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (data: FormValues) =>
      isEdit && recordId
        ? collateralApi.updateRecord(recordId, data as any)
        : collateralApi.createRecord(data as any),
    onSuccess,
    onError: (err: unknown) => {
      if (!applyApiValidationErrors(setError, err)) {
        const data = (err as { response?: { data?: { message?: string; error?: string } } })
          ?.response?.data;
        toast.error(
          data?.message ?? data?.error ?? 'Failed to save record',
        );
      } else {
        toast.error('Please fix the highlighted fields');
      }
    },
  });

  const onInvalid = () => {
    toast.error('Please fix the highlighted fields');
  };

  return (
    <form
      onSubmit={handleSubmit((d) => submit(d), onInvalid)}
      className="bg-white"
      noValidate
    >
      {/* ── Financier Section ── */}
      <FormSectionHeader title="Financier" variant="teal" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <div>
          <label className="text-xs font-medium text-slate-600">
            Financier Type
          </label>
          <select
            {...register('financier_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            <option value="company">Company</option>
            <option value="individual">Individual</option>
          </select>
        </div>
        <div className="col-span-2">
          <Controller
            name="financier_id"
            control={control}
            render={({ field }) => (
              <AutocompleteInput
                label="Name / ID / Reg. No."
                placeholder="Search financier..."
                queryKey="collateral-financier"
                displayLabel={financierDisplayLabel}
                fetchFn={clientsApi.searchClients}
                error={errors.financier_id?.message}
                value={field.value}
                onBlur={field.onBlur}
                onChange={(v) => field.onChange(Number(v))}
              />
            )}
          />
        </div>
        <Input
          label="Data Source Name"
          {...register('data_source_name')}
          error={errors.data_source_name?.message}
          required
        />
        <Input
          label="Data Date"
          type="date"
          {...register('data_date')}
          error={errors.data_date?.message}
          required
        />
        <Input label="Position" {...register('data_source_position')} />
      </div>

      {/* ── Debtor Section ── */}
      <FormSectionHeader title="Debtor" variant="teal" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <div>
          <label className="text-xs font-medium text-slate-600">
            Debtor Type
          </label>
          <select
            {...register('debtor_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            <option value="individual">Individual</option>
            <option value="company">Company</option>
          </select>
        </div>
        <div className="col-span-3">
          <Controller
            name="debtor_id"
            control={control}
            render={({ field }) => (
              <AutocompleteInput
                label="Name / ID / Reg. No."
                placeholder="Search debtor..."
                queryKey={`collateral-debtor-${watch('debtor_type')}`}
                displayLabel={debtorDisplayLabel}
                fetchFn={(q) =>
                  watch('debtor_type') === 'company'
                    ? companiesApi.searchBranches(q)
                    : individualsApi.searchIndividuals(q)
                }
                error={errors.debtor_id?.message}
                value={field.value}
                onBlur={field.onBlur}
                onChange={(v) => field.onChange(Number(v))}
              />
            )}
          />
        </div>
      </div>

      {/* ── Agreement & Asset Details ── */}
      <FormSectionHeader title="Agreement & Asset Details" variant="dark" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <Input
          label="Agreement Number"
          {...register('agreement_number')}
          error={errors.agreement_number?.message}
          required
        />
        <div>
          <label className="text-xs font-medium text-slate-600">
            Asset Type<span className="text-red-500 ml-0.5">*</span>
          </label>
          <select
            {...register('asset_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            <option value="">Click to select an option</option>
            {COLLATERAL_ASSET_TYPE_OPTIONS.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
          <FieldError message={errors.asset_type?.message} />
        </div>
        <Input
          label="Make"
          {...register('asset_make')}
          error={errors.asset_make?.message}
          required
        />
        <Input
          label="Model"
          {...register('asset_model')}
          error={errors.asset_model?.message}
          required
        />
        <Input
          label="Year"
          type="number"
          {...register('asset_year')}
          error={errors.asset_year?.message}
          required
        />
        <div>
          <label className="text-xs font-medium text-slate-600">
            Condition
          </label>
          <select
            {...register('asset_condition')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            {ASSET_CONDITIONS.map((c) => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="MV Registration No."
          {...register('asset_registration_no')}
          disabled={!isVehicle}
          className={!isVehicle ? 'bg-slate-100' : ''}
        />
        <Input
          label="Chassis Number"
          {...register('chassis_number')}
          disabled={!isVehicle}
          className={!isVehicle ? 'bg-slate-100' : ''}
        />
        <Input
          label="Engine Number"
          {...register('engine_number')}
          disabled={!isVehicle}
          className={!isVehicle ? 'bg-slate-100' : ''}
        />
        <Input label="Serial Number" {...register('serial_number')} />
      </div>

      {/* ── Financial Details ── */}
      <FormSectionHeader title="Financial Details" variant="teal" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <div>
          <label className="text-xs font-medium text-slate-600">
            Currency<span className="text-red-500 ml-0.5">*</span>
          </label>
          <select
            {...register('currency')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            {CURRENCIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Total Debt"
          type="number"
          step="0.01"
          {...register('loan_amount')}
          error={errors.loan_amount?.message}
          required
        />
        <Input
          label="Instalment Amount"
          type="number"
          step="0.01"
          {...register('instalment_amount')}
        />
        <Input
          label="Instalment Date (dd)"
          type="number"
          min="1"
          max="31"
          {...register('instalment_date')}
        />
        <Input
          label="Total Paid to Date"
          type="number"
          step="0.01"
          {...register('total_paid_to_date')}
        />
        <Input
          label="Balance"
          type="number"
          step="0.01"
          {...register('balance')}
        />
        <Input
          label="Agreement Start Date"
          type="date"
          {...register('start_date')}
          error={errors.start_date?.message}
          required
        />
        <Input
          label="Agreement End Date"
          type="date"
          {...register('end_date')}
          error={errors.end_date?.message}
          required
        />
      </div>

      {/* ── Footer ── */}
      <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-4 py-3">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" loading={isPending}>
          {isEdit ? 'Save Changes' : 'Upload'}
        </Button>
      </div>
    </form>
  );
}
