# app/dao/job_platform.py
from typing import List
from sqlalchemy.orm import Session
from ..models import JobPlatform
from .base import BaseDAO


class JobPlatformDAO(BaseDAO[JobPlatform]):
    """求职平台数据访问层"""

    def __init__(self, db: Session):
        super().__init__(JobPlatform, db)

    def get_active_platforms(self) -> List[JobPlatform]:
        """获取所有活跃平台"""
        return self.db.query(self.model) \
            .filter(self.model.is_active == True) \
            .order_by(self.model.platform_name) \
            .all()

    def get_by_login_type(self, login_type: str) -> List[JobPlatform]:
        """根据登录方式筛选平台"""
        return self.db.query(self.model) \
            .filter(self.model.login_type == login_type) \
            .all()

    def deactivate_platform(self, id: int) -> bool:
        """停用平台"""
        platform = self.get(id)
        if not platform:
            return False

        platform.is_active = False
        self.update(platform)
        return True
