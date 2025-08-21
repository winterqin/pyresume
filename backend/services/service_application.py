from ..models import JobApplication
from ..dao import JobApplicationDAO
from fastapi_crud import BaseService


class JobApplicationService(BaseService[JobApplication]):
    """求职记录业务逻辑层"""

    def __init__(self, dao: JobApplicationDAO):
        super().__init__(dao)
