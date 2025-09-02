import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Building, Plus, Edit, Trash2, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';
import Header from '@/components/Header';
import { api } from '@/config/api';
import { API_CONFIG } from '../config/constants';

function CompanyList() {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [visiblePasswords, setVisiblePasswords] = useState({});
  const [formData, setFormData] = useState({
    id: null,
    company_name: '',
    website_link: '',
    login_type: '',
    uname: '',
    upass: ''
  });

  const ITEMS_PER_PAGE = 10;

  useEffect(() => {
    const handler = setTimeout(() => {
      fetchCompanies();
    }, 800); // 500ms的防抖延迟

    return () => {
      clearTimeout(handler);
    };
  }, [currentPage, searchTerm]);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        page_size: ITEMS_PER_PAGE
      };
      
      if (searchTerm) {
        params.search = searchTerm;
      }

      const result = await api.get(buildApiUrl(API_CONFIG.COMPANY.LIST), params);
      setCompanies(result.data || []);
      setTotalPages(result.total_pages || 1);
    } catch (error) {
      console.error('获取公司列表失败:', error);
      toast.error('获取公司列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(buildApiUrl(API_CONFIG.COMPANY.CREATE), {
        company_name: formData.company_name,
        website_link: formData.website_link,
        login_type: formData.login_type,
        uname: formData.uname,
        upass: formData.upass
      });
      
      toast.success('公司信息创建成功');
      setIsDialogOpen(false);
      resetForm();
      fetchCompanies();
    } catch (error) {
      console.error('创建公司信息失败:', error);
      toast.error('创建公司信息失败');
    }
  };

  const handleUpdate = async () => {
    try {
      await api.put(buildApiUrl(API_CONFIG.COMPANY.UPDATE(formData.id)), {
        company_name: formData.company_name,
        website_link: formData.website_link,
        login_type: formData.login_type,
        uname: formData.uname,
        upass: formData.upass
      });
      
      toast.success('公司信息更新成功');
      setIsDialogOpen(false);
      resetForm();
      fetchCompanies();
    } catch (error) {
      console.error('更新公司信息失败:', error);
      toast.error('更新公司信息失败');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(buildApiUrl(API_CONFIG.COMPANY.DELETE(id)));
      toast.success('公司信息删除成功');
      fetchCompanies();
    } catch (error) {
      console.error('删除公司信息失败:', error);
      toast.error('删除公司信息失败');
    }
  };

  const resetForm = () => {
    setFormData({
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

  const openEditDialog = (company) => {
    setFormData({
      id: company.id,
      company_name: company.company_name,
      website_link: company.website_link,
      login_type: company.login_type,
      uname: company.uname,
      upass: company.upass
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

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const togglePasswordVisibility = (id) => {
    setVisiblePasswords(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const formatUrl = (url) => {
    if (!url) return '#';
    if (!/^(https?:\/\/)/i.test(url)) {
      return `http://${url}`;
    }
    return url;
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">加载中...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">

      <div className="max-w-7xl mx-auto  p-6">
              <Header />
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">公司信息管理</h1>
          <p className="text-gray-600 mt-2">管理您的公司信息</p>
        </div>

        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>公司信息列表</CardTitle>
              <div className="flex gap-4">
                <Input
                  placeholder="搜索公司名称或网站..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="w-64"
                />
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button onClick={openCreateDialog}>
                      <Plus className="w-4 h-4 mr-2" />
                      新增公司
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-md">
                    <DialogHeader>
                      <DialogTitle>
                        {formData.id ? '编辑公司信息' : '新增公司信息'}
                      </DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="company_name">公司名称</Label>
                        <Input
                          id="company_name"
                          value={formData.company_name}
                          onChange={(e) => setFormData({...formData, company_name: e.target.value})}
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="website_link">网站链接</Label>
                        <Input
                          id="website_link"
                          value={formData.website_link}
                          onChange={(e) => setFormData({...formData, website_link: e.target.value})}
                          placeholder="例如: https://talent.baidu.com/jobs/center"
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="login_type">登录方式</Label>
                        <Input
                          id="login_type"
                          value={formData.login_type}
                          onChange={(e) => setFormData({...formData, login_type: e.target.value})}
                          placeholder="例如: 邮箱、手机号、用户名"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="uname">用户名</Label>
                        <Input
                          id="uname"
                          value={formData.uname}
                          onChange={(e) => setFormData({...formData, uname: e.target.value})}
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="upass">密码</Label>
                        <Input
                          id="upass"
                          type="password"
                          value={formData.upass}
                          onChange={(e) => setFormData({...formData, upass: e.target.value})}
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
                  <TableHead>公司名称</TableHead>
                  <TableHead>网站链接</TableHead>
                  <TableHead>登录方式</TableHead>
                  <TableHead>用户名</TableHead>
                  <TableHead>密码</TableHead>
                  <TableHead>创建时间</TableHead>
                  <TableHead>操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {companies.map((company) => (
                  <TableRow key={company.id}>
                    <TableCell>
                      <div className="flex items-center">
                        <Building className="w-5 h-5 mr-2 text-gray-500" />
                        {company.company_name}
                      </div>
                    </TableCell>
                    <TableCell>
                      <a 
                        href={formatUrl(company.website_link)} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                      >
                        {company.website_link}
                      </a>
                    </TableCell>
                    <TableCell>{company.login_type || '未设置'}</TableCell>
                    <TableCell>{company.uname || '未设置'}</TableCell>
                    <TableCell>
                      <div className="flex items-center justify-between w-24">
                        <span>{visiblePasswords[company.id] ? company.upass : '******'}</span>
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => togglePasswordVisibility(company.id)}>
                          {visiblePasswords[company.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </Button>
                      </div>
                    </TableCell>
                    <TableCell>
                      {new Date(company.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => openEditDialog(company)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(company.id)}
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
    </div>
  );
};

export default CompanyList;
