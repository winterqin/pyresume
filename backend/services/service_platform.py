# app/services/job_platform.py
from datetime import datetime
from typing import List, Optional
from ..models import JobPlatform
from ..dao import JobPlatformDAO
from ..schemas import JobPlatformCreate
from .base import BaseService


class JobPlatformService(BaseService[JobPlatform]):
    """求职平台业务逻辑层"""

    def __init__(self, dao: JobPlatformDAO):
        super().__init__(dao)

    def register_platform(self, platform_data: JobPlatformCreate) -> JobPlatform:
        """注册新平台（自动设置激活状态）"""
        db_platform = JobPlatform(
            **platform_data.dict(),
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.dao.create(db_platform)

    def toggle_platform_status(self, platform_id: int) -> Optional[JobPlatform]:
        """切换平台激活状态"""
        platform = self.dao.get(platform_id)
        if not platform:
            return None

        platform.is_active = not platform.is_active
        return self.dao.update(platform)

    def get_platforms_by_usage(
            self,
            min_applications: int = 1
    ) -> List[dict]:
        """获取平台使用情况统计（带申请数量过滤）"""
        platforms = self.dao.get_all()
        result = []
        for platform in platforms:
            app_count = len(platform.applications)
            if app_count >= min_applications:
                result.append({
                    "platform": platform.platform_name,
                    "application_count": app_count,
                    "last_used": max(app.created_at for app in platform.applications) if platform.applications else None
                })
        return sorted(result, key=lambda x: x["application_count"], reverse=True)

    def update_platform(self, platform_id, update_data):
        platform = self.dao.get(platform_id)
        if not platform:
            return None
        # 2. 更新字段（排除未提供的字段）
        update_dict = update_data.dict(exclude_unset=True)
        update_dict["updated_at"] = datetime.now()
        for k, v in update_dict.items():
            setattr(platform, k, v)
        return self.dao.update(platform)

    def delete_platform(self, platform_id):
        platform = self.dao.get(platform_id)
        if not platform:
            return None
        return self.dao.delete(platform_id)
