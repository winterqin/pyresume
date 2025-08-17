from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class JobApplication(Base):
    """求职记录表"""
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100), nullable=False, comment='公司名称')
    position_name = Column(String(100), comment='职位名称')
    application_status = Column(
        Enum('已投递', '测评中', '笔试中', '一面', '二面', '三面', '已结束', 'offer', name='application_status_enum'),
        nullable=False,
        default='已投递',
        comment='投递状态'
    )
    base_location = Column(String(50), comment='工作地点')
    resume_content = Column(Text, comment='简历内容')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    notes = Column(Text, comment='备注信息')
    # 外键关联到JobPlatform
    platform_id = Column(Integer, ForeignKey('job_platforms.id'), comment='求职平台ID')
    platform = relationship("JobPlatform", back_populates="applications")
