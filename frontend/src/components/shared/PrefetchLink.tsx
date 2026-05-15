import { useQueryClient } from '@tanstack/react-query';
import { preloadRouteData, routePreloadConfigs } from './preloadConfig';

export interface PrefetchLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  to: keyof typeof routePreloadConfigs;
  children: React.ReactNode;
  className?: string;
}

/**
 * Link component that prefetches route data on hover
 * Reduces perceived loading time when navigating
 *
 * Usage:
 * <PrefetchLink to="collateral" href="/assetsafe/collateral">
 *   Collateral
 * </PrefetchLink>
 */
export function PrefetchLink({
  to,
  href,
  children,
  className,
  ...props
}: PrefetchLinkProps) {
  const queryClient = useQueryClient();
  const config = routePreloadConfigs[to];

  if (!config) {
    console.warn(`No preload config found for route: ${to}`);
    return (
      <a href={href} className={className} {...props}>
        {children}
      </a>
    );
  }

  const handleMouseEnter = () => {
    preloadRouteData(queryClient, config);
  };

  const handleFocus = () => {
    // Also preload on keyboard focus for accessibility
    preloadRouteData(queryClient, config);
  };

  return (
    <a
      href={href}
      className={className}
      onMouseEnter={handleMouseEnter}
      onFocus={handleFocus}
      {...props}
    >
      {children}
    </a>
  );
}
