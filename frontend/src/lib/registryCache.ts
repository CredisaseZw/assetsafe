import type { QueryClient } from '@tanstack/react-query';

export const registryQueryKeys = {
  assetDashboard: ['registry-dashboard'] as const,
  assetRecords: ['registry-records'] as const,
  collateralDashboard: ['collateral-dashboard'] as const,
  collateralRecords: ['collateral-records'] as const,
  hpDashboard: ['hp-dashboard'] as const,
  hpRecords: ['hp-records'] as const,
};

export function invalidateRegistryQueries(
  queryClient: QueryClient,
  scope: 'asset' | 'collateral' | 'hp',
  id?: number,
) {
  const keys =
    scope === 'asset'
      ? [registryQueryKeys.assetDashboard, registryQueryKeys.assetRecords]
      : scope === 'collateral'
        ? [
            registryQueryKeys.collateralDashboard,
            registryQueryKeys.collateralRecords,
          ]
        : [registryQueryKeys.hpDashboard, registryQueryKeys.hpRecords];

  for (const queryKey of keys) {
    void queryClient.invalidateQueries({ queryKey, refetchType: 'active' });
  }

  // If an ID is provided, also invalidate the detail query for that record
  if (id) {
    const detailKey =
      scope === 'collateral'
        ? 'collateral-detail'
        : scope === 'hp'
          ? 'hire-purchase-detail'
          : 'asset-detail';
    void queryClient.invalidateQueries({
      queryKey: [detailKey, id],
      refetchType: 'active',
    });
  }
}
