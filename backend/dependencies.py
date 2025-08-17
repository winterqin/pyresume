# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .dao import JobApplicationDAO, JobPlatformDAO
from .services import JobApplicationService, JobPlatformService


def get_job_application_service(db: Session = Depends(get_db)) -> JobApplicationService:
    return JobApplicationService(JobApplicationDAO(db))


def get_job_platform_service(db: Session = Depends(get_db)) -> JobPlatformService:
    return JobPlatformService(JobPlatformDAO(db))


def get_job_application_dao(db: Session = Depends(get_db)) -> JobApplicationDAO:
    return JobApplicationDAO(db)


def get_job_platform_dao(db: Session = Depends(get_db)) -> JobPlatformDAO:
    return JobPlatformDAO(db)
