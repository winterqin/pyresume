# app/dao/job_application.py
from datetime import datetime, timedelta
from typing import List, Optional, Type, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models import JobApplication
from .base import BaseDAO
from sqlalchemy import func

class JobApplicationDAO(BaseDAO[JobApplication]):
    """求职记录数据访问层"""

    def __init__(self, db: Session):
        super().__init__(JobApplication, db)

    def get_by_status(self, status: str) -> list[Type[JobApplication]]:
        """根据状态筛选记录"""
        return self.db.query(self.model) \
            .filter(self.model.application_status == status) \
            .all()

    def get_by_company(self, company_name: str) -> list[Type[JobApplication]]:
        """根据公司名称筛选记录（模糊匹配）"""
        return self.db.query(self.model) \
            .filter(self.model.company_name.ilike(f"%{company_name}%")) \
            .all()

    def get_recent_applications(self, days: int = 7) -> list[Type[JobApplication]]:
        """获取最近N天的投递记录"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.db.query(self.model) \
            .filter(self.model.created_at >= cutoff_date) \
            .order_by(self.model.created_at.desc()) \
            .all()

    def update_status(
            self,
            id: int,
            new_status: str,
            notes: Optional[str] = None
    ) -> Optional[JobApplication]:
        """更新投递状态并添加可选备注"""
        app = self.get(id)
        if not app:
            return None

        app.application_status = new_status
        if notes:
            app.notes = notes if not app.notes else f"{app.notes}\n{notes}"

        return self.update(app)

    def get_by_platform(self, platform_id: int) -> list[Type[JobApplication]]:
        """获取通过特定平台投递的记录"""
        return self.db.query(self.model) \
            .filter(self.model.platform_id == platform_id) \
            .all()

    def get_status_counts(self) -> Dict[str, int]:
        """
        获取所有状态的统计计数（单次查询完成）
        返回示例: {"已投递": 5, "面试中": 3, "已结束": 2}
        """
        results = self.db.query(
                self.model.application_status,
                func.count(self.model.id).label("count")
            ) \
            .group_by(self.model.application_status) \
            .all()

        return dict(results)
