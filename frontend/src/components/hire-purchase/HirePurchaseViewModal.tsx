import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Modal } from '@/components/shared/Modal';
import { HirePurchaseForm } from './HirePurchaseForm';
import type { HirePurchaseRecord } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Edit, CheckCircle } from 'lucide-react';
import { DeleteRecordButton } from '@/components/shared/DeleteRecordButton';
import { hirePurchaseApi } from '@/api/hirePurchaseApi';

interface HirePurchaseViewModalProps {
  record: HirePurchaseRecord;
  onClose: () => void;
  onSaved: () => void;
  onDeleted: () => void;
}

export function HirePurchaseViewModal({
  record,
  onClose,
  onSaved,
  onDeleted,
}: HirePurchaseViewModalProps) {
  const [editMode, setEditMode] = useState(false);
  const [confirmingClosure, setConfirmingClosure] = useState(false);
  const queryClient = useQueryClient();

  const { mutate: confirmClosure, isPending: isConfirming } = useMutation({
    mutationFn: () => hirePurchaseApi.confirmClosure(record.id),
    onSuccess: () => {
      toast.success('Hire purchase closure confirmed');
      queryClient.invalidateQueries({ queryKey: ['hire-purchase-dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['hire-purchase'] });
      setConfirmingClosure(false);
      onSaved();
    },
    onError: (err: any) => {
      toast.error(err?.response?.data?.message ?? 'Failed to confirm closure');
      setConfirmingClosure(false);
    },
  });

  return (
    <Modal
      open
      onClose={onClose}
      title={`Hire Purchase — ${record.agreement_number}`}
      size="xl"
    >
      {editMode ? (
        <HirePurchaseForm
          isEdit
          recordId={record.id}
          financierDisplayLabel={record.financier_name}
          purchaserDisplayLabel={record.purchaser_name}
          initial={{
            financier_id: record.financier_id,
            data_date: record.data_date,
            purchaser_type: record.purchaser_type,
            purchaser_id: record.purchaser_id,
            agreement_number: record.agreement_number,
            asset_type: record.asset_type,
            asset_make: record.asset_make,
            asset_model: record.asset_model,
            asset_year: record.asset_year,
            asset_condition: record.asset_condition,
            reg_serial_number: record.reg_serial_number,
            chassis_number: record.chassis_number,
            engine_number: record.engine_number,
            currency: record.currency,
            purchase_amount: record.purchase_amount,
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
          <div className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
            {[
              ['Financier', record.financier_name],
              ['Purchaser', record.purchaser_name],
              ['Agreement No.', record.agreement_number],
              ['Asset', `${record.asset_make} ${record.asset_model}`],
              ['Asset Type', record.asset_type],
              ['Reg/Serial', record.reg_serial_number],
              ['Currency', record.currency],
              ['Purchase Amount', formatCurrency(record.purchase_amount)],
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
              onDelete={() => hirePurchaseApi.deleteRecord(record.id)}
              onDeleted={onDeleted}
            />
            <div className="flex gap-2 items-center">
              {record.status !== 'closed' && (
                confirmingClosure ? (
                  <>
                    <span className="text-xs text-amber-700">Confirm closure?</span>
                    <Button
                      type="button"
                      size="sm"
                      variant="primary"
                      loading={isConfirming}
                      onClick={() => confirmClosure()}
                    >
                      Yes, Confirm
                    </Button>
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => setConfirmingClosure(false)}
                    >
                      Cancel
                    </Button>
                  </>
                ) : (
                  <Button
                    type="button"
                    size="sm"
                    variant="secondary"
                    leftIcon={<CheckCircle className="h-3.5 w-3.5" />}
                    onClick={() => setConfirmingClosure(true)}
                  >
                    Confirm Closure
                  </Button>
                )
              )}
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
