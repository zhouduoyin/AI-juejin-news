"""
用户模块数据模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, TIMESTAMP, func, Index, Enum
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """基类，包含创建时间和更新时间"""
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')


class User(Base):
    """用户模型"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码（加密存储）')
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='昵称')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='头像URL')
    gender: Mapped[Optional[str]] = mapped_column(
        Enum('male', 'female', 'unknown', name='gender_enum'),
        nullable=True,
        default='unknown',
        comment='性别'
    )
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment='个人简介')
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True, comment='手机号')

    __table_args__ = (
        Index('idx_user_username', 'username'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
