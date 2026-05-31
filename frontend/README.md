# AssetSafe Frontend

React + Vite dashboard for the AssetSafe registries (Asset, Collateral, Hire Purchase). This document describes **recent UI and integration work** on this codebase: layout, pagination, CRUD, search, validation, and API alignment with the Django backend.

---

## Quick start

```bash
cd frontend
npm install
npm run dev      # development server
npm run build    # production build
npm run preview  # preview production build
```

Set the API base URL (defaults to `http://localhost:8000/api`):

```bash
# .env or .env.local
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Routes

| Path | Page |
|------|------|
| `/login` | Login |
| `/collateral` | Collateral registry (default after login) |
| `/hire-purchase` | Hire purchase registry |
| `/registry` | Asset registry |

All registry routes use the shared layout in `src/layouts/Dashboard.tsx` (sidebar + top bar + tab nav).

---

## Summary of changes

| Area | What changed |
|------|----------------|
| **Layout** | Stats and search bars are compact; tables use most of the viewport (`PAGE_SIZE = 16`). |
| **Pagination** | Server-side pagination with numbered pages (Prev, `1 … 5 … 10`, Next). |
| **Profile** | User icon in the header shows name, email, and Logout (removed from sidebar footer). |
| **Create / update** | Forms map UI fields to backend field names so POST/PATCH succeed. |
| **Delete** | View modals include Delete with confirmation on all three registries. |
| **Search (lists)** | List pages use backend `search` / `financier` filters; page resets after create. |
| **Search (forms)** | Owner/debtor/financier fields call dedicated backend search APIs via autocomplete. |
| **Validation** | Custom Zod 4 resolver; errors show on fields (no summary block at top of forms). |
| **Party forms** | Modals to create individuals and companies from registry forms. |
| **Cache** | Central `invalidateRegistryQueries()` after mutations; logout still clears all queries. |

---

## 1. Dashboard layout (more space for tables)

**Before:** Large stat cards and tall search rows sat above the table, leaving little room for rows.

**After:**

- Stats moved into a **single inline bar** inside each registry card (`InlineStat`).
- Search/toolbar uses smaller controls (`h-7`, `py-2`).
- Main content padding reduced in `Dashboard.tsx`.
- Each registry page is a full-height flex column; the table body scrolls inside the card.

**Files:** `src/pages/AssetRegistryPage.tsx`, `CollateralPage.tsx`, `HirePurchasePage.tsx`, `src/components/shared/InlineStat.tsx`, `src/layouts/Dashboard.tsx`

---

## 2. Server pagination (numbered)

All three registries load paged data from the backend (`page`, `page_size`) and render:

- “Showing X to Y of Z entries”
- **Prev** / numbered page buttons with ellipsis / **Next**

```
┌─────────────────────────────────────────────────────────┐
│ Showing 1 to 16 of 142 entries    [Prev] 1 2 3 … 9 [Next] │
└─────────────────────────────────────────────────────────┘
```

**Shared pieces:**

| File | Role |
|------|------|
| `src/lib/pagination.ts` | `buildPaginationItems()` — window + ellipsis logic |
| `src/components/ui/pagination.tsx` | shadcn-style pagination primitives |
| `src/components/shared/NumberedPaginationFooter.tsx` | Footer wired on all registry pages |

**Example (records query):**

```tsx
useQuery({
  queryKey: ['registry-records', filterAssetType, appliedSearch, currentPage],
  queryFn: () =>
    assetRegistryApi.getRecords({
      page: currentPage,
      page_size: 16,
      ...(appliedSearch ? { search: appliedSearch } : {}),
      ...(filterAssetType ? { asset_type: filterAssetType } : {}),
    }),
});
```

After **create**, filters are cleared and `currentPage` is reset to `1` so new rows are visible.

---

## 3. User profile menu (navbar)

**Before:** Logout only in the sidebar footer.

**After:** Top-right **user icon** opens a dropdown with display name, email, and **Logout**.

**File:** `src/components/layout/UserProfileMenu.tsx` (used in `src/layouts/Dashboard.tsx`)

Logout still uses `useAuth().logout()`, which clears the TanStack Query cache.

---

## 4. CRUD: create, edit, delete

### Create / update

Forms used to POST UI-shaped payloads (`owner_id`, `asset_make`, …). The backend expects Django-style names (`individual_owner`, `make`, `financier`, …).

**Mapping layer:** `src/lib/registryPayloads.ts`

| Form helper | Used by |
|-------------|---------|
| `mapAssetFormToApi()` | Asset registry |
| `mapCollateralFormToApi()` | Collateral |
| `mapHirePurchaseFormToApi()` | Hire purchase |

API modules call these in `createRecord` / `updateRecord`:

```ts
// src/api/assetRegistryApi.ts (pattern repeated in collateral + hire purchase)
createRecord: async (payload) => {
  const { data } = await axiosInstance.post(
    '/asset-management/',
    mapAssetFormToApi(payload as Record<string, unknown>),
  );
  // ...
},
```

### Delete

View modals include **Delete** with a two-step confirm:

**Component:** `src/components/shared/DeleteRecordButton.tsx`

**API methods:** `deleteRecord(id)` on `assetRegistryApi`, `collateralApi`, `hirePurchaseApi`.

### Party creation (individual / company)

From **Asset** and **Hire Purchase** forms:

- **+ Add Individual** → `IndividualCreateForm` → `POST /api/individuals/`
- **+ Add Company** → `CompanyCreateForm` → `POST /api/companies/` (returns HQ branch id)

**Files:** `src/components/individuals/IndividualCreateForm.tsx`, `src/components/companies/CompanyCreateForm.tsx`

---

## 5. Asset types (frontend ↔ backend)

Backend uses slug values (`vehicles`, `computers`, …). The UI previously used labels (`Vehicles`, `Computers`), which broke filters and creates.

**Central mapping:** `src/lib/assetTypes.ts`

```ts
export const ASSET_TYPE_OPTIONS = [
  { value: 'vehicles', label: 'Vehicles' },
  { value: 'computers', label: 'Computers' },
  // ...
];

export function toBackendAssetType(value: string): string {
  // maps legacy labels → slugs
}
```

Forms use `ASSET_TYPE_OPTIONS` for `<select>` values; list APIs pass `toBackendAssetType()` when filtering.

---

## 6. Autocomplete search (add / edit forms)

Owner, debtor, and financier fields search the **backend search APIs**, not a generic `/users/search/` stub.

| Entity | Endpoint | Query param |
|--------|----------|-------------|
| Individual | `GET /api/individuals/search/` | `search` or `q` |
| Company branch | `GET /api/companies/branches/search/` | `q` |
| Client (financier) | `GET /api/clients/search/` | `q` |

**Flow:**

```
User types (≥2 chars)
    → useAutocomplete debounces 300ms
    → individualsApi.searchIndividuals / companiesApi.searchBranches / clientsApi.searchClients
    → unwrapSearchList() normalizes array | { data } | { results }
    → map*SearchResult() → { id, name, subtitle }
    → dropdown in AutocompleteInput
```

**Key files:**

| File | Role |
|------|------|
| `src/hooks/useAutocomplete.ts` | Debounced React Query; min 2 characters |
| `src/components/shared/AutocompleteInput.tsx` | Dropdown UI; `onMouseDown` so selection works on blur |
| `src/lib/searchResults.ts` | `SearchOption`, unwrap + map helpers |
| `src/api/individualsApi.ts` | `searchIndividuals()` |
| `src/api/companiesApi.ts` | `searchBranches()` |
| `src/api/clientsApi.ts` | `searchClients()` |

**Backend note (individuals):** `apps/individuals/api/views.py` was updated to accept `q` or `search`, use `IndividualSearchSerializer`, and cap results (25) on the `search` action.

---

## 7. Form validation (Zod 4)

The project uses **Zod 4** (`zod@^4`). `@hookform/resolvers@3` only reads `error.errors` (Zod 3). Validation failed silently and errors did not appear on fields.

**Fix:** custom resolver in `src/lib/zodResolver.ts` that reads `error.issues` and returns react-hook-form field errors.

```tsx
import { zodResolver } from '@/lib/zodResolver';
import { useFormState } from 'react-hook-form';

const { control, handleSubmit, setError } = useForm({ resolver: zodResolver(schema) });
const { errors } = useFormState({ control }); // ensures re-render when errors change
```

**Server errors:** `applyApiValidationErrors(setError, err)` in `src/lib/formErrors.ts` maps DRF field names to form fields (e.g. `individual_owner` → `owner_id`).

**Removed:** top-of-form error summary list (`FormErrorSummary` was removed per product preference). Errors remain **per field** via `Input` `error` prop and `FieldError` on selects.

---

## 8. Cache invalidation (multi-user / after mutations)

**File:** `src/lib/registryCache.ts`

```ts
export function invalidateRegistryQueries(
  queryClient: QueryClient,
  scope: 'asset' | 'collateral' | 'hp',
) {
  // invalidates dashboard + records keys with refetchType: 'active'
}
```

Registry pages call this after create, update, or delete instead of ad-hoc `invalidateQueries` strings. Logout still runs `queryClient.clear()` in `useAuth`.

---

## 9. List-page search behaviour

| Page | Search behaviour |
|------|------------------|
| **Asset** | Asset type filter + text `search` param |
| **Collateral** | Text search → `?search=` (DRF searches all configured fields) |
| **Hire purchase** | Financier search via `clientsApi` → list filter `financier=<id>` |

On successful **create**, list filters are cleared and page is set to **1** so the new record is not hidden behind an old filter or page number.

---

## New files

```
src/lib/assetTypes.ts
src/lib/formErrors.ts
src/lib/pagination.ts
src/lib/registryCache.ts
src/lib/registryPayloads.ts
src/lib/searchResults.ts
src/lib/zodResolver.ts
src/api/locationsApi.ts
src/components/companies/CompanyCreateForm.tsx
src/components/individuals/IndividualCreateForm.tsx
src/components/layout/UserProfileMenu.tsx
src/components/shared/DeleteRecordButton.tsx
src/components/shared/FieldError.tsx
src/components/shared/InlineStat.tsx
src/components/shared/NumberedPaginationFooter.tsx
src/components/ui/pagination.tsx
```

---

## Modified files (main)

```
src/layouts/Dashboard.tsx
src/components/app-sidebar.tsx
src/pages/AssetRegistryPage.tsx
src/pages/CollateralPage.tsx
src/pages/HirePurchasePage.tsx
src/api/assetRegistryApi.ts
src/api/collateralApi.ts
src/api/hirePurchaseApi.ts
src/api/individualsApi.ts
src/api/companiesApi.ts
src/api/clientsApi.ts
src/types/index.ts
src/components/registry/AssetRegistryForm.tsx
src/components/registry/AssetViewModal.tsx
src/components/collateral/CollateralForm.tsx
src/components/collateral/CollateralViewModal.tsx
src/components/hire-purchase/HirePurchaseForm.tsx
src/components/hire-purchase/HirePurchaseViewModal.tsx
src/components/shared/AutocompleteInput.tsx
src/hooks/useAutocomplete.ts
src/pages/LoginPage.tsx
```

---

## Project structure (relevant parts)

```
frontend/
├── README.md                 ← this file
├── package.json
├── vite.config.ts
└── src/
    ├── api/                  # Axios clients + DRF response normalization
    ├── components/
    │   ├── registry/         # Asset forms + view modal
    │   ├── collateral/
    │   ├── hire-purchase/
    │   ├── individuals/
    │   ├── companies/
    │   ├── layout/           # UserProfileMenu
    │   └── shared/           # Modal, Autocomplete, pagination footer, etc.
    ├── hooks/                # useAuth, useAutocomplete, …
    ├── layouts/              # Dashboard shell
    ├── lib/                  # Payload mappers, Zod resolver, pagination, cache
    ├── pages/                # Registry list pages
    ├── routes/
    └── types/
```

---

## Testing checklist

After pulling these changes, verify:

1. **Login** → redirect to collateral; profile menu shows user and logout works.
2. **Each registry** → table fills most of the screen; pagination changes pages via API.
3. **Add record** → required field errors appear on inputs when Upload/Save with empty form.
4. **Add record** → valid submit creates row; list refreshes on page 1 without stale search hiding the row.
5. **Autocomplete** → type 2+ characters for owner/debtor/financier; results from API; select fills the field.
6. **View → Edit → Save** and **View → Delete** on all three registries.
7. **Add Individual / Add Company** from asset or HP form (where buttons exist).

---

## Related backend change

Individuals search (`apps/individuals/api/views.py`):

- Accepts `q` or `search` query parameter.
- Uses `IndividualSearchSerializer` for the search action.
- Returns at most 25 matches when a term is provided.

No other backend changes are required for the frontend features above if your API already exposes standard CRUD and the search routes listed in section 6.

---

## Further reading

- `src/api/CACHE_STRATEGY_GUIDE.md` — TanStack Query patterns (optional; registry pages use `registryCache.ts` directly).
- Django REST pagination: list endpoints return `{ count, results }` (sometimes wrapped in `data` by custom renderers).
