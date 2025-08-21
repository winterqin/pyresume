from ..models import JobPlatform
from ..dao import JobPlatformDAO
from fastapi_crud import BaseService


class JobPlatformService(BaseService[JobPlatform]):
    """求职平台业务逻辑层"""

    def __init__(self, dao: JobPlatformDAO):
        super().__init__(dao)
