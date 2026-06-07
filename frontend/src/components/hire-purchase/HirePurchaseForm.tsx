import { useEffect, useState } from 'react';
import { useForm, useFormState, Controller } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation, useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';
import { UserPlus, Building } from 'lucide-react';
import { hirePurchaseApi } from '@/api/hirePurchaseApi';
import { clientsApi } from '@/api/clientsApi';
import { Modal } from '@/components/shared/Modal';
import { IndividualCreateForm } from '@/components/individuals/IndividualCreateForm';
import { CompanyCreateForm } from '@/components/companies/CompanyCreateForm';
import { Input } from '@/components/ui/input';
import { DateInput } from '@/components/ui/DateInput';
import AutocompleteInput from '@/components/shared/AutocompleteInput';
import { individualsApi } from '@/api/individualsApi';
import { companiesApi } from '@/api/companiesApi';
import { Button } from '@/components/ui/button';
import { FormSectionHeader } from '@/components/shared/FormSectionHeader';
import { FieldError } from '@/components/shared/FieldError';
import { commonApi } from '@/api/commonApi';
import { queryOptions } from '@/api/queryOptions';

const schema = z.object({
  financier_id: z
    .number({ error: 'Financier is required' })
    .min(1, 'Financier is required'),
  data_date: z.string().min(1, 'Required'),
  purchaser_type: z.string().min(1, 'Purchaser Type is required'),
  purchaser_id: z
    .number({ error: 'Purchaser is required' })
    .min(1, 'Purchaser is required'),
  purchaser_search: z.string().optional(),
  agreement_number: z.string().min(1, 'Required'),
  asset_type: z.string().min(1, 'Select asset type'),
  asset_make: z.string().min(1, 'Required'),
  asset_model: z.string().optional(),
  asset_year: z.coerce.number().min(1900).max(2100),
  asset_condition: z.string().min(1, 'Select condition'),
  reg_serial_number: z.string().optional(),
  chassis_number: z.string().optional(),
  engine_number: z.string().optional(),
  currency: z.string().min(1, 'Currency is required'),
  purchase_amount: z.coerce.number().min(0),
  instalment_amount: z.coerce.number().min(0),
  instalment_date: z.coerce.number().min(1).max(31),
  total_paid_to_date: z.coerce.number().min(0),
  balance: z.coerce.number().min(0),
  start_date: z.string().min(1),
  end_date: z.string().min(1),
});

type FormValues = z.infer<typeof schema>;

interface HirePurchaseFormProps {
  initial?: Partial<FormValues>;
  financierDisplayLabel?: string;
  purchaserDisplayLabel?: string;
  onSuccess: () => void;
  onSaveAndAdd?: () => void;
  onCancel: () => void;
  isEdit?: boolean;
  recordId?: number;
}

export function HirePurchaseForm({
  initial,
  financierDisplayLabel,
  purchaserDisplayLabel,
  onSuccess,
  onSaveAndAdd,
  onCancel,
  isEdit,
  recordId,
}: HirePurchaseFormProps) {
  const [addIndividualOpen, setAddIndividualOpen] = useState(false);
  const [addCompanyOpen, setAddCompanyOpen] = useState(false);
  const { register, control, handleSubmit, watch, reset, setValue, setError } =
    useForm<FormValues>({
      resolver: zodResolver(schema),
      mode: 'onSubmit',
      reValidateMode: 'onChange',
      shouldFocusError: true,
      defaultValues: {
        purchaser_type: 'individual',
        data_date: new Date().toISOString().split('T')[0],
        currency: '',
        asset_year: new Date().getFullYear(),
        asset_condition: 'new',
        total_paid_to_date: 0,
        balance: 0,
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
  const currentPurchaserType = watch('purchaser_type');

  useEffect(() => {
    if (!watch('currency') && currencies.length > 0) {
      setValue('currency', currencies[0].code, { shouldValidate: true });
    }
  }, [currencies, setValue, watch]);

  useEffect(() => {
    if (!watch('asset_condition') && assetConditionOptions.length > 0) {
      setValue('asset_condition', assetConditionOptions[0].value, {
        shouldValidate: true,
      });
    }
  }, [assetConditionOptions, setValue, watch]);

  useEffect(() => {
    if (!currentPurchaserType && partyTypeOptions.length > 0) {
      const defaultPurchaser =
        partyTypeOptions.find((p: any) => p.value === 'individual') ||
        partyTypeOptions[0];
      setValue('purchaser_type', defaultPurchaser.value, {
        shouldValidate: true,
      });
    }
  }, [partyTypeOptions, setValue, currentPurchaserType]);

  const watchAssetType = watch('asset_type');
  const isVehicle = watchAssetType === 'vehicles';

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (data: FormValues) =>
      isEdit && recordId
        ? hirePurchaseApi.updateRecord(recordId, data as any)
        : hirePurchaseApi.createRecord(data as any),
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

  const handleSaveAndAdd = handleSubmit((data) => {
    submit(data, {
      onSuccess: () => {
        reset();
        onSaveAndAdd?.();
      },
    });
  });

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

        {/* ── Financier Section ── */}
        <FormSectionHeader title="Financier" variant="red" />
        <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-3">
          <div className="col-span-2">
            <Controller
              name="financier_id"
              control={control}
              render={({ field }) => (
                <AutocompleteInput
                  label="Financier Name"
                  placeholder="Search financier..."
                  queryKey="hp-financier"
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
          <Controller
            name="data_date"
            control={control}
            render={({ field, fieldState }) => (
              <DateInput
                label="Data Date"
                value={field.value}
                onChange={field.onChange}
                onBlur={field.onBlur}
                error={fieldState.error?.message}
                required
              />
            )}
          />
        </div>

        {/* ── Lessee / Purchaser Section ── */}
        <FormSectionHeader title="Lessee" variant="teal" />
        <div className="p-4 space-y-3">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <div>
              <label className="text-xs font-medium text-slate-600">
                Purchaser Type
              </label>
              <select
                {...register('purchaser_type')}
                className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
                disabled={!partyTypeOptions.length}
              >
                <option value="">
                  {partyTypeOptions.length
                    ? 'Select type...'
                    : 'Loading types...'}
                </option>
                {partyTypeOptions.map((option: any) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Search Purchaser */}
          <div className="rounded border border-slate-200 bg-slate-50 p-3">
            <p className="mb-2 text-xs font-semibold text-slate-600 uppercase">
              Search:{' '}
              {watch('purchaser_type') === 'individual'
                ? 'Individual'
                : 'Company'}
            </p>
            <div className="flex gap-2">
              <Controller
                name="purchaser_id"
                control={control}
                render={({ field }) => (
                  <AutocompleteInput
                    placeholder={
                      watch('purchaser_type') === 'individual'
                        ? 'Search by Name / National ID'
                        : 'Search by Name / Reg Number'
                    }
                    queryKey={`hp-purchaser-${watch('purchaser_type')}`}
                    displayLabel={purchaserDisplayLabel}
                    fetchFn={(q) =>
                      watch('purchaser_type') === 'company'
                        ? companiesApi.searchBranches(q)
                        : individualsApi.searchIndividuals(q)
                    }
                    value={field.value}
                    onBlur={field.onBlur}
                    error={errors.purchaser_id?.message}
                    onChange={(v) => field.onChange(Number(v))}
                  />
                )}
              />
            </div>
          </div>
        </div>

        {/* ── HP Details ── */}
        <FormSectionHeader title="Hire Purchase Details" variant="dark" />
        <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-3">
          <Input
            label="Agreement Number"
            {...register('agreement_number')}
            error={errors.agreement_number?.message}
            required
          />
          <div>
            <label className="text-xs font-medium text-slate-600">
              Asset Type
            </label>
            <select
              {...register('asset_type')}
              className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
              disabled={!assetTypeOptions.length}
            >
              <option value="">
                {assetTypeOptions.length ? 'Click to select...' : 'Loading...'}
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
          <Input label="Model" {...register('asset_model')} />
          <Input label="Year" type="number" {...register('asset_year')} />
          <div>
            <label className="text-xs font-medium text-slate-600">
              Condition
            </label>
            <select
              {...register('asset_condition')}
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
          <Input label="Serial Number" {...register('reg_serial_number')} />
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
            label="Purchase Amount"
            type="number"
            step="0.01"
            {...register('purchase_amount')}
            required
          />
          <Input
            label="Instalment Amount"
            type="number"
            step="0.01"
            {...register('instalment_amount')}
            required
          />
          <Input
            label="Instalment Date (dd)"
            type="number"
            min="1"
            max="31"
            {...register('instalment_date')}
            required
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
          <Controller
            name="start_date"
            control={control}
            render={({ field, fieldState }) => (
              <DateInput
                label="Agreement Start Date"
                value={field.value}
                onChange={field.onChange}
                onBlur={field.onBlur}
                error={fieldState.error?.message}
                required
              />
            )}
          />
          <Controller
            name="end_date"
            control={control}
            render={({ field, fieldState }) => (
              <DateInput
                label="Agreement End Date"
                value={field.value}
                onChange={field.onChange}
                onBlur={field.onBlur}
                error={fieldState.error?.message}
                required
              />
            )}
          />
        </div>

        {/* ── Footer ── */}
        <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50 px-4 py-3">
          {!isEdit && (
            <Button
              type="button"
              variant="primary"
              loading={isPending}
              onClick={handleSaveAndAdd}
            >
              + Save And Add
            </Button>
          )}
          <div className="flex gap-2 ml-auto">
            <Button type="button" variant="ghost" onClick={onCancel}>
              Cancel
            </Button>
            <Button type="submit" variant="secondary" loading={isPending}>
              Save And Exit
            </Button>
          </div>
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
          onSuccess={({ id, name }) => {
            setValue('purchaser_type', 'individual');
            setValue('purchaser_id', id, { shouldValidate: true });
            setAddIndividualOpen(false);
            toast.success(`${name} added — select from search if needed`);
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
          onSuccess={({ id, name }) => {
            setValue('purchaser_type', 'company');
            setValue('purchaser_id', id, { shouldValidate: true });
            setAddCompanyOpen(false);
            toast.success(`${name} added — search branch to link purchaser`);
          }}
        />
      </Modal>
    </>
  );
}
