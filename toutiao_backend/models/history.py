"""
历史浏览数据模型
"""
from datetime import datetime
from sqlalchemy import TIMESTAMP, func, Index
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class History(Base):
    """浏览历史模型"""
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, comment='历史ID')
    user_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='用户ID')
    news_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False, comment='新闻ID')
    view_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='浏览时间')

    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', view_time.desc()),
    )

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
