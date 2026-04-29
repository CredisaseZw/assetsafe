import { createBrowserRouter, Navigate } from 'react-router-dom'
import AssetSafeLayout from '@/layouts/AssetSafeLayout'
import CollateralPage from '@/pages/CollateralPage'
import HirePurchasePage from '@/pages/HirePurchasePage'
import AssetRegistryPage from '@/pages/AssetRegistryPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/assetsafe/collateral" replace />,
  },
  {
    path: '/assetsafe',
    element: <AssetSafeLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="collateral" replace />,
      },
      {
        path: 'collateral',
        element: <CollateralPage />,
      },
      {
        path: 'hire-purchase',
        element: <HirePurchasePage />,
      },
      {
        path: 'registry',
        element: <AssetRegistryPage />,
      },
    ],
  },
])
