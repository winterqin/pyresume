import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class DBConfig:
    # 从环境变量读取配置，如果不存在则使用默认值
    DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
    DB_PORT = os.getenv('MYSQL_PORT', '3306')
    DB_NAME = os.getenv('MYSQL_NAME', 'job_search_db')
    DB_USER = os.getenv('MYSQL_USER', 'job_user')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'job_password')

    @classmethod
    def get_db_url(cls, async_mode=False):
        if async_mode:
            return f"mysql+asyncmy://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"