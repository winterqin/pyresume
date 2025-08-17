# app/schemas/job_application.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ApplicationStatus(str, Enum):
    """求职状态枚举"""
    submitted = "已投递"
    assessment = "测评中"
    written_test = "笔试中"
    first_interview = "一面"
    second_interview = "二面"
    third_interview = "三面"
    interviewing = "面试中"
    offer = "offer"
    rejected = "已结束"


class JobApplicationBase(BaseModel):
    """求职记录基础字段"""
    company_name: str = Field(..., max_length=100, example="字节跳动", description="公司名称")
    position_name: str = Field(..., max_length=100, example="Python开发工程师", description="职位名称")
    base_location: Optional[str] = Field(None, max_length=50, example="北京", description="工作地点")
    resume_content: Optional[str] = Field(None, example="我的简历内容...", description="简历内容")


class JobApplicationCreate(JobApplicationBase):
    """创建求职记录所需字段"""
    application_status: ApplicationStatus = Field(default=ApplicationStatus.submitted, description="投递状态")
    platform_id: Optional[int] = Field(None, example=1, description="关联平台ID")
    notes: Optional[str] = Field(None, example="HR邮箱：hr@example.com", description="备注信息")


class JobApplicationUpdate(BaseModel):
    """更新求职记录可选字段"""
    company_name: Optional[str] = Field(None, max_length=100)
    position_name: Optional[str] = Field(None, max_length=100)
    application_status: Optional[ApplicationStatus] = Field(None)
    base_location: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None)
    platform_id: Optional[int] = Field(None)


class JobApplicationOut(JobApplicationBase):
    """求职记录响应模型"""
    id: int = Field(..., example=1, description="记录ID")
    application_status: ApplicationStatus = Field(..., description="当前状态")
    platform_id: Optional[int] = Field(None, description="平台ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    notes: Optional[str] = Field(None)

    # 新配置
    class Config:
        from_attributes = True


class ApplicationStatusStats(BaseModel):
    """状态统计模型"""
    total: int = Field(..., example=100, description="总记录数")
    by_status: dict[ApplicationStatus, int] = Field(
        ...,
        example={"已投递": 30, "一面": 20},
        description="各状态计数"
    )
    last_updated: datetime = Field(..., description="最后更新时间")
