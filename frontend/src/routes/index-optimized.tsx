import { lazy, Suspense } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import AssetSafeLayout from '@/layouts/Dashboard';
import { ProtectedRoute } from '@/components/shared/ProtectedRoute';
import LoginPage from '@/pages/LoginPage';

// Lazy load route components to reduce initial bundle size
// Each route only loads when accessed, improving time-to-interactive
const CollateralPage = lazy(() => import('@/pages/CollateralPage'));
const HirePurchasePage = lazy(() => import('@/pages/HirePurchasePage'));
const AssetRegistryPage = lazy(() => import('@/pages/AssetRegistryPage'));

// Fallback component while route chunk loads
function RouteLoadingFallback() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-lg text-gray-500">Loading...</div>
    </div>
  );
}

// Wrapper for lazy-loaded routes
function LazyRoute({
  component: Component,
}: {
  component: React.ComponentType;
}) {
  return (
    <Suspense fallback={<RouteLoadingFallback />}>
      <Component />
    </Suspense>
  );
}

export const router = createBrowserRouter([
  // ── Public ──────────────────────────────────────────────────────────────────
  {
    path: '/login',
    element: <LoginPage />,
  },

  // ── Root redirect ────────────────────────────────────────────────────────────
  {
    path: '/',
    element: <Navigate to="/collateral" replace />,
  },

  // ── Protected ────────────────────────────────────────────────────────────────
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <AssetSafeLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Navigate to="collateral" replace /> },
      {
        path: 'collateral',
        element: <LazyRoute component={CollateralPage} />,
      },
      {
        path: 'hire-purchase',
        element: <LazyRoute component={HirePurchasePage} />,
      },
      {
        path: 'registry',
        element: <LazyRoute component={AssetRegistryPage} />,
      },
    ],
  },

  // ── Catch-all ────────────────────────────────────────────────────────────────
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
]);
