import { Link, useLocation } from 'react-router-dom';
import { navItems } from '../nav-items';
import { Button } from '@/components/ui/button';
import { Bell, Home, LogIn, UserPlus, User, LogOut } from 'lucide-react';
import { useState, useEffect } from 'react';
import tokenService from '../services/tokenService';
import authService from '../services/authService';

function Navigation() {
  const location = useLocation();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const token = tokenService.getAccessToken();
    setIsLoggedIn(!!token);
    
    // 如果已登录，从JWT中获取用户信息
    if (token) {
      const currentUser = tokenService.getCurrentUser();
      setUserInfo(currentUser);
    }
  }, [location.pathname]);

  const handleLogout = () => {
    authService.logout();
    setIsLoggedIn(false);
    setUserInfo(null);
    window.location.href = '/login';
  };

  const getCurrentPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return '首页';
      case '/login':
        return '登录';
      case '/register':
        return '注册';
      case '/applications':
        return '求职记录';
      case '/companies':
        return '公司管理';
      case '/selfinfo':
        return '个人信息'; 
      default:
        return '未知页面';
    }
  };

  const getCurrentPageIcon = () => {
    switch (location.pathname) {
      case '/':
        return <Home className="h-4 w-4" />;
      case '/login':
        return <LogIn className="h-4 w-4" />;
      case '/register':
        return <UserPlus className="h-4 w-4" />;
      default:
        return null;
    }
  };

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <Link to="/" className="flex items-center space-x-2 text-gray-900 hover:text-gray-700">
              <Home className="h-6 w-6" />
              <span className="font-semibold text-lg">ResumeGo</span>
            </Link>
            <div className="flex items-center space-x-2 text-gray-500">
              <span>/</span>
              <span className="flex items-center space-x-1">
                {getCurrentPageIcon()}
                <span>{getCurrentPageTitle()}</span>
              </span>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <User className="h-4 w-4" />
                  <span>{userInfo?.email || '用户'}</span>
                </div>
                <Button onClick={handleLogout} variant="ghost" size="sm">
                  <LogOut className="h-4 w-4 mr-2" />
                  登出
                </Button>
              </>
            ) : (
              <>
                {location.pathname !== '/login' && (
                  <Button asChild variant="ghost" size="sm">
                    <Link to="/login">登录</Link>
                  </Button>
                )}
                {location.pathname !== '/register' && (
                  <Button asChild size="sm">
                    <Link to="/register">注册</Link>
                  </Button>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;