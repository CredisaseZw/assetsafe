import { useEffect, useState } from 'react';
import { useForm, useFormState, Controller } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation, useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';
import { assetRegistryApi } from '@/api/assetRegistryApi';
import { Input } from '@/components/ui/input';
import { DateInput } from '@/components/ui/DateInput';
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
import { commonApi } from '@/api/commonApi';
import { queryOptions } from '@/api/queryOptions';

const schema = z.object({
  owner_type: z.string().min(1, 'Owner Type is required'),
  owner_id: z
    .number({ error: 'Owner is required' })
    .min(1, 'Owner is required'),
  owner_asset_number: z.string().optional(),
  asset_type: z.string().min(1, 'Select asset type'),
  asset_make: z.string().min(1, 'Required'),
  asset_model: z.string().min(1, 'Required'),
  year_of_make: z.coerce.number().min(1900).max(2100),
  condition: z.string().min(1, 'Select condition'),
  mv_registration_no: z.string().optional(),
  chassis_number: z.string().optional(),
  engine_number: z.string().optional(),
  serial_number: z.string().optional(),
  currency: z.string().min(1, 'Currency is required'),
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

  const { register, control, handleSubmit, watch, setValue, setError } =
    useForm<FormValues>({
      resolver: zodResolver(schema),
      mode: 'onSubmit',
      reValidateMode: 'onChange',
      shouldFocusError: true,
      defaultValues: {
        owner_type: 'company',
        currency: '',
        year_of_make: new Date().getFullYear(),
        condition: 'new',
        ...initial,
      },
    });

  const { errors } = useFormState({ control });
  const { data: currencies = [] } = useQuery({
    queryKey: ['common-currencies'],
    queryFn: commonApi.getCurrencies,
    ...queryOptions.static,
  });
  const { data: choices = {} } = useQuery({
    queryKey: ['common-choices'],
    queryFn: commonApi.getChoices,
    ...queryOptions.static,
  });

  const partyTypeOptions = choices.PartyType ?? [];
  const assetTypeOptions = choices.BaseAssetType ?? [];
  const assetConditionOptions = choices.AssetCondition ?? [];
  const currentOwnerType = watch('owner_type');

  useEffect(() => {
    if (!watch('currency') && currencies.length > 0) {
      setValue('currency', currencies[0].code, { shouldValidate: true });
    }
  }, [currencies, setValue, watch]);

  useEffect(() => {
    if (!watch('condition') && assetConditionOptions.length > 0) {
      setValue('condition', assetConditionOptions[0].value, {
        shouldValidate: true,
      });
    }
  }, [assetConditionOptions, setValue, watch]);

  useEffect(() => {
    if (!currentOwnerType && partyTypeOptions.length > 0) {
      const defaultOwner =
        partyTypeOptions.find((p: any) => p.value === 'company') ||
        partyTypeOptions[0];
      setValue('owner_type', defaultOwner.value, { shouldValidate: true });
    }
  }, [partyTypeOptions, setValue, currentOwnerType]);

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
        const data = (
          err as { response?: { data?: { message?: string; error?: string } } }
        )?.response?.data;
        toast.error(data?.message ?? data?.error ?? 'Failed to save');
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
              disabled={!partyTypeOptions.length}
            >
              <option value="">
                {partyTypeOptions.length
                  ? 'Select owner type...'
                  : 'Loading owner types...'}
              </option>
              {partyTypeOptions.map((option: any) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
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
              disabled={!assetTypeOptions.length}
            >
              <option value="">
                {assetTypeOptions.length ? 'Select asset type' : 'Loading...'}
              </option>
              {assetTypeOptions.map((t: any) => (
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
              disabled={!assetConditionOptions.length}
            >
              <option value="">
                {assetConditionOptions.length ? 'Select...' : 'Loading...'}
              </option>
              {assetConditionOptions.map((c: any) => (
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
              disabled={!currencies.length}
            >
              <option value="">
                {currencies.length
                  ? 'Select currency...'
                  : 'Loading currencies...'}
              </option>
              {currencies.map((currency) => (
                <option key={currency.code} value={currency.code}>
                  {currency.code} - {currency.name}
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
          <Controller
            name="subscription_start_date"
            control={control}
            render={({ field, fieldState }) => (
              <DateInput
                label="Subscription Start Date"
                value={field.value}
                onChange={field.onChange}
                onBlur={field.onBlur}
                error={fieldState.error?.message}
                required
              />
            )}
          />
          <Controller
            name="subscription_end_date"
            control={control}
            render={({ field, fieldState }) => (
              <DateInput
                label="Subscription End Date"
                value={field.value}
                onChange={field.onChange}
                onBlur={field.onBlur}
                error={fieldState.error?.message}
                required
              />
            )}
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

      <Modal
        open={addIndividualOpen}
        onClose={() => setAddIndividualOpen(false)}
        title="Add Individual"
        size="lg"
      >
        <IndividualCreateForm
          onCancel={() => setAddIndividualOpen(false)}
          onSuccess={({ id }) => {
            setValue('owner_type', 'individual');
            setValue('owner_id', id, { shouldValidate: true });
            setAddIndividualOpen(false);
          }}
        />
      </Modal>
      <Modal
        open={addCompanyOpen}
        onClose={() => setAddCompanyOpen(false)}
        title="Add Company"
        size="lg"
        disableBackdropClose
      >
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
