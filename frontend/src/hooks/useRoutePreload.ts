import { useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useLocation } from 'react-router-dom';
import { preloadRouteData, routePreloadConfigs } from '@/routes/preloadConfig';

/**
 * Hook to preload route data when the active route changes
 * Improves perceived performance on route transitions
 *
 * Call this in your layout component
 *
 * Usage:
 * export function AssetSafeLayout() {
 *   useRoutePreload();
 *   return (...)
 * }
 */
export function useRoutePreload() {
  const queryClient = useQueryClient();
  const location = useLocation();
  const lastPathnameRef = useRef(location.pathname);

  useEffect(() => {
    // Skip on initial mount
    if (lastPathnameRef.current === location.pathname) return;

    lastPathnameRef.current = location.pathname;

    // Determine which route we're on and preload its data
    if (location.pathname.includes('/collateral')) {
      preloadRouteData(queryClient, routePreloadConfigs.collateral);
    } else if (location.pathname.includes('/hire-purchase')) {
      preloadRouteData(queryClient, routePreloadConfigs.hirePurchase);
    } else if (location.pathname.includes('/registry')) {
      preloadRouteData(queryClient, routePreloadConfigs.registry);
    }
  }, [location.pathname, queryClient]);
}

/**
 * Prefetch all routes eagerly (optional - for aggressive preloading)
 * Good for desktop apps where bandwidth is not a concern
 *
 * Usage:
 * export function App() {
 *   usePrefetchAllRoutes();
 *   return (...)
 * }
 */
export function usePrefetchAllRoutes() {
  const queryClient = useQueryClient();

  useEffect(() => {
    // Prefetch all route data on app load
    // Stagger with setTimeout to avoid network saturation
    setTimeout(() => {
      preloadRouteData(queryClient, routePreloadConfigs.collateral);
    }, 500);

    setTimeout(() => {
      preloadRouteData(queryClient, routePreloadConfigs.hirePurchase);
    }, 1000);

    setTimeout(() => {
      preloadRouteData(queryClient, routePreloadConfigs.registry);
    }, 1500);
  }, [queryClient]);
}
