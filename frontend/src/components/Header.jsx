import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Home, FileText, BuildingIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="mb-6 bg-white rounded-lg shadow p-4">
      <div className="flex space-x-4">
        <Button 
          onClick={() => navigate('/')}
          variant={location.pathname === '/' ? 'default' : 'secondary'}
          className="flex items-center"
        >
          <Home className="w-4 h-4 mr-2" />
          首页
        </Button>
        <Button 
          onClick={() => navigate('/applications')}
          variant={location.pathname === '/applications' ? 'default' : 'secondary'}
          className="flex items-center"
        >
          <FileText className="w-4 h-4 mr-2" />
          求职记录
        </Button>
        <Button 
          onClick={() => navigate('/companies')}
          variant={location.pathname === '/companies' ? 'default' : 'secondary'}
          className="flex items-center"
        >
          <BuildingIcon className="w-4 h-4 mr-2" />
          公司管理
        </Button>
      </div>
    </div>
  );
};

export default Header;
