from ..schemas import (
    JobPlatformCreate,
    JobPlatformUpdate,
)
from ..dependencies import get_job_platform_service
from fastapi_crud import BaseRouter


class PlatformRouter(BaseRouter[JobPlatformCreate, JobPlatformUpdate]):
    def __init__(self):
        super().__init__(
            get_service=get_job_platform_service,
            create_schema=JobPlatformCreate,
            update_schema=JobPlatformUpdate,
            prefix="/platforms",
            tags=["Platforms"]
        )


def get_platform_router():
    return PlatformRouter().router
