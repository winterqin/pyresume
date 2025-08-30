import { HomeIcon, LogInIcon, UserPlusIcon } from "lucide-react";
import Index from "./pages/Index.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";

/**
* Central place for defining the navigation items. Used for navigation components and routing.
*/
export const navItems = [
  {
    title: "首页",
    to: "/",
    icon: <HomeIcon className="h-4 w-4" />,
    page: <Index />,
  },
  {
    title: "登录",
    to: "/login",
    icon: <LogInIcon className="h-4 w-4" />,
    page: <LoginPage />,
  },
  {
    title: "注册",
    to: "/register",
    icon: <UserPlusIcon className="h-4 w-4" />,
    page: <RegisterPage />,
  },
];
