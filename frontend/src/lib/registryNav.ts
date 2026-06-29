import type { AuthUser } from '@/api/authApi';

export const ASSET_REGISTRY_PATH = '/registry';

export const REGISTRY_DASHBOARD_TABS = [
  { label: 'Asset', path: ASSET_REGISTRY_PATH, staffOnly: true },
  { label: 'Collateral Registry', path: '/collateral', staffOnly: false },
  { label: 'HP', path: '/hire-purchase', staffOnly: false },
] as const;

export function isStaffUser(user: AuthUser | null | undefined): boolean {
  return user?.is_staff === true;
}

/** Asset registry nav/routes only when session user has been loaded and is_staff. */
export function canAccessAssetRegistry(
  user: AuthUser | null | undefined,
  authReady: boolean,
): boolean {
  return authReady && isStaffUser(user);
}

export function getRegistryDashboardTabs(isStaff: boolean) {
  return REGISTRY_DASHBOARD_TABS.filter((tab) => isStaff || !tab.staffOnly);
}

/** Non-staff users cannot land on asset registry after login or deep links. */
export function resolveSafeRedirect(
  path: string | undefined,
  isStaff: boolean,
): string {
  const target = path && path.startsWith('/') ? path : '/collateral';
  if (!isStaff && target.startsWith(ASSET_REGISTRY_PATH)) {
    return '/collateral';
  }
  return target;
}
