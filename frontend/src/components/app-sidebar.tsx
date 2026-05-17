import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from '@/components/ui/sidebar';
import DarkModeToggle from '@/components/ui/DarkModeToggle';

export function AppSidebar() {
  const location = useLocation();
  const [dashboardOpen, setDashboardOpen] = useState(() => {
    const dashboardPaths = ['/', '/registry', '/collateral', '/hire-purchase'];

    return dashboardPaths.some((path) => location.pathname.startsWith(path));
  });

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="px-2 py-2 text-lg font-bold">AssetSafe</div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton
                type="button"
                onClick={() => setDashboardOpen((open) => !open)}
                aria-expanded={dashboardOpen}
                className="justify-between"
              >
                <span>Dashboard</span>
                <ChevronDown
                  className={
                    dashboardOpen
                      ? 'h-4 w-4 rotate-180 transition-transform duration-200'
                      : 'h-4 w-4 transition-transform duration-200'
                  }
                />
              </SidebarMenuButton>

              {dashboardOpen ? (
                <SidebarMenuSub>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton asChild>
                      <NavLink to="/registry">Asset Registry</NavLink>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton asChild>
                      <NavLink to="/collateral">Collateral</NavLink>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                  <SidebarMenuSubItem>
                    <SidebarMenuSubButton asChild>
                      <NavLink to="/hire-purchase">Hire Purchase</NavLink>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                </SidebarMenuSub>
              ) : null}
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <NavLink to="/reports">Report</NavLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <div className="flex items-center justify-between gap-2 px-2 py-2">
          <div className="text-sm text-sidebar-foreground/80">v1.0</div>
          <div>
            <DarkModeToggle />
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
