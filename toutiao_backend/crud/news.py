"""
新闻模块CRUD操作
"""
from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News


async def get_news_list(db: AsyncSession, category_id: int = None, page: int = 1, page_size: int = 10) -> Tuple[List[News], int]:
    """分页查询新闻列表"""
    skip = (page - 1) * page_size

    # 查询总数
    count_query = select(func.count()).select_from(News)
    if category_id:
        count_query = count_query.where(News.category_id == category_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    query = select(News)
    if category_id:
        query = query.where(News.category_id == category_id)
    query = query.offset(skip).limit(page_size).order_by(News.created_at.desc())
    result = await db.execute(query)
    news_list = list(result.scalars().all())

    return news_list, total


async def get_news_detail(db: AsyncSession, news_id: int) -> Optional[News]:
    """查询新闻详情"""
    query = select(News).where(News.id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5) -> List[News]:
    """获取同分类的相关新闻"""
    query = (
        select(News)
        .where(News.category_id == category_id, News.id != news_id)
        .order_by(News.views.desc(), News.publish_time.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return list(result.scalars().all())