"""
新闻分类路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.category_cache import (
    create_cached_category,
    get_cached_categories_list,
    update_cached_category,
    delete_cached_category,
)
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from utils.response import success_response
from utils.exception import raise_not_found, raise_bad_request

router = APIRouter(prefix="/api/news/categories", tags=["category"])


@router.get("")
async def get_categories_endpoint(db: AsyncSession = Depends(get_db)):
    """获取所有分类（Redis 缓存）"""
    categories = await get_cached_categories_list(db)
    data = [CategoryResponse.model_validate(c) for c in categories]
    return success_response(message="查询成功", data=data)


@router.post("")
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """创建分类"""
    try:
        new_category = await create_cached_category(db, category.name, category.sort_order)
        return success_response(message="创建成功", data=CategoryResponse.model_validate(new_category))
    except Exception:
        raise_bad_request(f"分类名称已存在: {category.name}")


@router.put("/{category_id}")
async def update_category_endpoint(category_id: int, category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    """更新分类"""
    updated = await update_cached_category(db, category_id, category.name, category.sort_order)
    if not updated:
        raise_not_found("分类不存在")
    return success_response(message="更新成功", data=CategoryResponse.model_validate(updated))


@router.delete("/{category_id}")
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    """删除分类"""
    result = await delete_cached_category(db, category_id)
    if not result:
        raise_not_found("分类不存在")
    return success_response(message="删除成功")
