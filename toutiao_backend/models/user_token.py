"""
用户令牌数据模型
"""
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, Index
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """基类，包含创建时间和更新时间"""
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')


class UserToken(Base):
    """用户令牌模型"""
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='令牌ID')
    user_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='用户ID')
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment='令牌值')
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, comment='过期时间')

    # 该表没有 updated_at 字段，置空覆盖 Base 的定义
    updated_at = None  # type: ignore

    __table_args__ = (
        Index('fk_user_token_user_idx', 'user_id'),
    )

    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id})>"
