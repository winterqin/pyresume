#!/bin/bash

# 等待数据库服务可用
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Database is ready!"

# 等待数据库完全初始化（额外等待）
sleep 5

# 运行数据库迁移
echo "Running database migrations..."
python manage.py migrate --noinput

if [ $? -ne 0 ]; then
    echo "Migration failed!"
    exit 1
fi

# 创建超级用户（如果需要）
echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 启动Gunicorn服务器
echo "Starting Gunicorn server..."
echo "Gunicorn will be available at http://0.0.0.0:8000"
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload \
    configs.wsgi:application