import { useState } from 'react';
import { useForm, useFormState, Controller } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { assetRegistryApi } from '@/api/assetRegistryApi';
import { Input } from '@/components/ui/input';
import AutocompleteInput from '@/components/shared/AutocompleteInput';
import { individualsApi } from '@/api/individualsApi';
import { companiesApi } from '@/api/companiesApi';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/shared/Modal';
import { IndividualCreateForm } from '@/components/individuals/IndividualCreateForm';
import { CompanyCreateForm } from '@/components/companies/CompanyCreateForm';
import { UserPlus, Building } from 'lucide-react';
import { FormSectionHeader } from '@/components/shared/FormSectionHeader';
import { FieldError } from '@/components/shared/FieldError';
import {
  ASSET_TYPE_OPTIONS,
  ASSET_TYPE_VALUES,
  ASSET_CONDITIONS,
  CURRENCIES,
} from '@/types';

const schema = z.object({
  owner_type: z.enum(['individual', 'company']),
  owner_id: z
    .number({ error: 'Owner is required' })
    .min(1, 'Owner is required'),
  owner_asset_number: z.string().optional(),
  asset_type: z
    .string()
    .min(1, 'Select asset type')
    .refine(
      (v) => (ASSET_TYPE_VALUES as readonly string[]).includes(v),
      'Select asset type',
    ),
  asset_make: z.string().min(1, 'Required'),
  asset_model: z.string().min(1, 'Required'),
  year_of_make: z.coerce.number().min(1900).max(2100),
  condition: z.enum(['new', 'second_hand', 'reconditioned', 'non_functioning']),
  mv_registration_no: z.string().optional(),
  chassis_number: z.string().optional(),
  engine_number: z.string().optional(),
  serial_number: z.string().optional(),
  currency: z.enum(['USD', 'ZWL', 'ZAR', 'GBP', 'EUR']),
  estimated_value: z.coerce.number().min(0),
  location_address: z.string().min(1, 'Required'),
  subscription_start_date: z.string().min(1, 'Required'),
  subscription_end_date: z.string().min(1, 'Required'),
});

type FormValues = z.infer<typeof schema>;

interface AssetRegistryFormProps {
  initial?: Partial<FormValues>;
  ownerDisplayLabel?: string;
  onSuccess: () => void;
  onCancel: () => void;
  isEdit?: boolean;
  recordId?: number;
}

export function AssetRegistryForm({
  initial,
  ownerDisplayLabel,
  onSuccess,
  onCancel,
  isEdit,
  recordId,
}: AssetRegistryFormProps) {
  const [addIndividualOpen, setAddIndividualOpen] = useState(false);
  const [addCompanyOpen, setAddCompanyOpen] = useState(false);

  const {
    register,
    control,
    handleSubmit,
    watch,
    setValue,
    setError,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: 'onSubmit',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      owner_type: 'company',
      currency: 'USD',
      year_of_make: new Date().getFullYear(),
      condition: 'new',
      ...initial,
    },
  });

  const { errors } = useFormState({ control });

  const watchAssetType = watch('asset_type');
  const isVehicle = watchAssetType === 'vehicles';

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (data: FormValues) =>
      isEdit && recordId
        ? assetRegistryApi.updateRecord(recordId, data as any)
        : assetRegistryApi.createRecord(data as any),
    onSuccess,
    onError: (err: unknown) => {
      if (!applyApiValidationErrors(setError, err)) {
        const data = (err as { response?: { data?: { message?: string; error?: string } } })
          ?.response?.data;
        toast.error(
          data?.message ?? data?.error ?? 'Failed to save',
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
    <>
    <form
      onSubmit={handleSubmit((d) => submit(d), onInvalid)}
      className="bg-white"
      noValidate
    >
      <div className="flex gap-2 px-4 pt-4 pb-1">
        <Button
          type="button"
          size="sm"
          variant="primary"
          leftIcon={<UserPlus className="h-3 w-3" />}
          onClick={() => setAddIndividualOpen(true)}
        >
          + Add Individual
        </Button>
        <Button
          type="button"
          size="sm"
          variant="secondary"
          leftIcon={<Building className="h-3 w-3" />}
          onClick={() => setAddCompanyOpen(true)}
        >
          + Add Company
        </Button>
      </div>
      <FormSectionHeader title="Owner Details" variant="teal" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <div>
          <label className="text-xs font-medium text-slate-600">
            Owner Type
          </label>
          <select
            {...register('owner_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            <option value="company">Company</option>
            <option value="individual">Individual</option>
          </select>
        </div>
        <div className="col-span-2">
          <Controller
            name="owner_id"
            control={control}
            render={({ field }) => (
              <AutocompleteInput
                label="Name / ID / Co. Reg #"
                placeholder="Search owner..."
                queryKey={`asset-owner-${watch('owner_type')}`}
                displayLabel={ownerDisplayLabel}
                fetchFn={(q) =>
                  watch('owner_type') === 'company'
                    ? companiesApi.searchBranches(q)
                    : individualsApi.searchIndividuals(q)
                }
                error={errors.owner_id?.message}
                value={field.value}
                onBlur={field.onBlur}
                onChange={(v) => field.onChange(Number(v))}
              />
            )}
          />
        </div>
        <Input
          label="Owner Asset Number"
          {...register('owner_asset_number')}
          placeholder="Internal asset code"
        />
      </div>

      {/* ── Asset Details ── */}
      <FormSectionHeader title="Asset Details" variant="dark" />
      <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
        <div>
          <label className="text-xs font-medium text-slate-600">
            Asset Type<span className="text-red-500 ml-0.5">*</span>
          </label>
          <select
            {...register('asset_type')}
            className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
          >
            <option value="">Select asset type</option>
            {ASSET_TYPE_OPTIONS.map((t) => (
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
          label="Year of Make"
          type="number"
          {...register('year_of_make', { valueAsNumber: true })}
          error={errors.year_of_make?.message}
        />
        <div>
          <label className="text-xs font-medium text-slate-600">
            Condition
          </label>
          <select
            {...register('condition')}
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
          {...register('mv_registration_no')}
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

      {/* ── Valuation & Subscription ── */}
      <FormSectionHeader title="Valuation & Subscription" variant="teal" />
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
          label="Estimated Value"
          type="number"
          step="0.01"
          {...register('estimated_value')}
          error={errors.estimated_value?.message}
          required
        />
        <div className="col-span-2">
          <Input
            label="Location Address"
            {...register('location_address')}
            error={errors.location_address?.message}
            placeholder="Primary location of asset"
            required
          />
        </div>
        <Input
          label="Subscription Start Date"
          type="date"
          {...register('subscription_start_date')}
          error={errors.subscription_start_date?.message}
          required
        />
        <Input
          label="Subscription End Date"
          type="date"
          {...register('subscription_end_date')}
          error={errors.subscription_end_date?.message}
          required
        />
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-4 py-3">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" loading={isPending}>
          {isEdit ? 'Edit' : 'Upload'}
        </Button>
      </div>
    </form>

    <Modal open={addIndividualOpen} onClose={() => setAddIndividualOpen(false)} title="Add Individual" size="lg">
      <IndividualCreateForm
        onCancel={() => setAddIndividualOpen(false)}
        onSuccess={({ id }) => {
          setValue('owner_type', 'individual');
          setValue('owner_id', id, { shouldValidate: true });
          setAddIndividualOpen(false);
        }}
      />
    </Modal>
    <Modal open={addCompanyOpen} onClose={() => setAddCompanyOpen(false)} title="Add Company" size="lg">
      <CompanyCreateForm
        onCancel={() => setAddCompanyOpen(false)}
        onSuccess={({ id }) => {
          setValue('owner_type', 'company');
          setValue('owner_id', id, { shouldValidate: true });
          setAddCompanyOpen(false);
        }}
      />
    </Modal>
    </>
  );
}
