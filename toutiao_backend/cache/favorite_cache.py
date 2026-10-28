"""
收藏缓存模块
"""
from typing import Optional, List

from config.redis_config import get_json_cache, set_json_cache, redis_client


FAVORITE_USER_LIST_KEY = "favorite:user:{}:list"
FAVORITE_USER_COUNT_KEY = "favorite:user:{}:count"
FAVORITE_EXPIRE = 1800


async def get_user_favorite_list_cache(user_id: int) -> Optional[List[dict]]:
    """读取用户收藏列表缓存"""
    return await get_json_cache(FAVORITE_USER_LIST_KEY.format(user_id))


async def set_user_favorite_list_cache(user_id: int, data: List[dict]) -> bool:
    """写入用户收藏列表缓存"""
    return await set_json_cache(FAVORITE_USER_LIST_KEY.format(user_id), data, FAVORITE_EXPIRE)


async def get_user_favorite_count_cache(user_id: int) -> Optional[int]:
    """读取用户收藏总数缓存"""
    key = FAVORITE_USER_COUNT_KEY.format(user_id)
    cached = await redis_client.get(key)
    if cached is None:
        return None
    try:
        return int(cached)
    except (ValueError, TypeError):
        return None


async def set_user_favorite_count_cache(user_id: int, count: int) -> bool:
    """写入用户收藏总数缓存"""
    try:
        await redis_client.set(FAVORITE_USER_COUNT_KEY.format(user_id), count, ex=FAVORITE_EXPIRE)
        return True
    except Exception:
        return False


async def invalidate_user_favorite_cache(user_id: int):
    """删除用户收藏相关缓存"""
    await redis_client.delete(
        FAVORITE_USER_LIST_KEY.format(user_id),
        FAVORITE_USER_COUNT_KEY.format(user_id),
    )
