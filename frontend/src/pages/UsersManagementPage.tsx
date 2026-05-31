import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { toast } from 'sonner';
import { usersApi, type CreateUserPayload } from '@/api/usersApi';
import { TableSkeleton } from '@/components/shared/TableSkeleton';
import { EmptyState } from '@/components/shared/EmptyState';
import { NumberedPaginationFooter } from '@/components/shared/NumberedPaginationFooter';
import { Modal } from '@/components/shared/Modal';
import { Button } from '@/components/ui/button';
import { formatDate } from '@/lib/utils';

const PAGE_SIZE = 16;

export default function UsersManagementPage() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [appliedSearch, setAppliedSearch] = useState('');
  const [createOpen, setCreateOpen] = useState(false);
  const [form, setForm] = useState<CreateUserPayload>({
    email: '',
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    is_staff: false,
    is_superuser: false,
  });
  const [saving, setSaving] = useState(false);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['managed-users', page, appliedSearch],
    queryFn: () =>
      usersApi.list({
        page,
        page_size: PAGE_SIZE,
        ...(appliedSearch ? { search: appliedSearch } : {}),
      }),
  });

  const totalRecords = data?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalRecords / PAGE_SIZE));
  const activePage = Math.min(page, totalPages);
  const rows = data?.results ?? [];
  const startItem = totalRecords === 0 ? 0 : (activePage - 1) * PAGE_SIZE + 1;
  const endItem = Math.min(activePage * PAGE_SIZE, totalRecords);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await usersApi.create({
        ...form,
        email: form.email.trim().toLowerCase(),
        username: form.username.trim() || form.email.split('@')[0],
      });
      toast.success('User created');
      setCreateOpen(false);
      setForm({
        email: '',
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        is_staff: false,
        is_superuser: false,
      });
      queryClient.invalidateQueries({ queryKey: ['managed-users'] });
    } catch {
      toast.error('Could not create user');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900">User management</h1>
          <p className="text-sm text-slate-600">Create and manage system users.</p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="mr-1 h-4 w-4" /> New user
        </Button>
      </div>

      <div className="flex gap-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search username or email"
          className="rounded border border-slate-300 px-3 py-1.5 text-sm"
        />
        <button
          type="button"
          className="rounded bg-[#0f7d8e] px-3 py-1.5 text-sm font-semibold text-white"
          onClick={() => {
            setAppliedSearch(search.trim());
            setPage(1);
          }}
        >
          Search
        </button>
      </div>

      <div className="flex min-h-0 flex-1 flex-col overflow-hidden border border-[#8f8f8f]">
        <div className="min-h-0 flex-1 overflow-auto">
          {isLoading ? (
            <TableSkeleton cols={6} rows={8} />
          ) : isError ? (
            <EmptyState message="Could not load users." />
          ) : rows.length === 0 ? (
            <EmptyState message="No users found." />
          ) : (
            <table className="w-full min-w-[700px] border-collapse text-left text-sm">
              <thead className="sticky top-0 bg-[#e3e0da] text-xs font-bold uppercase">
                <tr>
                  <th className="px-3 py-2">Username</th>
                  <th className="px-3 py-2">Email</th>
                  <th className="px-3 py-2">Type</th>
                  <th className="px-3 py-2">Staff</th>
                  <th className="px-3 py-2">Superuser</th>
                  <th className="px-3 py-2">Joined</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id} className="border-t border-slate-200">
                    <td className="px-3 py-2 font-medium">{row.username}</td>
                    <td className="px-3 py-2">{row.email}</td>
                    <td className="px-3 py-2">{row.user_type}</td>
                    <td className="px-3 py-2">{row.is_staff ? 'Yes' : 'No'}</td>
                    <td className="px-3 py-2">
                      {row.is_superuser ? 'Yes' : 'No'}
                    </td>
                    <td className="px-3 py-2">{formatDate(row.date_joined)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        {totalRecords > 0 ? (
          <NumberedPaginationFooter
            startItem={startItem}
            endItem={endItem}
            totalRecords={totalRecords}
            activePage={activePage}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        ) : null}
      </div>

      <Modal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        title="Create user"
      >
        <form onSubmit={handleCreate} className="space-y-3">
          {(
            [
              ['email', 'Email', 'email'],
              ['username', 'Username', 'text'],
              ['password', 'Password', 'password'],
              ['first_name', 'First name', 'text'],
              ['last_name', 'Last name', 'text'],
            ] as const
          ).map(([key, label, type]) => (
            <div key={key}>
              <label className="text-sm font-semibold">{label}</label>
              <input
                type={type}
                required={key === 'email' || key === 'password'}
                value={form[key] as string}
                onChange={(e) =>
                  setForm((f) => ({ ...f, [key]: e.target.value }))
                }
                className="mt-1 w-full rounded border border-slate-300 px-3 py-2 text-sm"
              />
            </div>
          ))}
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={form.is_staff}
              onChange={(e) =>
                setForm((f) => ({ ...f, is_staff: e.target.checked }))
              }
            />
            Staff (can access asset registry)
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={form.is_superuser}
              onChange={(e) =>
                setForm((f) => ({ ...f, is_superuser: e.target.checked }))
              }
            />
            Superuser (admin tools)
          </label>
          <div className="flex justify-end gap-2 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setCreateOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={saving}>
              {saving ? 'Creating…' : 'Create'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
