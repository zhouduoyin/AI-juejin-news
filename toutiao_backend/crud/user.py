"""
用户模块CRUD操作
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserRequest, UserUpdateRequest
from utils.security import get_hash_password, verify_password


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名查询用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest) -> User:
    """创建新用户"""
    user = User(
        username=user_data.username,
        password=get_hash_password(user_data.password),
    )
    db.add(user)
    await db.flush()
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """认证用户：查用户 → 不存在返回 None → 验密码 → 返回用户或 None"""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def update_user(db: AsyncSession, user: User, update_data: UserUpdateRequest) -> User:
    """更新用户资料——只更新实际传入的字段"""
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.flush()
    return user


async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str) -> bool:
    """修改密码——验旧密码，成功返回 True，旧密码错误返回 False"""
    if not verify_password(old_password, user.password):
        return False
    user.password = get_hash_password(new_password)
    await db.flush()
    return True
