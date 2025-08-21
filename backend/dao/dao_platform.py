from sqlalchemy.orm import Session
from ..models import JobPlatform
from fastapi_crud import BaseDAO


class JobPlatformDAO(BaseDAO[JobPlatform]):
    """求职平台数据访问层"""

    def __init__(self, db: Session):
        super().__init__(JobPlatform, db)

