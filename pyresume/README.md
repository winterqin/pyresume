# PyResume API 使用说明

## 概述
PyResume 是一个求职管理系统，包含公司管理和求职记录管理功能。

## 认证问题解决方案

### 问题描述
如果遇到以下错误：
```
"Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at ...>>": "Company.user" must be a "myUser" instance."
```

这是因为当前用户是匿名用户，但模型要求用户必须是 `myUser` 实例。

### 解决方案

#### 方案1：允许匿名用户（开发环境推荐）
当前代码已经配置为允许匿名用户创建数据，用户字段会被设置为 `None`。

#### 方案2：创建测试用户
```bash
# 进入Django shell
python manage.py shell

# 创建测试用户
from user.models import myUser
user = myUser.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
print(f"创建用户成功: {user.username}")
```

#### 方案3：使用Django管理界面
```bash
# 创建超级用户
python manage.py createsuperuser

# 启动管理界面
python manage.py runserver

# 访问 http://localhost:8000/admin/
```

## API 接口列表

### Company API
- `GET /api/companies/` - 获取公司列表（支持搜索和分页）
- `POST /api/companies/create/` - 创建新公司
- `PUT /api/companies/{id}/update/` - 更新公司信息
- `DELETE /api/companies/{id}/delete/` - 删除公司
- `GET /api/companies/options/` - 获取公司选项

### Application API
- `GET /api/applications/` - 获取求职记录列表（支持搜索和分页）
- `POST /api/applications/create/` - 创建新求职记录
- `PUT /api/applications/{id}/update/` - 更新求职记录
- `DELETE /api/applications/{id}/delete/` - 删除求职记录

## 测试API

### 使用测试脚本
```bash
# 确保Django后端运行在8000端口
python manage.py runserver

# 在另一个终端运行测试脚本
python pyresume/test_api.py
```

### 使用curl命令
```bash
# 创建公司
curl -X POST "http://localhost:8000/api/companies/create/" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"测试公司","website_link":"https://test.com"}'

# 获取公司列表
curl -X GET "http://localhost:8000/api/companies/"

# 创建求职记录
curl -X POST "http://localhost:8000/api/applications/create/" \
  -H "Content-Type: application/json" \
  -d '{"position":"软件工程师","base":"北京","status":"已投递"}'
```

### 使用Postman
1. 导入API测试文件
2. 设置基础URL为 `http://localhost:8000`
3. 测试各个接口

## 开发环境配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 数据库迁移
```bash
python manage.py makemigrations pyresume
python manage.py migrate
```

### 3. 启动服务
```bash
# 启动后端
python manage.py runserver

# 启动前端（另一个终端）
cd frontend
npm run dev
```

## 生产环境注意事项

1. **用户认证**：生产环境应该要求用户登录
2. **权限控制**：只有数据创建者或管理员可以编辑/删除数据
3. **CORS设置**：配置适当的跨域访问策略
4. **安全设置**：移除 `@csrf_exempt` 装饰器，添加适当的CSRF保护

## 故障排除

### 常见问题

1. **500错误**：检查Django日志，通常是模型字段类型不匹配
2. **404错误**：检查URL配置和路由
3. **认证错误**：检查用户模型和认证设置
4. **数据库错误**：检查数据库连接和迁移状态

### 调试技巧

1. 查看Django控制台输出
2. 检查浏览器开发者工具的网络请求
3. 使用Django shell测试模型操作
4. 查看Django日志文件

## 联系支持
如果遇到问题，请检查：
1. Django版本兼容性
2. 数据库配置
3. 用户模型设置
4. URL路由配置 