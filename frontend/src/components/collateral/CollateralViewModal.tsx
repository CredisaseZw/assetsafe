import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Modal } from '@/components/shared/Modal';
import { CollateralForm } from './CollateralForm';
import type { CollateralRecord } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';
import { assetTypeLabel } from '@/lib/assetTypes';
import { Button } from '@/components/ui/button';
import { Edit } from 'lucide-react';
import { DeleteRecordButton } from '@/components/shared/DeleteRecordButton';
import { collateralApi } from '@/api/collateralApi';

interface CollateralViewModalProps {
  record: CollateralRecord;
  onClose: () => void;
  onSaved: () => void;
  onDeleted: () => void;
}

export function CollateralViewModal({
  record,
  onClose,
  onSaved,
  onDeleted,
}: CollateralViewModalProps) {
  const [editMode, setEditMode] = useState(false);

  const { data: detail } = useQuery({
    queryKey: ['collateral-detail', record.id],
    queryFn: () => collateralApi.getRecord(record.id),
    staleTime: 5 * 60 * 1000,
  });

  return (
    <Modal
      open
      onClose={onClose}
      title={`Collateral — ${record.agreement_number}`}
      size="xl"
    >
      {editMode ? (
        detail ? (
          <CollateralForm
            isEdit
            recordId={record.id}
            financierDisplayLabel={detail.financier_name}
            debtorDisplayLabel={detail.debtor_name}
            initial={{
              financier_type: detail.financier_type,
              financier_id: detail.financier_id,
              data_date: detail.data_date,
              debtor_type: detail.debtor_type,
              debtor_id: detail.debtor_id,
              agreement_number: detail.agreement_number,
              asset_type: detail.asset_type,
              asset_make: detail.asset_make,
              asset_model: detail.asset_model,
              asset_year: detail.asset_year,
              asset_condition: detail.asset_condition,
              asset_registration_no: detail.asset_registration_no,
              chassis_number: detail.chassis_number,
              engine_number: detail.engine_number,
              serial_number: detail.serial_number,
              currency: detail.currency,
              loan_amount: detail.loan_amount,
              instalment_amount: detail.instalment_amount,
              instalment_date: detail.instalment_date,
              total_paid_to_date: detail.total_paid_to_date,
              start_date: detail.start_date,
              end_date: detail.end_date,
            }}
            onSuccess={onSaved}
            onCancel={() => setEditMode(false)}
          />
        ) : (
          <div className="flex items-center justify-center p-10 text-sm text-slate-400">
            Loading…
          </div>
        )
      ) : (
        <div className="p-5 space-y-4 bg-white">
          {/* Detail grid */}
          <div className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
            {[
              ['Financier', detail?.financier_name ?? record.financier_name],
              ['Debtor', detail?.debtor_name ?? record.debtor_name],
              ['Agreement No.', record.agreement_number],
              ['Asset', `${detail?.asset_make ?? ''} ${detail?.asset_model ?? ''}`.trim() || record.asset_description],
              ['Asset Type', assetTypeLabel(detail?.asset_type ?? record.asset_type)],
              ['Year', detail?.asset_year ?? record.asset_year],
              ['Condition', detail?.asset_condition ?? record.asset_condition],
              ['Reg/Serial', detail?.serial_number || detail?.asset_registration_no || record.serial_number || record.asset_registration_no],
              ['Currency', detail?.currency ?? record.currency],
              ['Loan Amount', formatCurrency(detail?.loan_amount ?? record.loan_amount)],
              ['Instalment', formatCurrency(detail?.instalment_amount ?? record.instalment_amount)],
              ['Balance', formatCurrency(detail?.balance ?? record.balance)],
              ['Start Date', formatDate(detail?.start_date ?? record.start_date)],
              ['End Date', formatDate(detail?.end_date ?? record.end_date)],
              ['Status', detail?.status ?? record.status],
            ].map(([k, v]) => (
              <div key={String(k)}>
                <dt className="text-xs font-medium uppercase text-slate-400">
                  {k}
                </dt>
                <dd className="mt-0.5 font-medium text-slate-800">
                  {String(v ?? '—')}
                </dd>
              </div>
            ))}
          </div>
          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-100">
            <DeleteRecordButton
              onDelete={() => collateralApi.deleteRecord(record.id)}
              onDeleted={onDeleted}
            />
            <div className="flex gap-2">
              <Button variant="ghost" onClick={onClose}>
                Close
              </Button>
              <Button
                leftIcon={<Edit className="h-3.5 w-3.5" />}
                onClick={() => setEditMode(true)}
              >
                Edit
              </Button>
            </div>
          </div>
        </div>
      )}
    </Modal>
  );
}
