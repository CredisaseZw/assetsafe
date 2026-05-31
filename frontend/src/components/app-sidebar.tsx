import { NavLink, useLocation } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  BarChart3,
  HandCoins,
  Landmark,
  Package,
  ScrollText,
  Shield,
  Users,
} from 'lucide-react';
import { useIsStaff } from '@/hooks/useIsStaff';
import { useIsSuperuser } from '@/hooks/useIsSuperuser';
import { SidebarUserMenu } from '@/components/layout/SidebarUserMenu';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar';

function SidebarNavLink({
  to,
  icon: Icon,
  label,
  end,
}: {
  to: string;
  icon: LucideIcon;
  label: string;
  end?: boolean;
}) {
  const location = useLocation();
  const isActive = end
    ? location.pathname === to
    : location.pathname === to || location.pathname.startsWith(`${to}/`);

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild isActive={isActive} tooltip={label}>
        <NavLink to={to}>
          <Icon />
          <span>{label}</span>
        </NavLink>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
}

export function AppSidebar() {
  const isStaff = useIsStaff();
  const isSuperuser = useIsSuperuser();
  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-1 py-1">
          <Shield className="size-5 shrink-0 text-[#0f7d8e]" />
          <span className="truncate text-lg font-bold group-data-[collapsible=icon]:hidden">
            AssetSafe
          </span>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Dashboard</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {isStaff ? (
                <SidebarNavLink
                  to="/registry"
                  icon={Package}
                  label="Asset Registry"
                />
              ) : null}
              <SidebarNavLink
                to="/collateral"
                icon={Landmark}
                label="Collateral"
              />
              <SidebarNavLink
                to="/hire-purchase"
                icon={HandCoins}
                label="Hire Purchase"
              />
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>System</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarNavLink to="/reports" icon={BarChart3} label="Report" />
              {isSuperuser ? (
                <>
                  <SidebarNavLink
                    to="/admin/users"
                    icon={Users}
                    label="User management"
                  />
                  <SidebarNavLink
                    to="/admin/audit-logs"
                    icon={ScrollText}
                    label="Audit logs"
                  />
                </>
              ) : null}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarUserMenu />
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
