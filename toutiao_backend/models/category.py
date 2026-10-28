"""
新闻分类模型
"""
from datetime import datetime
from sqlalchemy import String, Integer, TIMESTAMP, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """基类，包含创建时间和更新时间"""
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')


class NewsCategory(Base):
    """新闻分类模型"""
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='分类ID')
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='分类名称')
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='排序顺序')

    def __repr__(self):
        return f"<NewsCategory(id={self.id}, name='{self.name}')>"