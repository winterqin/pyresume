# app/services/job_application.py
from datetime import datetime, timedelta
from typing import Optional, List
from ..models import JobApplication
from ..dao import JobApplicationDAO
from ..schemas import JobApplicationCreate, ApplicationStatusStats
from .base import BaseService


class JobApplicationService(BaseService[JobApplication]):
    """求职记录业务逻辑层"""
    # 状态分组规则（可配置化）
    _STATUS_GROUPS = {
        "面试中": ["一面", "二面", "三面"],  # 需要合并的状态
        # 可扩展其他分组规则
    }

    def __init__(self, dao: JobApplicationDAO):
        super().__init__(dao)

    def create_application(self, app_data: JobApplicationCreate) -> JobApplication:
        """创建求职记录（自动设置时间戳）"""
        db_app = JobApplication(
            **app_data.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.dao.create(db_app)

    def update_application_status(
            self,
            app_id: int,
            new_status: str,
            notes: Optional[str] = None
    ) -> Optional[JobApplication]:
        """更新求职状态（带状态校验和备注追加）"""
        valid_statuses = ['已投递', '测评中', '笔试中', '一面', '二面', '三面', '已结束', 'offer']
        if new_status not in valid_statuses:
            raise ValueError(f"无效状态: {new_status}。可选值: {valid_statuses}")

        app = self.dao.get(app_id)
        if not app:
            return None

        # 保留历史状态记录
        status_history = f"\n状态变更: {app.application_status} → {new_status} @ {datetime.now()}"
        app.notes = f"{app.notes or ''}{status_history}"

        return self.dao.update_status(app_id, new_status, notes)

    def get_recent_applications(
            self,
            days: int = 7,
            status: Optional[str] = None
    ) -> List[JobApplication]:
        """获取近期求职记录（可选状态过滤）"""
        apps = self.dao.get_recent_applications(days)
        if status:
            return [app for app in apps if app.application_status == status]
        return apps

    def get_company_stats(self, company_name: str) -> dict:
        """获取公司在各阶段的统计信息"""
        apps = self.dao.get_by_company(company_name)
        status_counts = {}
        for app in apps:
            status_counts[app.application_status] = status_counts.get(app.application_status, 0) + 1

        return {
            "company": company_name,
            "total": len(apps),
            "status_distribution": status_counts,
            "latest_update": max(app.updated_at for app in apps) if apps else None
        }

    def update_application(self, application_id, update_data):
        application = self.dao.get(application_id)
        if not application:
            return None

        application_dict = update_data.dict(exclude_unset=True)
        application_dict["updated_at"] = datetime.now()
        for k, v in application_dict.items():
            setattr(application, k, v)
        return self.dao.update(application)

    def delete_application(self, application_id):
        application = self.dao.get(application_id)
        if not application:
            return None

        return self.dao.delete(application_id)

    def get_filtered_applications(self, **param):

        return []

    def get_status_distribution(self):
        raw_counts = self.dao.get_status_counts()

        result = {
            group_name: 0
            for group_name in self._STATUS_GROUPS.keys()
        }
        # 3. 处理未分组的独立状态
        for status, count in raw_counts.items():
            matched_group = None

            # 检查是否属于某个分组
            for group_name, status_list in self._STATUS_GROUPS.items():
                if status in status_list:
                    matched_group = group_name
                    break

            if matched_group:
                # 4. 合并到分组
                result[matched_group] += count
            else:
                # 5. 保留独立状态
                result[status] = count

        # 3. 返回模型实例
        return ApplicationStatusStats(
            total=sum(raw_counts.values()),
            by_status=result,
            last_updated=datetime.now()
        )

