import React, { useState, useEffect } from 'react';
import { api } from '../config/api'; // 只导入 api
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

function SelfInfo() {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSelfInfo = async () => {
      try {
        setLoading(true);
        const response = await api.get(buildApiUrl(API_CONFIG.AUTH.SELF_INFO));
        if (response.success) {
          setUserInfo(response.data);
        } else {
          setError(response.error || '获取用户信息失败');
        }
      } catch (err) {
        setError(err.message || '您需要登录才能查看此页面。');
      } finally {
        setLoading(false);
      }
    };

    fetchSelfInfo();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <Header />
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">个人信息</h1>
          <p className="text-gray-600 mt-2">这里是您的账户信息。</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>用户信息</CardTitle>
          </CardHeader>
          <CardContent>
            {loading && <p>加载中...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {userInfo && (
              <div className="space-y-2">
                <p><strong>ID:</strong> {userInfo.id}</p>
                <p><strong>邮箱:</strong> {userInfo.email}</p>
                <p><strong>用户名:</strong> {userInfo.username}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SelfInfo;