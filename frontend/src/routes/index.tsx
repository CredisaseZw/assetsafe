import { createBrowserRouter, Navigate } from 'react-router-dom'
import AssetSafeLayout from '@/layouts/AssetSafeLayout'
import { ProtectedRoute } from '@/components/shared/ProtectedRoute'
import LoginPage from '@/pages/LoginPage'
import CollateralPage from '@/pages/CollateralPage'
import HirePurchasePage from '@/pages/HirePurchasePage'
import AssetRegistryPage from '@/pages/AssetRegistryPage'

export const router = createBrowserRouter([
  // ── Public ──────────────────────────────────────────────────────────────────
  {
    path: '/login',
    element: <LoginPage />,
  },

  // ── Root redirect ────────────────────────────────────────────────────────────
  {
    path: '/',
    element: <Navigate to="/assetsafe/collateral" replace />,
  },

  // ── Protected ────────────────────────────────────────────────────────────────
  {
    path: '/assetsafe',
    element: (
      <ProtectedRoute>
        <AssetSafeLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Navigate to="collateral" replace /> },
      { path: 'collateral',     element: <CollateralPage /> },
      { path: 'hire-purchase',  element: <HirePurchasePage /> },
      { path: 'registry',       element: <AssetRegistryPage /> },
    ],
  },

  // ── Catch-all ────────────────────────────────────────────────────────────────
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
])
