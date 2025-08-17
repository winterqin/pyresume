from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class JobPlatform(Base):
    """求职平台信息表"""
    __tablename__ = 'job_platforms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_name = Column(String(100), nullable=False, comment='平台名称')
    website_url = Column(String(255), nullable=False, comment='网站URL')
    login_type = Column(String(255), nullable=False, comment="登录方式")
    username = Column(String(100), comment='登录用户名')
    encrypted_password = Column(String(255), comment='加密后的密码')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    notes = Column(Text, comment='备注信息')
    is_active = Column(Boolean, default=True, comment='是否活跃(1:是,0:否)')

    # 与JobApplication的一对多关系
    applications = relationship("JobApplication", back_populates="platform")
