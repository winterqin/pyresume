import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Index from './pages/Index';
import ApplicationList from './pages/ApplicationList';
import CompanyList from './pages/CompanyList';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import SelfInfo from './pages/SelfInfo';
import Navigation from './components/Navigation';

// 路由守卫：检查用户是否已登录
// const ProtectedRoute = () => <div>protected ok</div>;
const ProtectedRoute = () => {
  const isAuthenticated = !!localStorage.getItem('accessToken');

  if (!isAuthenticated) {
    // 如果未登录，重定向到登录页
    return <Navigate to="/login" replace />;
  }

  // 如果已登录，显示带导航栏的布局，并通过 <Outlet /> 渲染子路由
  return (
    <div className="flex-col">
      <Navigation />
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
};

// 路由守卫：用于公共页面，如登录/注册
const GuestRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');
  if (isAuthenticated) {
    // 如果用户已登录，直接重定向到主页
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* 公共路由 */}
        <Route
          path="/login"
          element={
            <GuestRoute>
              <LoginPage />
            </GuestRoute>
          }
        />
        <Route
          path="/register"
          element={
            <GuestRoute>
              <RegisterPage />
            </GuestRoute>
          }
        />

        {/* 受保护的路由组 */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Index />} />
          <Route path="/applications" element={<ApplicationList />} />
          <Route path="/companies" element={<CompanyList />} />
          <Route path="/selfinfo" element={<SelfInfo />} />
        </Route>

        {/* 兜底路由，匹配所有未定义的路径，重定向到主页 */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
