import React, { useState, useEffect } from 'react';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Building, Plus, Edit, Trash2, Eye, EyeOff,Search } from 'lucide-react';
import { Label } from '@/components/ui/label';
import Header from '@/components/Header';
import { api, buildApiUrl } from '@/config/api';
import { API_CONFIG } from '../config/constants';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import tokenService from '../services/tokenService';
import { useNavigate } from 'react-router-dom';

function ApplicationList() {
  const [applications, setApplications] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [filteredCompanies, setFilteredCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isCompanyDialogOpen, setIsCompanyDialogOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [companySearchTerm, setCompanySearchTerm] = useState('');
  const [formData, setFormData] = useState({
    id: null,
    position: '',
    base: '',
    salery: '',
    status: '已投递',
    resume: '',
    company: ''
  });
  const [companyFormData, setCompanyFormData] = useState({
    id: null,
    company_name: '',
    website_link: '',
    login_type: '',
    uname: '',
    upass: ''
  });

  const navigate = useNavigate();
  const ITEMS_PER_PAGE = 10;

  // 页面加载时检查用户登录状态并获取数据
  useEffect(() => {
    const initializePage = async () => {
      try {
        // 检查用户是否已登录
        const currentUser = tokenService.getCurrentUser();
        if (!currentUser) {
          console.log('用户未登录，重定向到登录页面');
          navigate('/login');
          return;
        }

        console.log('当前用户:', currentUser);
        
        // 获取初始数据
        await Promise.all([
          fetchApplications(),
          fetchCompanies()
        ]);
      } catch (error) {
        console.error('初始化页面失败:', error);
        if (error.response?.status === 401) {
          console.log('Token 已过期，重定向到登录页面');
          tokenService.clearTokens();
          navigate('/login');
        }
      }
    };

    initializePage();
  }, [navigate]);

  useEffect(() => {
    if (companySearchTerm) {
      const filtered = companies.filter(company => 
        company.company_name.toLowerCase().includes(companySearchTerm.toLowerCase())
      );
      setFilteredCompanies(filtered);
    } else {
      setFilteredCompanies(companies);
    }
  }, [companySearchTerm, companies]);

  // 当页码或搜索词变化时重新获取数据
  useEffect(() => {
    const handler = setTimeout(() => {
      if (tokenService.getCurrentUser()) {
        fetchApplications();
      }
    }, 500); // 500ms的防抖延迟

    return () => {
      clearTimeout(handler);
    };
  }, [currentPage, searchTerm]);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        page_size: ITEMS_PER_PAGE
      };
      
      if (searchTerm) {
        params.search = searchTerm;
      }

      console.log('获取求职记录，参数:', params);
      const response = await api.get(buildApiUrl(API_CONFIG.APPLICATION.LIST), params);
      console.log('求职记录 API 响应:', response.data);
      
      // 处理嵌套的响应结构
      const responseData = response.data;
      console.log(responseData)
      if (responseData.success) {
        console.log("responseData success")
        setApplications(responseData.data || []);
        setTotalPages(responseData.total_pages || 1);
      } else {
        setApplications([]);
        setTotalPages( 1);
      }
    } catch (error) {
      console.error('获取求职记录失败:', error);
      if (error.response?.status === 401) {
        tokenService.clearTokens();
        navigate('/login');
      } else {
        toast.error('获取求职记录失败');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchCompanies = async () => {
    try {
      console.log('获取公司选项列表');
      const response = await api.get(buildApiUrl(API_CONFIG.COMPANY.OPTIONS));
      console.log('公司选项 API 响应:', response.data);
      
      // 处理嵌套的响应结构
      const responseData = response.data;
      if (responseData.success) {
        setCompanies(responseData.data || []);
        setFilteredCompanies(responseData.data || []);
      } else {
        setCompanies(responseData.data || []);
        setFilteredCompanies(responseData.data || []);
      }
    } catch (error) {
      console.error('获取公司列表失败:', error);
      if (error.response?.status === 401) {
        tokenService.clearTokens();
        navigate('/login');
      } else {
        toast.error('获取公司列表失败');
      }
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(buildApiUrl(API_CONFIG.APPLICATION.CREATE), {
        position: formData.position,
        base: formData.base,
        salery: formData.salery,
        status: formData.status,
        resume: formData.resume,
        company: formData.company || null
      });
      
      toast.success('求职记录创建成功');
      setIsDialogOpen(false);
      resetForm();
      fetchApplications();
    } catch (error) {
      console.error('创建求职记录失败:', error);
      toast.error('创建求职记录失败');
    }
  };

  const handleUpdate = async () => {
    try {
      await api.put(buildApiUrl(API_CONFIG.APPLICATION.UPDATE(formData.id)), {
        position: formData.position,
        base: formData.base,
        salery: formData.salery,
        status: formData.status,
        resume: formData.resume,
        company: formData.company || null
      });
      
      toast.success('求职记录更新成功');
      setIsDialogOpen(false);
      resetForm();
      fetchApplications();
    } catch (error) {
      console.error('更新求职记录失败:', error);
      toast.error('更新求职记录失败');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(buildApiUrl(API_CONFIG.APPLICATION.DELETE(id)));
      toast.success('求职记录删除成功');
      fetchApplications();
    } catch (error) {
      console.error('删除求职记录失败:', error);
      toast.error('删除求职记录失败');
    }
  };

  const resetForm = () => {
    setFormData({
      id: null,
      position: '',
      base: '',
      salery: '',
      status: '已投递',
      resume: '',
      company: ''
    });
  };

  const resetCompanyForm = () => {
    setCompanyFormData({
      id: null,
      company_name: '',
      website_link: '',
      login_type: '',
      uname: '',
      upass: ''
    });
  };

  const openCreateDialog = () => {
    resetForm();
    setIsDialogOpen(true);
  };

  const openCreateCompanyDialog = () => {
    resetCompanyForm();
    setIsCompanyDialogOpen(true);
  };

  const openEditDialog = (record) => {
    setFormData({
      id: record.id,
      position: record.position,
      base: record.base,
      salery: record.salery,
      status: record.status,
      resume: record.resume,
      company: record.company?.id || ''
    });
    setIsDialogOpen(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.id) {
      handleUpdate();
    } else {
      handleCreate();
    }
  };

  const handleCompanySubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post(buildApiUrl(API_CONFIG.COMPANY.CREATE), {
        company_name: companyFormData.company_name,
        website_link: companyFormData.website_link,
        login_type: companyFormData.login_type,
        uname: companyFormData.uname,
        upass: companyFormData.upass
      });
      
      toast.success('公司信息创建成功');
      setIsCompanyDialogOpen(false);
      resetCompanyForm();
      fetchCompanies();
    } catch (error) {
      console.error('创建公司信息失败:', error);
      toast.error('创建公司信息失败');
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">加载中...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto  p-6">
              <Header />
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">求职记录管理</h1>
          <p className="text-gray-600 mt-2">管理您的求职申请记录</p>
        </div>

        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>求职记录列表</CardTitle>
              <div className="flex gap-4">
                <Input
                  placeholder="搜索公司、职位或地点..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="w-64"
                />
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button onClick={openCreateDialog}>
                      <Plus className="w-4 h-4 mr-2" />
                      新增记录
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-md">
                    <DialogHeader>
                      <DialogTitle>
                        {formData.id ? '编辑求职记录' : '新增求职记录'}
                      </DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="company">公司</Label>
                        <div className="flex gap-2">
                          <div className="relative flex-1">
                            <Input
                              placeholder="搜索公司..."
                              value={companySearchTerm}
                              onChange={(e) => setCompanySearchTerm(e.target.value)}
                              className="pr-10"
                            />
                            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                          </div>
                          <Button type="button" onClick={openCreateCompanyDialog} variant="outline">
                            <Plus className="w-4 h-4" />
                          </Button>
                        </div>
                        <Select
                          value={formData.company}
                          onValueChange={(value) => setFormData({...formData, company: value})}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="选择公司" />
                          </SelectTrigger>
                          <SelectContent>
                            {filteredCompanies.map((company) => (
                              <SelectItem key={company.id} value={company.id.toString()}>
                                {company.company_name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="position">职位</Label>
                        <Input
                          id="position"
                          value={formData.position}
                          onChange={(e) => setFormData({...formData, position: e.target.value})}
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="base">工作地点</Label>
                        <Input
                          id="base"
                          value={formData.base}
                          onChange={(e) => setFormData({...formData, base: e.target.value})}
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="salery">薪资</Label>
                        <Input
                          id="salery"
                          value={formData.salery}
                          onChange={(e) => setFormData({...formData, salery: e.target.value})}
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="status">状态</Label>
                        <Select
                          value={formData.status}
                          onValueChange={(value) => setFormData({...formData, status: value})}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="已投递">已投递 - 申请成功，简历已进入企业人才库</SelectItem>
                            <SelectItem value="简历筛选中">简历筛选中 - HR和业务部门正在筛选简历</SelectItem>
                            <SelectItem value="测评/笔试中">测评/笔试中 - 通过初筛后，需要完成线上测评或笔试题目</SelectItem>
                            <SelectItem value="面试中">面试中 - 正在安排或正在进行一轮或多轮面试</SelectItem>
                            <SelectItem value="已录用">已录用 - 通过所有考核，成功收到正式录用通知书</SelectItem>
                            <SelectItem value="已结束">已结束 - 最终状态</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="resume">简历</Label>
                        <Input
                          id="resume"
                          value={formData.resume}
                          onChange={(e) => setFormData({...formData, resume: e.target.value})}
                          required
                        />
                      </div>
                      
                      <div className="flex justify-end gap-2">
                        <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                          取消
                        </Button>
                        <Button type="submit">
                          {formData.id ? '更新' : '创建'}
                        </Button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>公司</TableHead>
                  <TableHead>职位</TableHead>
                  <TableHead>工作地点</TableHead>
                  <TableHead>薪资</TableHead>
                  <TableHead>状态</TableHead>
                  <TableHead>简历</TableHead>
                  <TableHead>创建时间</TableHead>
                  <TableHead>操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {applications.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>
                      {record.company?.company_name || '未指定'}
                    </TableCell>
                    <TableCell>{record.position}</TableCell>
                    <TableCell>{record.base}</TableCell>
                    <TableCell>{record.salery}</TableCell>
                    <TableCell>
                      <Badge className={`${
                        record.status === '已投递' ? 'bg-blue-500' :
                        record.status === '简历筛选中' ? 'bg-yellow-500' :
                        record.status === '测评/笔试中' ? 'bg-green-500' :
                        record.status === '面试中' ? 'bg-purple-500' :
                        record.status === '已录用' ? 'bg-red-500' :
                        record.status === '已结束' ? 'bg-gray-500' : 'bg-gray-400'
                      } text-white`}>
                        {record.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{record.resume}</TableCell>
                    <TableCell>
                      {new Date(record.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => openEditDialog(record)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(record.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            
            {/* 分页控件 */}
            <div className="flex justify-between items-center mt-6">
              <div className="text-sm text-gray-500">
                共 {totalPages * ITEMS_PER_PAGE} 条记录
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                >
                  上一页
                </Button>
                <span className="flex items-center px-3 text-sm">
                  第 {currentPage} 页，共 {totalPages} 页
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                >
                  下一页
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 新增公司信息对话框 */}
      <Dialog open={isCompanyDialogOpen} onOpenChange={setIsCompanyDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>新增公司信息</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleCompanySubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="company_name">公司名称</Label>
              <Input
                id="company_name"
                value={companyFormData.company_name}
                onChange={(e) => setCompanyFormData({...companyFormData, company_name: e.target.value})}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="website_link">网站链接</Label>
              <Input
                id="website_link"
                value={companyFormData.website_link}
                onChange={(e) => setCompanyFormData({...companyFormData, website_link: e.target.value})}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="login_type">登录方式</Label>
              <Select
                value={companyFormData.login_type}
                onValueChange={(value) => setCompanyFormData({...companyFormData, login_type: value})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="选择登录方式" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="邮箱">邮箱</SelectItem>
                  <SelectItem value="手机号">手机号</SelectItem>
                  <SelectItem value="用户名">用户名</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="uname">用户名</Label>
              <Input
                id="uname"
                value={companyFormData.uname}
                onChange={(e) => setCompanyFormData({...companyFormData, uname: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="upass">密码</Label>
              <Input
                id="upass"
                type="password"
                value={companyFormData.upass}
                onChange={(e) => setCompanyFormData({...companyFormData, upass: e.target.value})}
              />
            </div>
            
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setIsCompanyDialogOpen(false)}>
                取消
              </Button>
              <Button type="submit">
                创建
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ApplicationList;
