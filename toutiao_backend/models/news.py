"""
新闻模块数据模型
"""
from datetime import datetime
from sqlalchemy import String, Integer, TIMESTAMP, func, Text, Index
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    """基类，包含创建时间和更新时间"""
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), comment='更新时间')

class News(Base):
    """新闻文章模型"""
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='新闻ID')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='新闻标题')
    description: Mapped[str] = mapped_column(String(500), nullable=True, comment='新闻简介')
    content: Mapped[str] = mapped_column(Text, nullable=False, comment='新闻内容')
    image: Mapped[str] = mapped_column(String(255), nullable=True, comment='封面图片URL')
    author: Mapped[str] = mapped_column(String(50), nullable=True, comment='作者')
    category_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='分类ID')
    views: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, default=0, comment='浏览量')
    publish_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='发布时间')

    __table_args__ = (
        Index('idx_news_category_id', 'category_id'),
        Index('idx_news_created_at', 'created_at'),
        Index('idx_news_category_created', 'category_id', 'created_at'),
        Index('idx_news_publish_time', 'publish_time'),
        Index('idx_news_views', 'views'),
    )

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', category_id={self.category_id})>"