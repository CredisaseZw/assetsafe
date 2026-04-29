import { useState } from 'react'
import { Modal } from '@/components/shared/Modal'
import { AssetRegistryForm } from './AssetRegistryForm'
import type { AssetRecord } from '@/types'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { Edit } from 'lucide-react'

interface AssetViewModalProps {
  record: AssetRecord
  onClose: () => void
  onSaved: () => void
}

export function AssetViewModal({ record, onClose, onSaved }: AssetViewModalProps) {
  const [editMode, setEditMode] = useState(false)

  return (
    <Modal open onClose={onClose} title={`Asset — ${record.registration_number}`} size="xl">
      {editMode ? (
        <AssetRegistryForm
          isEdit
          recordId={record.id}
          initial={{
            owner_type: record.owner_type,
            owner_id: record.owner_id,
            owner_asset_number: record.owner_asset_number,
            asset_type: record.asset_type,
            asset_make: record.asset_make,
            asset_model: record.asset_model,
            year_of_make: record.year_of_make,
            condition: record.condition,
            mv_registration_no: record.mv_registration_no,
            chassis_number: record.chassis_number,
            engine_number: record.engine_number,
            serial_number: record.serial_number,
            currency: record.currency,
            estimated_value: record.estimated_value,
            location_address: record.location_address,
            subscription_start_date: record.subscription_start_date,
            subscription_end_date: record.subscription_end_date,
          }}
          onSuccess={onSaved}
          onCancel={() => setEditMode(false)}
        />
      ) : (
        <div className="p-5 space-y-4 bg-white">
          <div className="grid grid-cols-2 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
            {[
              ['Registry No.', record.registration_number],
              ['Owner', record.owner_name],
              ['Asset', `${record.asset_make} ${record.asset_model}`],
              ['Asset Type', record.asset_type],
              ['Year', record.year_of_make],
              ['Condition', record.condition],
              ['Reg/Serial', record.serial_number || record.mv_registration_no],
              ['Currency', record.currency],
              ['Est. Value', formatCurrency(record.estimated_value)],
              ['Location', record.location_address],
              ['Sub. Start', formatDate(record.subscription_start_date)],
              ['Sub. End', formatDate(record.subscription_end_date)],
            ].map(([k, v]) => (
              <div key={String(k)}>
                <dt className="text-xs font-medium uppercase text-slate-400">{k}</dt>
                <dd className="mt-0.5 font-medium text-slate-800">{String(v)}</dd>
              </div>
            ))}
          </div>
          <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
            <Button variant="ghost" onClick={onClose}>Close</Button>
            <Button leftIcon={<Edit className="h-3.5 w-3.5" />} onClick={() => setEditMode(true)}>Edit</Button>
          </div>
        </div>
      )}
    </Modal>
  )
}
