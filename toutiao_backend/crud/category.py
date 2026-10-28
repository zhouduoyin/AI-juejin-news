"""
新闻分类CRUD操作
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.category import NewsCategory


async def create_category(db: AsyncSession, name: str, sort_order: int = 0) -> NewsCategory:
    """创建分类"""
    category = NewsCategory(name=name, sort_order=sort_order)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: int) -> Optional[NewsCategory]:
    """获取单个分类"""
    result = await db.execute(select(NewsCategory).where(NewsCategory.id == category_id))
    return result.scalar_one_or_none()


async def get_categories(db: AsyncSession) -> List[NewsCategory]:
    """获取所有分类（按排序顺序）"""
    result = await db.execute(select(NewsCategory).order_by(NewsCategory.sort_order))
    return list(result.scalars().all())


async def update_category(db: AsyncSession, category_id: int, name: str = None, sort_order: int = None) -> Optional[NewsCategory]:
    """更新分类"""
    category = await get_category(db, category_id)
    if not category:
        return None
    if name is not None:
        category.name = name
    if sort_order is not None:
        category.sort_order = sort_order
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    """删除分类"""
    category = await get_category(db, category_id)
    if not category:
        return False
    await db.delete(category)
    await db.commit()
    return True
