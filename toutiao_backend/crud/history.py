"""
历史模块 CRUD 操作
"""
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import News


async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    """添加浏览记录"""
    record = History(user_id=user_id, news_id=news_id)
    db.add(record)
    await db.flush()
    return record


async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """分页查询浏览历史——返回 (News列表, 总数)"""
    skip = (page - 1) * page_size

    count_stmt = select(func.count()).select_from(History).where(History.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar()

    query = (
        select(News)
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(skip)
        .limit(page_size)
    )
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def clear_history(db: AsyncSession, user_id: int) -> int:
    """清空浏览历史——返回删除条数"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.flush()
    return result.rowcount


async def remove_history(db: AsyncSession, news_id: int, user_id: int) -> bool:
    """删除单条浏览历史——按文章ID删除自己的记录"""
    result = await db.execute(
        select(History).where(History.news_id == news_id, History.user_id == user_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        return False
    await db.delete(record)
    await db.flush()
    return True
