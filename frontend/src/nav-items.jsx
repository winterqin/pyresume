import { Home, Briefcase, Building, User } from 'lucide-react';

export const navItems = [
  {
    label: '仪表盘',
    href: '/',
    icon: <Home className="h-5 w-5" />,
  },
  {
    label: '求职管理',
    href: '/applications',
    icon: <Briefcase className="h-5 w-5" />,
  },
  {
    label: '公司管理',
    href: '/companies',
    icon: <Building className="h-5 w-5" />,
  },
  {
    label: '个人信息',
    href: '/selfinfo',
    icon: <User className="h-5 w-5" />,
  },
];
