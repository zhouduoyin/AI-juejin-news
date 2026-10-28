"""
新闻分类缓存模块
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from config.redis_config import get_json_cache, set_json_cache
from crud.category import get_categories, get_category


CATEGORIES_ALL_KEY = "news:categories:all"
CATEGORIES_ONE_KEY = "news:categories:{}"

# 缓存过期时间（秒）：数据越稳定，缓存越持久
CATEGORIES_EXPIRE = 7200      # 分类
NEWS_LIST_EXPIRE = 600        # 新闻列表
NEWS_DETAIL_EXPIRE = 1800     # 新闻详情
VERIFY_CODE_EXPIRE = 120      # 验证码


async def get_cached_categories():
    """
    获取新闻分类缓存

    优先从 Redis 读取，未命中则查数据库并回写缓存
    """
    return await get_json_cache(CATEGORIES_ALL_KEY)


async def set_cached_categories(data: List[dict], expire: int = CATEGORIES_EXPIRE) -> bool:
    """
    写入新闻分类缓存

    Args:
        data: 分类数据列表
        expire: 过期时间（秒），默认 7200
    """
    return await set_json_cache(CATEGORIES_ALL_KEY, data, expire)
