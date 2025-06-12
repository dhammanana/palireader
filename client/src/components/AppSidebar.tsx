import { useState, useEffect, JSX } from 'react';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { ChevronDown, ChevronRight, Menu } from "lucide-react";
import PaliTextDialog from './PaliTextDialog'; // Import the new dialog component
import { ThemeModeToggle } from './ThemeModeToggle';

interface MenuItem {
  name: string;
  tag: string[];
  children?: MenuItem[];
}

export default function AppSidebar() {
  const [menuData, setMenuData] = useState<MenuItem[]>([]);
  const [openStates, setOpenStates] = useState<{ [key: string]: boolean }>({});
  const [selected, setSelected] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false); // State for dialog visibility
  const { state, isMobile, openMobile, setOpenMobile } = useSidebar();

  useEffect(() => {
    fetch('http://localhost:5000/api/menu')
      .then(response => response.json())
      .then(data => setMenuData(data))
      .catch(error => console.error('Error fetching menu:', error));
  }, []);

  const toggleSubCollapse = (tag: string) => {
    setOpenStates(prev => ({ ...prev, [tag]: !prev[tag] }));
  };

  const handleItemClick = (item: MenuItem) => {
    const tagKey = item.tag.join(',');

    // If item has children, toggle its open state
    if (item.children && item.children.length > 0) {
      toggleSubCollapse(tagKey);
    } else {
      // Open dialog for items without children
      setDialogOpen(true);
    }

    // Always set as selected
    setSelected(tagKey);

    // Close mobile menu when selecting an item without children
    if (isMobile && (!item.children || item.children.length === 0)) {
      setOpenMobile(false);
    }
  };

  const renderMenuItems = (items: MenuItem[], level: number = 0): JSX.Element[] => {
    return items.map((item) => {
      const tagKey = item.tag.join(',');
      const isOpen = openStates[tagKey] || false;
      const isSelected = selected === tagKey;
      const isCollapsed = state === 'collapsed';
      const hasChildren = item.children && item.children.length > 0;

      // For collapsed state, only show top-level items
      if (isCollapsed && level > 0) {
        return null;
      }

      return (
        <SidebarMenuItem key={tagKey}>
          <SidebarMenuButton
            className={`
              group relative flex items-center justify-between w-full text-left
              ${level === 0 ? 'font-semibold' : level === 1 ? 'font-medium' : 'font-normal'}
              ${level === 0 ? 'text-base' : 'text-sm'}
              ${isSelected ? 'bg-sidebar-accent text-sidebar-accent-foreground' : 'hover:bg-sidebar-accent/50'}
              ${isCollapsed ? 'justify-center px-2' : `pl-${2 + level * 4} pr-2`}
              py-2 rounded-md transition-all duration-200
            `}
            onClick={() => handleItemClick(item)}
            title={isCollapsed ? item.name : undefined}
          >
            <span className={`
              truncate
              ${isCollapsed ? 'sr-only' : 'block'}
            `}>
              {item.name}
            </span>

            {hasChildren && !isCollapsed && (
              <span className="ml-auto flex-shrink-0">
                {isOpen ? (
                  <ChevronDown className="h-4 w-4 transition-transform duration-200" />
                ) : (
                  <ChevronRight className="h-4 w-4 transition-transform duration-200" />
                )}
              </span>
            )}

            {/* Collapsed state indicator */}
            {isCollapsed && hasChildren && (
              <div className="absolute right-1 top-1 h-2 w-2 rounded-full bg-sidebar-accent opacity-50" />
            )}
          </SidebarMenuButton>

          {/* Recursive submenu rendering */}
          {hasChildren && isOpen && !isCollapsed && (
            <SidebarMenuSub className="ml-0 border-l-2 border-sidebar-border/50">
              {renderMenuItems(item.children as [MenuItem], level + 1)}
            </SidebarMenuSub>
          )}
        </SidebarMenuItem>
      );
    }).filter(Boolean) as JSX.Element[];
  };

  return (
    <>
      <Sidebar
        collapsible="icon"
        className="border-r bg-sidebar"
        variant="sidebar"
      >
        <SidebarContent >
          <SidebarGroup>
            <SidebarGroupLabel className="px-4 py-2 text-sidebar-foreground/70">
              <span className={state === 'collapsed' ? 'sr-only' : 'block'}>
                Tree View
              </span>
              {state === 'collapsed' && (
                <Menu className="h-4 w-4 mx-auto" />
              )}
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu className="space-y-1 px-2">
                {renderMenuItems(menuData)}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
      </Sidebar>
      <PaliTextDialog
        tagKey={selected}
        isOpen={dialogOpen}
        onClose={() => setDialogOpen(false)}
      />
    </>
  );
}