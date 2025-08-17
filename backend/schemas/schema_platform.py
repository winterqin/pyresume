# app/schemas/job_platform.py
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional


class JobPlatformBase(BaseModel):
    """平台基础字段"""
    platform_name: str = Field(..., max_length=100, example="BOSS直聘", description="平台名称")
    website_url: HttpUrl = Field(..., example="https://www.zhipin.com", description="网站URL")
    login_type: str = Field(..., max_length=50, example="账号密码", description="登录方式")


class JobPlatformCreate(JobPlatformBase):
    """创建平台所需字段"""
    username: Optional[str] = Field(None, max_length=100, example="user123", description="登录用户名")
    encrypted_password: Optional[str] = Field(None, max_length=100, example="encrypted_password", description="密码（前端加密前）")
    notes: Optional[str] = Field(None, example="平台使用注意事项", description="备注信息")


class JobPlatformUpdate(BaseModel):
    """更新平台可选字段"""
    platform_name: Optional[str] = Field(None, max_length=100, example="BOSS直聘新版")
    website_url: Optional[HttpUrl] = Field(None, example="https://new.zhipin.com")
    login_type: Optional[str] = Field(None, max_length=50, example="手机验证码")
    username: Optional[str] = Field(None, max_length=100)
    encrypted_password: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = Field(None, example=True)
    notes: Optional[str] = Field(None)


class JobPlatformOut(JobPlatformBase):
    """平台响应模型"""
    id: int = Field(..., example=1, description="平台ID")
    is_active: bool = Field(..., example=True, description="是否活跃")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    updated_at: datetime = Field(..., example="2023-01-01T00:00:00")

    # 新配置
    class Config:
        from_attributes = True


class PlatformUsageStats(BaseModel):
    """平台使用统计"""
    platform_id: int
    platform_name: str
    application_count: int
    last_used: Optional[datetime]