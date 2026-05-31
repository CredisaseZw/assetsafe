import { useState } from 'react';
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

  return (
    <Modal
      open
      onClose={onClose}
      title={`Collateral — ${record.agreement_number}`}
      size="xl"
    >
      {editMode ? (
        <CollateralForm
          isEdit
          recordId={record.id}
          financierDisplayLabel={record.financier_name}
          debtorDisplayLabel={record.debtor_name}
          initial={{
            financier_type: record.financier_type,
            financier_id: record.financier_id,
            data_source_name: record.data_source_name,
            data_source_position: record.data_source_position,
            data_date: record.data_date,
            debtor_type: record.debtor_type,
            debtor_id: record.debtor_id,
            agreement_number: record.agreement_number,
            asset_type: record.asset_type,
            asset_make: record.asset_make,
            asset_model: record.asset_model,
            asset_year: record.asset_year,
            asset_condition: record.asset_condition,
            asset_registration_no: record.asset_registration_no,
            chassis_number: record.chassis_number,
            engine_number: record.engine_number,
            serial_number: record.serial_number,
            currency: record.currency,
            loan_amount: record.loan_amount,
            instalment_amount: record.instalment_amount,
            instalment_date: record.instalment_date,
            total_paid_to_date: record.total_paid_to_date,
            balance: record.balance,
            start_date: record.start_date,
            end_date: record.end_date,
          }}
          onSuccess={onSaved}
          onCancel={() => setEditMode(false)}
        />
      ) : (
        <div className="p-5 space-y-4 bg-white">
          {/* Detail grid */}
          <div className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
            {[
              ['Financier', record.financier_name],
              ['Debtor', record.debtor_name],
              ['Agreement No.', record.agreement_number],
              ['Asset', `${record.asset_make} ${record.asset_model}`],
              ['Asset Type', assetTypeLabel(record.asset_type)],
              ['Year', record.asset_year],
              ['Condition', record.asset_condition],
              [
                'Reg/Serial',
                record.serial_number || record.asset_registration_no,
              ],
              ['Currency', record.currency],
              ['Loan Amount', formatCurrency(record.loan_amount)],
              ['Instalment', formatCurrency(record.instalment_amount)],
              ['Balance', formatCurrency(record.balance)],
              ['Start Date', formatDate(record.start_date)],
              ['End Date', formatDate(record.end_date)],
              ['Status', record.status],
            ].map(([k, v]) => (
              <div key={String(k)}>
                <dt className="text-xs font-medium uppercase text-slate-400">
                  {k}
                </dt>
                <dd className="mt-0.5 font-medium text-slate-800">
                  {String(v)}
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
