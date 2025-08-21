from sqlalchemy.orm import Session
from ..models import JobApplication
from fastapi_crud import BaseDAO


class JobApplicationDAO(BaseDAO[JobApplication]):
    """求职记录数据访问层"""

    def __init__(self, db: Session):
        super().__init__(JobApplication, db)

