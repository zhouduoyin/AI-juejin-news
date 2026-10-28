"""
Redis 配置模块
"""
import json
from typing import Any, Optional, Union

import redis.asyncio as aioredis

# Redis 连接配置
REDIS_URL = "redis://localhost:6379/0"

# 创建 Redis 连接对象
redis_client = aioredis.from_url(
    REDIS_URL,
    max_connections=10,
    decode_responses=True,
    protocol=2,  # 强制 RESP2，兼容 Windows 旧版 Redis
)

async def get_cache(key: str) -> Optional[str]:
    """
    从 Redis 中读取字符串缓存

    Args:
        key: 缓存键

    Returns:
        缓存字符串，不存在或异常返回 None
    """
    try:
        return await redis_client.get(key)
    except Exception as e:
        return None


async def get_json_cache(key: str) -> Optional[Union[dict, list]]:
    """
    从 Redis 中获取 JSON 缓存数据

    Args:
        key: 缓存键

    Returns:
        反序列化后的 dict 或 list，不存在或解析失败返回 None
    """
    try:
        data = await redis_client.get(key)
        if data is None:
            return None
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return None


async def set_json_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """
    将数据以 JSON 格式写入 Redis 缓存

    Args:
        key: 缓存键
        value: 缓存值（会被 JSON 序列化）
        expire: 过期时间（秒），默认 3600

    Returns:
        写入成功返回 True，异常返回 False
    """
    try:
        await redis_client.set(key, json.dumps(value, ensure_ascii=False), ex=expire)
        return True
    except Exception as e:
        return False


async def set_cache(key: str, value: str, expire: int = 3600) -> bool:
    """
    写入字符串缓存到 Redis

    Args:
        key: 缓存键
        value: 缓存值（字符串）
        expire: 过期时间（秒），默认 3600

    Returns:
        写入成功返回 True，异常返回 False
    """
    try:
        await redis_client.set(key, value, ex=expire)
        return True
    except Exception as e:
        return False


async def close_redis():
    """关闭 Redis 连接"""
    await redis_client.aclose()
