import { toBackendAssetType } from '@/lib/assetTypes';

type OwnerPayload = {
  owner_type: 'individual' | 'company';
  owner_id: number;
};

export function mapAssetFormToApi(data: Record<string, unknown>) {
  const owner = data as OwnerPayload & Record<string, unknown>;
  const asset_category = toBackendAssetType(String(data.asset_category ?? ''));
  const isVehicle = asset_category === 'vehicles';

  const payload: Record<string, unknown> = {
    owner_type: owner.owner_type,
    asset_category,
    asset_type: String(data.asset_type ?? '').trim(),
    make: data.asset_make,
    model: data.asset_model,
    year_of_make: data.year_of_make,
    condition: data.condition,
    currency: data.currency,
    estimated_value: data.estimated_value,
    location_address: data.location_address,
    subscription_start_date: data.subscription_start_date,
    subscription_end_date: data.subscription_end_date,
    owner_asset_number: data.owner_asset_number ?? '',
    serial_number: data.serial_number ?? '',
    mv_registration_number: isVehicle ? (data.mv_registration_no ?? '') : '',
    chassis_number: isVehicle ? (data.chassis_number ?? '') : '',
    engine_number: isVehicle ? (data.engine_number ?? '') : '',
    custody_type: data.custody_type ?? '',
    custodian_type: data.custodian_type ?? '',
    custodian_address: data.custodian_address ?? '',
    custodian_email: data.custodian_email ?? '',
    custodian_mobile: data.custodian_mobile ?? '',
    custodian_telephone: data.custodian_telephone ?? '',
    guarantor_name: data.guarantor_name ?? '',
    guarantor_identification: data.guarantor_identification ?? '',
  };

  if (owner.owner_type === 'individual') {
    payload.individual_owner = owner.owner_id;
    payload.company_owner = null;
  } else {
    payload.company_owner = owner.owner_id;
    payload.individual_owner = null;
  }

  const custodyType = String(data.custody_type ?? '');
  if (custodyType) {
    const custodianType = data.custodian_type as 'individual' | 'company';
    if (custodianType === 'individual') {
      payload.individual_custodian = data.custodian_id;
      payload.company_custodian = null;
    } else {
      payload.company_custodian = data.custodian_id;
      payload.individual_custodian = null;
    }
  } else {
    payload.individual_custodian = null;
    payload.company_custodian = null;
    payload.custodian_type = '';
  }

  return payload;
}

export function mapCollateralFormToApi(data: Record<string, unknown>) {
  const asset_category = toBackendAssetType(String(data.asset_category ?? ''));
  const isVehicle = asset_category === 'vehicles';
  const debtor_type = data.debtor_type as 'individual' | 'company';

  return {
    financier: data.financier_id,
    data_date: data.data_date,
    debtor_type,
    individual_debtor: debtor_type === 'individual' ? data.debtor_id : null,
    company_debtor: debtor_type === 'company' ? data.debtor_id : null,
    agreement_number: data.agreement_number,
    asset_category,
    asset_type: String(data.asset_type ?? '').trim(),
    make: data.asset_make,
    model: data.asset_model,
    year_of_make: data.asset_year,
    condition: data.asset_condition,
    asset_registration_number: isVehicle
      ? (data.asset_registration_no ?? '')
      : '',
    chassis_number: isVehicle ? (data.chassis_number ?? '') : '',
    engine_number: isVehicle ? (data.engine_number ?? '') : '',
    serial_number: data.serial_number ?? '',
    currency: data.currency,
    total_debt: data.loan_amount,
    instalment_amount: data.instalment_amount,
    instalment_day: data.instalment_date,
    total_paid_to_date: data.total_paid_to_date,
    agreement_start_date: data.start_date,
    agreement_end_date: data.end_date,
  };
}

export function mapHirePurchaseFormToApi(data: Record<string, unknown>) {
  const asset_category = toBackendAssetType(String(data.asset_category ?? ''));
  const purchaser_type = data.purchaser_type as 'individual' | 'company';
  const isVehicle = asset_category === 'vehicles';

  return {
    financier: data.financier_id,
    data_date: data.data_date,
    purchaser_type,
    purchaser_individual:
      purchaser_type === 'individual' ? data.purchaser_id : null,
    purchaser_company: purchaser_type === 'company' ? data.purchaser_id : null,
    agreement_number: data.agreement_number,
    asset_category,
    asset_type: String(data.asset_type ?? '').trim(),
    make: data.asset_make,
    model: data.asset_model ?? '',
    year_of_make: data.asset_year,
    condition: data.asset_condition,
    serial_number: data.reg_serial_number ?? '',
    mv_registration_number: isVehicle ? (data.reg_serial_number ?? '') : '',
    chassis_number: isVehicle ? (data.chassis_number ?? '') : '',
    engine_number: isVehicle ? (data.engine_number ?? '') : '',
    currency: data.currency,
    purchase_amount: data.purchase_amount,
    instalment_amount: data.instalment_amount,
    instalment_day: data.instalment_date,
    total_paid_to_date: data.total_paid_to_date,
    balance: data.balance,
    agreement_start_date: data.start_date,
    agreement_end_date: data.end_date,
    ...(data.data_source_user_id
      ? { data_source_user_id: data.data_source_user_id }
      : {}),
  };
}
