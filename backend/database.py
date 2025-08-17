from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DBConfig

Base = declarative_base()  # 现在这是推荐的导入方式


def init_db(async_mode=False):
    """初始化数据库连接和创建表"""
    db_url = DBConfig.get_db_url(async_mode=async_mode)

    if async_mode:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        engine = create_async_engine(db_url, echo=True)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        return AsyncSessionLocal
    else:
        engine = create_engine(db_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal


def get_db():
    """获取数据库会话的依赖函数"""
    SessionLocal = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    db = get_db()
