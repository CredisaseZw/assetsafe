import { createBrowserRouter, Navigate } from 'react-router-dom';
import AssetSafeLayout from '@/layouts/Dashboard';
import RouteError from '@/components/shared/RouteError';
import { ProtectedRoute } from '@/components/shared/ProtectedRoute';
import { StaffOnlyRoute } from '@/components/shared/StaffOnlyRoute';
import { SuperuserOnlyRoute } from '@/components/shared/SuperuserOnlyRoute';
import LoginPage from '@/pages/LoginPage';
import ForgotPasswordPage from '@/pages/ForgotPasswordPage';
import ForgotPasswordSentPage from '@/pages/ForgotPasswordSentPage';
import ResetPasswordPage from '@/pages/ResetPasswordPage';
import CollateralPage from '@/pages/CollateralPage';
import HirePurchasePage from '@/pages/HirePurchasePage';
import AssetRegistryPage from '@/pages/AssetRegistryPage';
import AccountSettingsPage from '@/pages/AccountSettingsPage';
import AuditLogsPage from '@/pages/AuditLogsPage';
import UsersManagementPage from '@/pages/UsersManagementPage';
import ReportsPage from '@/pages/ReportsPage';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/forgot-password',
    element: <ForgotPasswordPage />,
  },
  {
    path: '/forgot-password/sent',
    element: <ForgotPasswordSentPage />,
  },
  {
    path: '/reset-password',
    element: <ResetPasswordPage />,
  },

  {
    path: '/',
    element: <Navigate to="/collateral" replace />,
  },

  {
    path: '/',
    element: (
      <ProtectedRoute>
        <AssetSafeLayout />
      </ProtectedRoute>
    ),
    errorElement: <RouteError />,
    children: [
      { index: true, element: <Navigate to="collateral" replace /> },
      { path: 'collateral', element: <CollateralPage /> },
      { path: 'hire-purchase', element: <HirePurchasePage /> },
      {
        path: 'registry',
        element: (
          <StaffOnlyRoute>
            <AssetRegistryPage />
          </StaffOnlyRoute>
        ),
      },
      { path: 'settings', element: <AccountSettingsPage /> },
      { path: 'reports', element: <ReportsPage /> },
      {
        path: 'admin/audit-logs',
        element: (
          <SuperuserOnlyRoute>
            <AuditLogsPage />
          </SuperuserOnlyRoute>
        ),
      },
      {
        path: 'admin/users',
        element: (
          <SuperuserOnlyRoute>
            <UsersManagementPage />
          </SuperuserOnlyRoute>
        ),
      },
    ],
  },

  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
]);
