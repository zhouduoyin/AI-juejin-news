"""
收藏模块 CRUD 操作
"""
from sqlalchemy import select, exists, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News


async def check_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """检查用户是否已收藏某条新闻"""
    stmt = select(exists().where(Favorite.user_id == user_id, Favorite.news_id == news_id))
    result = await db.execute(stmt)
    return result.scalar()


async def add_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """添加收藏——已收藏返回 False，新增成功返回 True"""
    is_favorited = await check_favorite(db, user_id, news_id)
    if is_favorited:
        return False
    db.add(Favorite(user_id=user_id, news_id=news_id))
    await db.flush()
    return True


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """取消收藏——没有收藏返回 False，删除成功返回 True"""
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.flush()
    return result.rowcount > 0


async def clear_favorite(db: AsyncSession, user_id: int) -> int:
    """清空收藏列表——返回删除条数"""
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.flush()
    return result.rowcount


async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """分页查询收藏列表——返回 (News列表, 总数)"""
    skip = (page - 1) * page_size

    # 总数
    count_stmt = select(func.count()).select_from(Favorite).where(Favorite.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar()

    # 分页查询，JOIN news 表拿新闻详情
    query = (
        select(News)
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(page_size)
    )
    result = await db.execute(query)
    return list(result.scalars().all()), total
