from ..schemas import JobApplicationCreate, JobApplicationUpdate
from ..dependencies import get_job_application_service
from fastapi_crud import BaseRouter


class ApplicationRouter(BaseRouter[JobApplicationCreate, JobApplicationUpdate]):
    def __init__(self):
        super().__init__(
            get_service=get_job_application_service,
            create_schema=JobApplicationCreate,
            update_schema=JobApplicationUpdate,
            prefix="/applications",
            tags=["Applications"],
        )


def get_application_router():
    return ApplicationRouter().router
