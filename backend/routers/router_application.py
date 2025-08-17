# app/routers/job_applications.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from typing import List, Optional
from ..schemas import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationOut,
    ApplicationStatusStats
)
from ..services import JobApplicationService
from ..dependencies import get_job_application_service

router = APIRouter(
    prefix="/api/applications",
    tags=["求职记录管理"],
    responses={404: {"description": "未找到资源"}}
)


@router.post(
    "/",
    response_model=JobApplicationOut,
    status_code=status.HTTP_201_CREATED,
    summary="创建新的求职记录"
)
async def create_application(
        application: JobApplicationCreate,
        service: JobApplicationService = Depends(get_job_application_service)
):
    """创建新的求职申请"""
    return service.create_application(application)


@router.get(
    "/{application_id}",
    response_model=JobApplicationOut,
    summary="获取单个求职记录详情"
)
async def get_application(
        application_id: int,
        service: JobApplicationService = Depends(get_job_application_service)
):
    """通过ID获取求职记录详情"""
    app = service.dao.get(application_id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到该求职记录"
        )
    return app


@router.get(
    "/",
    response_model=List[JobApplicationOut],
    summary="分页获取求职记录列表"
)
async def list_applications(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, le=1000),
        status: Optional[str] = Query(None),
        company: Optional[str] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        service: JobApplicationService = Depends(get_job_application_service)
):
    """获取分页的求职记录列表，支持多种过滤条件"""
    query_params = {
        "skip": skip,
        "limit": limit,
        "status": status,
        "company": company,
        "start_date": start_date,
        "end_date": end_date
    }
    return service.get_filtered_applications(**query_params)


@router.put(
    "/{application_id}",
    response_model=JobApplicationOut,
    summary="更新求职记录"
)
async def update_application(
        application_id: int,
        update_data: JobApplicationUpdate,
        service: JobApplicationService = Depends(get_job_application_service)
):
    """全量更新求职记录信息"""
    updated = service.update_application(application_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职记录不存在"
        )
    return updated


@router.patch(
    "/{application_id}/status",
    response_model=JobApplicationOut,
    summary="更新求职状态"
)
async def update_application_status(
        application_id: int,
        new_status: str = Query(..., min_length=2),
        notes: Optional[str] = Query(None),
        service: JobApplicationService = Depends(get_job_application_service)
):
    """更新求职状态并添加可选备注"""
    updated = service.update_application_status(application_id, new_status, notes)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职记录不存在或状态无效"
        )
    return updated


@router.get(
    "/stats/status",
    response_model=ApplicationStatusStats,
    summary="获取状态统计信息"
)
async def get_status_stats(
        service: JobApplicationService = Depends(get_job_application_service)
):
    """获取各状态的求职记录统计"""
    return service.get_status_distribution()


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除求职记录"
)
async def delete_application(
        application_id: int,
        service: JobApplicationService = Depends(get_job_application_service)
):
    """删除指定的求职记录"""
    if not service.delete_application(application_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="求职记录不存在"
        )
