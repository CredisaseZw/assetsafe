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
export function preloadRouteData(
  queryClient: QueryClient,
  config: RoutePreloadConfig,
) {
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
    queryKey: ['collateral-dashboard'],
    queryFn: async () => {
      // Import here to avoid circular deps
      const { collateralApi } = await import('@/api/collateralApi');
      return collateralApi.getDashboard();
    },
  },

  hirePurchase: {
    queryKey: ['hp-dashboard'],
    queryFn: async () => {
      const { hirePurchaseApi } = await import('@/api/hirePurchaseApi');
      return hirePurchaseApi.getDashboard();
    },
  },

  registry: {
    queryKey: ['registry-dashboard'],
    queryFn: async () => {
      const { assetRegistryApi } = await import('@/api/assetRegistryApi');
      return assetRegistryApi.getDashboard();
    },
  },
};
