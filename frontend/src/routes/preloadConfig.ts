/**
 * Route prefetching strategy for TanStack Query integration
 * Preload queries when routes are hovered or navigated to
 */

import { QueryClient } from '@tanstack/react-query';

export interface RoutePreloadConfig {
  queryKey: string[];
  queryFn: () => Promise<any>;
  staleTime?: number;
}

/**
 * Preload route data before navigation
 * Call this on route hover or intent to navigate
 *
 * Usage:
 * onMouseEnter={() => preloadRouteData(queryClient, collateralRouteConfig)}
 */
export function preloadRouteData(queryClient: QueryClient, config: RoutePreloadConfig) {
  queryClient.prefetchQuery({
    queryKey: config.queryKey,
    queryFn: config.queryFn,
    staleTime: config.staleTime || 5 * 60 * 1000,
  });
}

/**
 * Route data preload configurations
 * Define what data to load for each route
 */
export const routePreloadConfigs = {
  collateral: {
    queryKey: ['collateral-stats'],
    queryFn: async () => {
      // Import here to avoid circular deps
      const { fetchCollateralStats } = await import('@/api/collateralApi');
      return fetchCollateralStats();
    },
  },

  hirePurchase: {
    queryKey: ['hp-dashboard'],
    queryFn: async () => {
      const { fetchHPDashboard } = await import('@/api/hirePurchaseApi');
      return fetchHPDashboard();
    },
  },

  registry: {
    queryKey: ['asset-registry-stats'],
    queryFn: async () => {
      const { fetchAssetRegistryStats } = await import('@/api/assetRegistryApi');
      return fetchAssetRegistryStats();
    },
  },
};
