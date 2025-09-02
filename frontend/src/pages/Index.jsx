import { Badge } from '@/components/ui/badge';
import { CardContent, CardHeader, Card, CardTitle } from '@/components/ui/card';
import { useNavigate } from 'react-router-dom';
import { Building, Calendar, MapPin, FileText, TrendingUp, Users, Target, Award, BookCheck, Search, XCircle } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { Bar, Legend, PieChart, Tooltip, BarChart, CartesianGrid, ResponsiveContainer, Pie, Cell, XAxis, YAxis } from 'recharts';
import { api, buildApiUrl } from '@/config/api';
import { API_CONFIG } from '../config/constants';
import Header from '@/components/Header';
import tokenService from '../services/tokenService';

function Index() {
  const [stats, setStats] = useState({
    status_counts: {},
    funnel_stats: {},
  });
  const [recentApplications, setRecentApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // 检查用户是否已登录
        const currentUser = tokenService.getCurrentUser();
        if (!currentUser) {
          navigate('/login');
          return;
        }
        
        // 获取仪表盘统计数据
        const result = await api.get(API_CONFIG.DASHBOARD.STATS);
        console.log('API响应:', result.data); // 调试日志
        
        // 修复数据结构解析
        const responseData = result.data;
        const actualData = responseData.success ? responseData.data : responseData;
        
        setStats({
          status_counts: actualData.status_counts || {},
          funnel_stats: actualData.funnel_stats || {},
        });
        setRecentApplications(actualData.recent_applications || []);
      } catch (error) {
        console.error('获取仪表盘数据失败:', error);
        if (error.response?.status === 401) {
          // Token过期，重定向到登录页
          tokenService.clearTokens();
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  const status_counts = stats.status_counts || {};
  const funnel_stats = stats.funnel_stats || {};

  // 求职状态统计数据
  const statusData = [
    { name: '已投递', value: status_counts['已投递'] || 0 },
    { name: '简历筛选中', value: status_counts['简历筛选中'] || 0 },
    { name: '测评/笔试中', value: status_counts['测评/笔试中'] || 0 },
    { name: '面试中', value: status_counts['面试中'] || 0 },
    { name: '已录用', value: status_counts['已录用'] || 0 },
    { name: '已结束', value: status_counts['已结束'] || 0 },
  ];

  // 各阶段统计柱状图数据
  const stageData = [
    { name: '总投递', value: funnel_stats.total_applications || 0 },
    { name: '过筛选', value: funnel_stats.passed_screening || 0 },
    { name: '过笔试', value: funnel_stats.passed_assessment || 0 },
    { name: '过面试', value: funnel_stats.passed_interview || 0 },
    { name: '已录用', value: funnel_stats.hired || 0 },
  ];

  const COLORS = ['#3B82F6', '#F59E0B', '#10B981', '#8B5CF6', '#EF4444', '#6B7280'];

  if (loading) {
    return <div className="flex justify-center items-center h-screen">加载中...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <Header />
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">求职进度管理仪表盘</h1>
          <p className="text-gray-600 mt-2">跟踪您的求职进度和状态</p>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-blue-100 p-3 rounded-full mr-4">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">总投递数</p>
                  <p className="text-2xl font-bold text-gray-900">{funnel_stats.total_applications || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-yellow-100 p-3 rounded-full mr-4">
                  <Search className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">筛选中</p>
                  <p className="text-2xl font-bold text-gray-900">{status_counts['简历筛选中'] || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-orange-100 p-3 rounded-full mr-4">
                  <BookCheck className="w-6 h-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">测评/笔试中</p>
                  <p className="text-2xl font-bold text-gray-900">{status_counts['测评/笔试中'] || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-purple-100 p-3 rounded-full mr-4">
                  <Users className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">面试中</p>
                  <p className="text-2xl font-bold text-gray-900">{status_counts['面试中'] || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-green-100 p-3 rounded-full mr-4">
                  <Award className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">已录用</p>
                  <p className="text-2xl font-bold text-gray-900">{status_counts['已录用'] || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="bg-gray-100 p-3 rounded-full mr-4">
                  <XCircle className="w-6 h-6 text-gray-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 font-medium">已结束</p>
                  <p className="text-2xl font-bold text-gray-900">{status_counts['已结束'] || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* 求职状态分布饼图 */}
          <Card>
            <CardHeader>
              <CardTitle>求职状态分布</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 求职漏斗统计柱状图 */}
          <Card>
            <CardHeader>
              <CardTitle>求职进度漏斗</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* 最近求职记录 */}
        <Card>
          <CardHeader>
            <CardTitle>最近求职记录</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentApplications.length > 0 ? (
                recentApplications.map((app) => (
                  <div key={app.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="bg-blue-100 p-2 rounded-full">
                        <Building className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900">{app.job_title}</h3>
                        <p className="text-sm text-gray-500">{app.company}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <Badge 
                        variant={app.status === '已录用' ? 'default' : 'secondary'}
                        className={app.status === '已录用' ? 'bg-green-100 text-green-800' : ''}
                      >
                        {app.status}
                      </Badge>
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar className="w-4 h-4 mr-1" />
                        {app.created_at}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>暂无求职记录</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Index;
