# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .dao import JobApplicationDAO, JobPlatformDAO
from .services import JobApplicationService, JobPlatformService


# -------------------------------
# DAO 依赖
# -------------------------------
def get_job_application_dao(db: Session = Depends(get_db)) -> JobApplicationDAO:
    return JobApplicationDAO(db)


def get_job_platform_dao(db: Session = Depends(get_db)) -> JobPlatformDAO:
    return JobPlatformDAO(db)


# -------------------------------
# Service 依赖
# -------------------------------
def get_job_application_service(
        dao: JobApplicationDAO = Depends(get_job_application_dao),
) -> JobApplicationService:
    return JobApplicationService(dao)


def get_job_platform_service(
        dao: JobPlatformDAO = Depends(get_job_platform_dao),
) -> JobPlatformService:
    return JobPlatformService(dao)
