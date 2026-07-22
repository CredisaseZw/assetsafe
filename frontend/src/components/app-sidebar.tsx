import { NavLink, useLocation } from 'react-router-dom';
import type { LucideIcon } from 'lucide-react';
import {
  BarChart3,
  ChevronRight,
  FolderKanban,
  HandCoins,
  Landmark,
  LayoutDashboard,
  Package,
  ScrollText,
  Settings,
  Shield,
  Users,
} from 'lucide-react';
import { useIsStaff } from '@/hooks/useIsStaff';
import { useIsSuperuser } from '@/hooks/useIsSuperuser';
import { SidebarUserMenu } from '@/components/layout/SidebarUserMenu';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
} from '@/components/ui/sidebar';

const REGISTRY_PATHS = ['/collateral', '/hire-purchase', '/registry'] as const;
const SYSTEM_PATHS = ['/admin/users', '/admin/audit-logs'] as const;

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
        <NavLink to={to} end={end}>
          <Icon />
          <span>{label}</span>
        </NavLink>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
}

function NavSubLink({
  to,
  icon: Icon,
  label,
}: {
  to: string;
  icon: LucideIcon;
  label: string;
}) {
  const location = useLocation();
  const isActive =
    location.pathname === to || location.pathname.startsWith(`${to}/`);

  return (
    <SidebarMenuSubItem>
      <SidebarMenuSubButton asChild isActive={isActive}>
        <NavLink to={to}>
          <Icon />
          <span>{label}</span>
        </NavLink>
      </SidebarMenuSubButton>
    </SidebarMenuSubItem>
  );
}

function pathIsActive(pathname: string, paths: readonly string[]): boolean {
  return paths.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`),
  );
}

export function AppSidebar() {
  const isStaff = useIsStaff();
  const isSuperuser = useIsSuperuser();
  const location = useLocation();
  const registriesOpen = pathIsActive(location.pathname, REGISTRY_PATHS);
  const systemOpen = pathIsActive(location.pathname, SYSTEM_PATHS);

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
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarNavLink
                to="/dashboard"
                icon={LayoutDashboard}
                label="Dashboard"
                end
              />

              <Collapsible
                key={registriesOpen ? 'registries-open' : 'registries-closed'}
                defaultOpen={registriesOpen}
                className="group/collapsible"
              >
                <SidebarMenuItem>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton tooltip="Registries">
                      <FolderKanban />
                      <span>Registries</span>
                      <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      <NavSubLink
                        to="/collateral"
                        icon={Landmark}
                        label="Collateral Registry"
                      />
                      <NavSubLink
                        to="/hire-purchase"
                        icon={HandCoins}
                        label="Hire Purchase Registry"
                      />
                      {isStaff ? (
                        <NavSubLink
                          to="/registry"
                          icon={Package}
                          label="Asset Registry"
                        />
                      ) : null}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </SidebarMenuItem>
              </Collapsible>

              <SidebarNavLink to="/reports" icon={BarChart3} label="Reports" />

              {isSuperuser ? (
                <Collapsible
                  key={systemOpen ? 'system-open' : 'system-closed'}
                  defaultOpen={systemOpen}
                  className="group/collapsible"
                >
                  <SidebarMenuItem>
                    <CollapsibleTrigger asChild>
                      <SidebarMenuButton tooltip="System">
                        <Settings />
                        <span>System</span>
                        <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                      </SidebarMenuButton>
                    </CollapsibleTrigger>
                    <CollapsibleContent>
                      <SidebarMenuSub>
                        <NavSubLink
                          to="/admin/users"
                          icon={Users}
                          label="User management"
                        />
                        <NavSubLink
                          to="/admin/audit-logs"
                          icon={ScrollText}
                          label="Audit logs"
                        />
                      </SidebarMenuSub>
                    </CollapsibleContent>
                  </SidebarMenuItem>
                </Collapsible>
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
