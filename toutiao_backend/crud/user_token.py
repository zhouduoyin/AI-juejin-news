"""
用户令牌CRUD操作
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.user_token import UserToken

TOKEN_EXPIRE_DAYS = 7


async def get_user_by_token(db: AsyncSession, token: str) -> Optional[User]:
    """根据 token 查询用户（非过期）"""
    result = await db.execute(
        select(User)
        .join(UserToken, User.id == UserToken.user_id)
        .where(UserToken.token == token, UserToken.expires_at > datetime.utcnow())
    )
    return result.scalar_one_or_none()


async def upsert_user_token(db: AsyncSession, user_id: int) -> str:
    """为用户创建或更新令牌，返回 token 值"""
    result = await db.execute(
        select(UserToken).where(UserToken.user_id == user_id)
    )
    token_record = result.scalar_one_or_none()
    expires_at = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)

    if token_record:
        token_record.token = uuid.uuid4().hex
        token_record.expires_at = expires_at
    else:
        token_record = UserToken(
            user_id=user_id,
            token=uuid.uuid4().hex,
            expires_at=expires_at,
        )
        db.add(token_record)

    await db.flush()
    return token_record.token
