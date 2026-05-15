/**
 * Example: How to use preset cache strategies
 *
 * Before (default 5-min cache):
 * const { data } = useQuery({
 *   queryKey: ['collateral-stats'],
 *   queryFn: fetchCollateralStats,
 * });
 *
 * After (15-min cache for dashboard data):
 * const { data } = useQuery({
 *   queryKey: ['collateral-stats'],
 *   queryFn: fetchCollateralStats,
 *   ...queryOptions.dashboard,  // ← Add this for dashboard data
 * });
 *
 * ─────────────────────────────────────────────────────────────
 *
 * Cache Strategy Guide:
 *
 * dashboard  - Summary pages, stats, overview data
 *              Cache: 15 min fresh, keep 1 hour in memory
 *              Use for: Main dashboard, summary views
 *
 * lists      - Record lists, paginated data
 *              Cache: 10 min fresh, keep 45 min in memory
 *              Use for: Collateral records, assets list, hire purchase list
 *
 * details    - Individual record details (DEFAULT)
 *              Cache: 5 min fresh, keep 30 min in memory
 *              Use for: Single asset detail, collateral detail page
 *
 * realtime   - Frequently changing data, live counters
 *              Cache: 30 sec fresh, keep 5 min in memory
 *              Use for: Active trades, real-time notifications, status updates
 *
 * static     - Lookup tables, enums, rarely change data
 *              Cache: 1 hour fresh, keep 24 hours in memory
 *              Use for: Asset types, status options, configurations
 *
 * ─────────────────────────────────────────────────────────────
 *
 * Apply to your pages:
 *
 * import { queryOptions } from '@/api/queryOptions';
 *
 * export function CollateralPage() {
 *   // Dashboard stats: rarely change, use longer cache
 *   const { data: statsData } = useQuery({
 *     queryKey: ['collateral-stats'],
 *     queryFn: fetchStats,
 *     ...queryOptions.dashboard,
 *   });
 *
 *   // List of records: moderate cache
 *   const { data: recordsData } = useQuery({
 *     queryKey: ['collateral-records', page, limit],
 *     queryFn: () => fetchRecords(page, limit),
 *     ...queryOptions.lists,
 *   });
 *
 *   // Asset type options: static data, very long cache
 *   const { data: assetTypes } = useQuery({
 *     queryKey: ['asset-types'],\n *     queryFn: fetchAssetTypes,\n *     ...queryOptions.static,\n *   });\n *\n *   return (...)\n * }\n */\n"
