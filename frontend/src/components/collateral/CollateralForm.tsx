import { useEffect, useRef, useState } from 'react';
import { useForm, useFormState, Controller } from 'react-hook-form';
import { zodResolver } from '@/lib/zodResolver';
import { applyApiValidationErrors } from '@/lib/formErrors';
import { z } from 'zod';
import { useMutation, useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';
import { UserPlus, Building } from 'lucide-react';
import { collateralApi } from '@/api/collateralApi';
import { individualsApi } from '@/api/individualsApi';
import { companiesApi } from '@/api/companiesApi';
import { Input } from '@/components/ui/input';
import { DateInput } from '@/components/ui/DateInput';
import AutocompleteInput from '@/components/shared/AutocompleteInput';
import { Button } from '@/components/ui/button';
import { FormSectionHeader } from '@/components/shared/FormSectionHeader';
import { FieldError } from '@/components/shared/FieldError';
import { Modal } from '@/components/shared/Modal';
import { IndividualCreateForm } from '@/components/individuals/IndividualCreateForm';
import { CompanyCreateForm } from '@/components/companies/CompanyCreateForm';
import { commonApi } from '@/api/commonApi';
import { queryOptions } from '@/api/queryOptions';

const schema = z.object({
  financier_type: z.string().min(1, 'Financier Type is required'),
  financier_id: z
    .number({ error: 'Financier is required' })
    .min(1, 'Financier is required'),
  data_date: z.string().min(1, 'Required'),
  debtor_type: z.string().min(1, 'Debtor Type is required'),
  debtor_id: z
    .number({ error: 'Debtor is required' })
    .min(1, 'Debtor is required'),
  agreement_number: z.string().min(1, 'Required'),
  asset_type: z.string().min(1, 'Select asset type'),
  asset_make: z.string().min(1, 'Required'),
  asset_model: z.string().min(1, 'Required'),
  asset_year: z.coerce.number().min(1900).max(2100),
  asset_condition: z.string().min(1, 'Select condition'),
  asset_registration_no: z.string().optional(),
  chassis_number: z.string().optional(),
  engine_number: z.string().optional(),
  serial_number: z.string().optional(),
  currency: z.string().min(1, 'Currency is required'),
  loan_amount: z.coerce.number().min(0),
  instalment_amount: z.coerce.number().min(0),
  instalment_date: z.coerce.number().min(1).max(31),
  total_paid_to_date: z.coerce.number().min(0),
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
  /** When true shows "Save & Add Another" instead of "Upload" */
  onSuccessAndAddAnother?: () => void;
  isEdit?: boolean;
  recordId?: number;
}

export function CollateralForm({
  initial,
  financierDisplayLabel,
  debtorDisplayLabel,
  onSuccess,
  onCancel,
  onSuccessAndAddAnother,
  isEdit,
  recordId,
}: CollateralFormProps) {
  const [addIndividualOpen, setAddIndividualOpen] = useState(false);
  const [addCompanyOpen, setAddCompanyOpen] = useState(false);
  const [financierLabel, setFinancierLabel] = useState(
    financierDisplayLabel ?? '',
  );
  const isFirstRender = useRef(true);

  const { register, handleSubmit, control, watch, setError, setValue } =
    useForm<FormValues>({
      resolver: zodResolver(schema),
      mode: 'onSubmit',
      reValidateMode: 'onChange',
      shouldFocusError: true,
      defaultValues: {
        financier_type: 'company',
        debtor_type: 'individual',
        data_date: new Date().toISOString().split('T')[0],
        currency: '',
        asset_year: new Date().getFullYear(),
        total_paid_to_date: 0,
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
  const assetTypeOptions = choices.CollateralAssetType ?? [];
  const assetConditionOptions = choices.AssetCondition ?? [];

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
    if (!watch('financier_type') && partyTypeOptions.length > 0) {
      const defaultFinancier =
        partyTypeOptions.find((p: any) => p.value === 'company') ||
        partyTypeOptions[0];
      setValue('financier_type', defaultFinancier.value, {
        shouldValidate: true,
      });
    }
    if (!watch('debtor_type') && partyTypeOptions.length > 0) {
      const defaultDebtor =
        partyTypeOptions.find((p: any) => p.value === 'individual') ||
        partyTypeOptions[0];
      setValue('debtor_type', defaultDebtor.value, { shouldValidate: true });
    }
  }, [partyTypeOptions, setValue, watch]);

  const watchedFinancierType = watch('financier_type');
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    setValue('financier_id', 0 as unknown as number);
    setFinancierLabel('');
    setAddIndividualOpen(false);
    setAddCompanyOpen(false);
  }, [watchedFinancierType, setValue]);

  const watchedAssetType = watch('asset_type');
  const isVehicle = watchedAssetType === 'vehicles';
  const computedBalance =
    (watch('loan_amount') ?? 0) - (watch('total_paid_to_date') ?? 0);

  const [addAnother, setAddAnother] = useState(false);

  const { mutate: submit, isPending } = useMutation({
    mutationFn: (data: FormValues) =>
      isEdit && recordId
        ? collateralApi.updateRecord(recordId, data as any)
        : collateralApi.createRecord(data as any),
    onSuccess: () => {
      if (addAnother && onSuccessAndAddAnother) {
        onSuccessAndAddAnother();
      } else {
        onSuccess();
      }
    },
    onError: (err: unknown) => {
      setAddAnother(false);
      if (!applyApiValidationErrors(setError, err)) {
        const data = (
          err as { response?: { data?: { message?: string; error?: string } } }
        )?.response?.data;
        toast.error(data?.message ?? data?.error ?? 'Failed to save record');
      } else {
        toast.error('Please fix the highlighted fields');
      }
    },
  });

  const onInvalid = () => {
    setAddAnother(false);
    toast.error('Please fix the highlighted fields');
  };

  return (
    <>
      <form
        onSubmit={handleSubmit((d) => submit(d), onInvalid)}
        className="bg-white"
        noValidate
      >
        {/* ── Add Individual / Company — top-level action buttons ── */}
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
        <FormSectionHeader title="Financier" variant="teal" />
        <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
          <div>
            <label className="text-xs font-medium text-slate-600">
              Financier Type
            </label>
            <select
              {...register('financier_type')}
              className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-sm focus:outline-none focus:border-[#0f7d8e]"
              disabled={!partyTypeOptions.length}
            >
              <option value="">
                {partyTypeOptions.length ? 'Select type...' : 'Loading...'}
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
              name="financier_id"
              control={control}
              render={({ field }) => (
                <AutocompleteInput
                  label="Name / ID / Reg. No."
                  placeholder="Search financier..."
                  queryKey={`collateral-financier-${watch('financier_type')}`}
                  displayLabel={financierLabel}
                  fetchFn={(q) =>
                    watch('financier_type') === 'company'
                      ? companiesApi.searchBranches(q)
                      : individualsApi.searchIndividuals(q)
                  }
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
              disabled={!partyTypeOptions.length}
            >
              <option value="">
                {partyTypeOptions.length ? 'Select type...' : 'Loading...'}
              </option>
              {partyTypeOptions.map((option: any) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
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
              disabled={!currencies.length}
            >
              <option value="">
                {currencies.length ? 'Select currency...' : 'Loading...'}
              </option>
              {currencies.map((currency) => (
                <option key={currency.code} value={currency.code}>
                  {currency.code} - {currency.name}
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
          <div>
            <label className="text-xs font-medium text-slate-600">
              Balance
            </label>
            <div className="mt-1 flex h-8 w-full items-center rounded border border-slate-200 bg-slate-50 px-2 text-sm text-slate-700">
              {computedBalance.toFixed(2)}
            </div>
          </div>
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
          <Button type="button" variant="ghost" onClick={onCancel}>
            {onSuccessAndAddAnother ? 'Done' : 'Cancel'}
          </Button>
          <div className="flex gap-2">
            {onSuccessAndAddAnother && !isEdit && (
              <Button
                type="submit"
                variant="secondary"
                loading={isPending && addAnother}
                disabled={isPending && !addAnother}
                onClick={() => setAddAnother(true)}
              >
                Save & Add Another
              </Button>
            )}
            <Button
              type="submit"
              loading={isPending && !addAnother}
              disabled={isPending && addAnother}
              onClick={() => setAddAnother(false)}
            >
              {isEdit
                ? 'Save Changes'
                : onSuccessAndAddAnother
                  ? 'Save'
                  : 'Upload'}
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
            setValue('financier_type', 'individual');
            setValue('financier_id', id, { shouldValidate: true });
            setFinancierLabel(name);
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
          onSuccess={({ id, name }) => {
            setValue('financier_type', 'company');
            setValue('financier_id', id, { shouldValidate: true });
            setFinancierLabel(name);
            setAddCompanyOpen(false);
          }}
        />
      </Modal>
    </>
  );
}
