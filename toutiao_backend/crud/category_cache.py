"""
新闻分类 旁路缓存策略
"""
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from models.category import NewsCategory

from crud.category import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category,
)
from cache.news_cache import (
    CATEGORIES_ALL_KEY,
    CATEGORIES_ONE_KEY,
    CATEGORIES_EXPIRE,
    get_cached_categories,
    set_cached_categories,
)
from config.redis_config import get_json_cache, set_json_cache, redis_client


def _category_to_dict(c: NewsCategory) -> dict:
    """ORM 对象转字典"""
    return {
        "id": c.id,
        "name": c.name,
        "sort_order": c.sort_order,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


async def _invalidate_category_cache(category_id: int = None):
    """删除分类缓存（单个 + 全部）"""
    if category_id:
        await redis_client.delete(CATEGORIES_ONE_KEY.format(category_id))
    await redis_client.delete(CATEGORIES_ALL_KEY)


async def get_cached_categories_list(db: AsyncSession) -> List[dict]:
    """
    获取分类列表（旁路缓存）

    先查 Redis → 未命中查 DB → 写缓存 → 返回
    """
    cached = await get_cached_categories()
    if cached is not None:
        return cached

    categories = await get_categories(db)
    data = [_category_to_dict(c) for c in categories]
    await set_cached_categories(data)
    return data


async def get_cached_category_one(db: AsyncSession, category_id: int) -> Optional[dict]:
    """
    获取单个分类（旁路缓存）

    先查 Redis → 未命中查 DB → 写缓存 → 返回
    """
    cached = await get_json_cache(CATEGORIES_ONE_KEY.format(category_id))
    if cached is not None:
        return cached

    category = await get_category(db, category_id)
    if category is None:
        return None

    data = _category_to_dict(category)
    await set_json_cache(CATEGORIES_ONE_KEY.format(category_id), data, CATEGORIES_EXPIRE)
    return data


async def create_cached_category(db: AsyncSession, name: str, sort_order: int = 0) -> NewsCategory:
    """创建分类 → 删除缓存"""
    category = await create_category(db, name, sort_order)
    await _invalidate_category_cache()
    return category


async def update_cached_category(db: AsyncSession, category_id: int, name: str = None, sort_order: int = None) -> Optional[NewsCategory]:
    """更新分类 → 删除缓存"""
    category = await update_category(db, category_id, name, sort_order)
    if category:
        await _invalidate_category_cache(category_id)
    return category


async def delete_cached_category(db: AsyncSession, category_id: int) -> bool:
    """删除分类 → 删除缓存"""
    result = await delete_category(db, category_id)
    if result:
        await _invalidate_category_cache(category_id)
    return True
