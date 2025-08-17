# app/routers/job_platforms.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from ..schemas import (
    JobPlatformCreate,
    JobPlatformUpdate,
    JobPlatformOut,
    PlatformUsageStats
)
from ..dao import dao_platform
from ..services import JobPlatformService
from ..dependencies import get_job_platform_service, get_job_platform_dao

router = APIRouter(
    prefix="/api/platforms",
    tags=["求职平台管理"],
    responses={404: {"description": "未找到资源"}}
)


@router.post(
    "/",
    response_model=JobPlatformOut,
    status_code=status.HTTP_201_CREATED,
    summary="注册新平台"
)
async def create_platform(
        platform: JobPlatformCreate,
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """注册新的求职平台"""
    return service.register_platform(platform)


@router.get(
    "/",
    response_model=List[JobPlatformOut],
    summary="获取平台列表"
)
async def list_platforms(
        dao: dao_platform = Depends(get_job_platform_dao)
):
    """获取所有求职平台（默认只返回活跃平台）"""
    return dao.get_active_platforms()


@router.get(
    "/{platform_id}",
    response_model=JobPlatformOut,
    summary="获取平台详情"
)
async def get_platform(
        platform_id: int,
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """通过ID获取平台详情"""
    platform = service.dao.get(platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="平台不存在"
        )
    return platform


@router.put(
    "/{platform_id}",
    response_model=JobPlatformOut,
    summary="更新平台信息"
)
async def update_platform(
        platform_id: int,
        update_data: JobPlatformUpdate,
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """全量更新平台信息"""
    updated = service.update_platform(platform_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="平台不存在"
        )
    return updated


@router.patch(
    "/{platform_id}/toggle-active",
    response_model=JobPlatformOut,
    summary="切换平台激活状态"
)
async def toggle_platform_status(
        platform_id: int,
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """激活/停用平台"""
    updated = service.toggle_platform_status(platform_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="平台不存在"
        )
    return updated


@router.get(
    "/stats/usage",
    response_model=List[PlatformUsageStats],
    summary="获取平台使用统计"
)
async def get_platform_usage_stats(
        min_applications: int = Query(1, ge=0),
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """获取各平台的使用情况统计"""
    return service.get_platforms_by_usage(min_applications)


@router.delete(
    "/{platform_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除平台"
)
async def delete_platform(
        platform_id: int,
        service: JobPlatformService = Depends(get_job_platform_service)
):
    """删除平台（关联的求职记录不会被删除）"""
    if not service.delete_platform(platform_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="平台不存在"
        )
