@echo off
echo 启动Django后端服务器...
cd /d "%~dp0"
uv run python manage.py runserver 8000
pause 