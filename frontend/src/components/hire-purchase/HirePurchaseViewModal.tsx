import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Modal } from '@/components/shared/Modal';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { HirePurchaseForm } from './HirePurchaseForm';
import type { HirePurchaseRecord } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';
import { assetTypeLabel } from '@/lib/assetTypes';
import { Button } from '@/components/ui/button';
import { Edit } from 'lucide-react';
import { hirePurchaseApi } from '@/api/hirePurchaseApi';
import { invalidateRegistryQueries } from '@/lib/registryCache';

interface HirePurchaseViewModalProps {
  record: HirePurchaseRecord;
  onClose: () => void;
  onSaved: (id?: number) => void;
}

export function HirePurchaseViewModal({
  record,
  onClose,
  onSaved,
}: HirePurchaseViewModalProps) {
  const [editMode, setEditMode] = useState(false);
  const [confirmingClosure, setConfirmingClosure] = useState(false);
  const queryClient = useQueryClient();

  const { data: detail } = useQuery({
    queryKey: ['hire-purchase-detail', record.id],
    queryFn: () => hirePurchaseApi.getRecord(record.id),
    staleTime: 5 * 60 * 1000,
  });

  const { mutate: confirmClosure, isPending: isConfirming } = useMutation({
    mutationFn: () => hirePurchaseApi.confirmClosure(record.id),
    onSuccess: () => {
      toast.success('Hire purchase closure confirmed');
      queryClient.invalidateQueries({
        queryKey: ['hire-purchase-detail', record.id],
      });
      invalidateRegistryQueries(queryClient, 'hp', record.id);
      setConfirmingClosure(false);
      onSaved(record.id);
    },
    onError: (err: any) => {
      toast.error(err?.response?.data?.message ?? 'Failed to confirm closure');
      setConfirmingClosure(false);
    },
  });

  return (
    <>
      <Modal
        open
        onClose={onClose}
        title={`Hire Purchase — ${record.agreement_number}`}
        size="xl"
      >
        {editMode ? (
          detail ? (
            <HirePurchaseForm
              isEdit
              recordId={record.id}
              financierDisplayLabel={detail.financier_name}
              purchaserDisplayLabel={detail.purchaser_name}
              dataSourceDisplayLabel={detail.data_source_display}
              dataSourcePositionLabel={detail.data_source_position}
              initial={{
                financier_id: detail.financier_id,
                data_date: detail.data_date,
                purchaser_type: detail.purchaser_type,
                purchaser_id: detail.purchaser_id,
                agreement_number: detail.agreement_number,
                asset_type: detail.asset_type,
                asset_category: detail.asset_category,
                asset_make: detail.asset_make,
                asset_model: detail.asset_model,
                asset_year: detail.asset_year,
                asset_condition: detail.asset_condition,
                reg_serial_number: detail.reg_serial_number,
                chassis_number: detail.chassis_number,
                engine_number: detail.engine_number,
                currency: detail.currency,
                purchase_amount: detail.purchase_amount,
                instalment_amount: detail.instalment_amount,
                instalment_date: detail.instalment_date,
                total_paid_to_date: detail.total_paid_to_date,
                balance: detail.balance,
                start_date: detail.start_date,
                end_date: detail.end_date,
              }}
              onSuccess={() => onSaved(record.id)}
              onCancel={() => setEditMode(false)}
              onCloseRecord={() => setConfirmingClosure(true)}
              closurePending={isConfirming}
            />
          ) : (
            <div className="flex items-center justify-center p-10 text-sm text-slate-400">
              Loading...
            </div>
          )
        ) : (
          <div className="p-5 space-y-4 bg-white">
            <div className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
              {[
                ['Financier', detail?.financier_name ?? record.financier_name],
                ['Purchaser', detail?.purchaser_name ?? record.purchaser_name],
                ['Agreement No.', record.agreement_number],
                [
                  'Asset',
                  `${detail?.asset_make ?? ''} ${detail?.asset_model ?? ''}`.trim() ||
                    record.asset_description,
                ],
                [
                  'Asset Category',
                  assetTypeLabel(
                    detail?.asset_category ?? record.asset_category,
                  ),
                ],
                [
                  'Asset Type',
                  detail?.asset_type || record.asset_type || '—',
                ],
                [
                  'Reg/Serial',
                  detail?.reg_serial_number || record.reg_serial_number,
                ],
                ['Currency', detail?.currency ?? record.currency],
                [
                  'Purchase Amount',
                  formatCurrency(
                    detail?.purchase_amount ?? record.purchase_amount,
                  ),
                ],
                [
                  'Instalment',
                  formatCurrency(
                    detail?.instalment_amount ?? record.instalment_amount,
                  ),
                ],
                ['Balance', formatCurrency(detail?.balance ?? record.balance)],
                [
                  'Start Date',
                  formatDate(detail?.start_date ?? record.start_date),
                ],
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
            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <Button
                leftIcon={<Edit className="h-3.5 w-3.5" />}
                onClick={() => setEditMode(true)}
              >
                Edit
              </Button>
            </div>
          </div>
        )}
      </Modal>

      <ConfirmDialog
        open={confirmingClosure}
        title="Close Hire Purchase Agreement"
        message="Are you sure you want to close this hire purchase agreement?"
        confirmLabel="Yes, Confirm"
        variant="danger"
        loading={isConfirming}
        onConfirm={() => confirmClosure()}
        onCancel={() => setConfirmingClosure(false)}
      />
    </>
  );
}
