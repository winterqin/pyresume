# pyresume 一键部署指南
docker-compose up --build -d
## 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd pyresume
```

### 2. 配置环境变量
复制并编辑环境配置文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，修改以下关键配置：

#### 必须修改的配置：
- `DJANGO_SECRET_KEY`: 生产环境请生成新的密钥
- `DB_PASSWORD`: 数据库密码
- `DB_ROOT_PASSWORD`: 数据库root密码
- `DJANGO_ALLOWED_HOSTS`: 添加你的域名

#### 可选配置：
- `FRONTEND_PORT`: 前端访问端口（默认3000）
- `BACKEND_PORT`: 后端API端口（默认8000）
- `EMAIL_*`: 邮件服务配置

### 3. 一键启动
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

### 4. 访问应用
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- 数据库: localhost:3306

## 管理命令

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 重启服务
```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 停止服务
```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎使用）
docker-compose down -v
```

### 更新应用
```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up --build -d
```

## 数据库管理

### 执行Django命令
```bash
# 数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户
docker-compose exec backend python manage.py createsuperuser

# 收集静态文件
docker-compose exec backend python manage.py collectstatic
```

### 数据库备份
```bash
# 备份数据库
docker-compose exec db mysqldump -u pyresume -p pyresume_db > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -u pyresume -p pyresume_db < backup.sql
```

## 生产环境注意事项

1. **安全配置**：
   - 修改默认密码
   - 设置 `DJANGO_DEBUG=False`
   - 使用强密码和新的SECRET_KEY

2. **域名配置**：
   - 在 `DJANGO_ALLOWED_HOSTS` 中添加你的域名
   - 配置反向代理（Nginx）

3. **SSL证书**：
   - 配置HTTPS
   - 使用Let's Encrypt等免费证书

4. **监控**：
   - 设置日志监控
   - 配置健康检查

## 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查数据库是否启动
   docker-compose logs db
   
   # 检查网络连接
   docker-compose exec backend ping db
   ```

2. **前端无法访问后端API**
   - 检查CORS配置
   - 确认后端服务正常运行

3. **端口冲突**
   - 修改 `.env` 文件中的端口配置
   - 确保端口未被其他服务占用

### 获取帮助
如有问题，请查看项目文档或提交Issue。