"""
收藏模块数据模型
"""
from datetime import datetime
from sqlalchemy import TIMESTAMP, func, Index, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    """收藏模型"""
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='收藏ID')
    user_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='用户ID')
    news_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='新闻ID')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='收藏时间')

    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id'),
    )

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
