"""
收藏模块路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.favorite import check_favorite, add_favorite, remove_favorite, clear_favorite, get_favorite_list
from schemas.favorite import FavoriteRequest, FavoriteCheckResponse, FavoriteListData
from schemas.news import NewsItemResponse
from utils.response import success_response
from utils.exception import raise_conflict, raise_not_found
from utils.auth import get_current_user

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite_status(
    newsId: int = Query(..., alias="newsId", description="新闻ID"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """检查当前用户是否已收藏某条新闻"""
    is_favorited = await check_favorite(db, user_id=current_user.id, news_id=newsId)
    return success_response(message="查询成功", data=FavoriteCheckResponse(isFavorite=is_favorited))


@router.get("/list")
async def get_favorite_list_endpoint(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, alias="pageSize", description="每页条数"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """分页查询收藏列表"""
    news_list, total = await get_favorite_list(db, user_id=current_user.id, page=page, page_size=pageSize)
    list_data = FavoriteListData(
        list=[NewsItemResponse.model_validate(n) for n in news_list],
        total=total,
        page=page,
        page_size=pageSize,
    )
    return success_response(message="查询成功", data=list_data)


@router.post("/add")
async def add_favorite_endpoint(
    req: FavoriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """添加收藏"""
    ok = await add_favorite(db, user_id=current_user.id, news_id=req.news_id)
    if not ok:
        raise_conflict("已收藏过了")
    return success_response(message="收藏成功")


@router.delete("/remove")
async def remove_favorite_endpoint(
    newsId: int = Query(..., alias="newsId", description="新闻ID"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """取消收藏"""
    ok = await remove_favorite(db, user_id=current_user.id, news_id=newsId)
    if not ok:
        raise_not_found("未收藏该新闻")
    return success_response(message="取消收藏成功")


@router.delete("/clear")
async def clear_favorite_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """清空收藏列表"""
    await clear_favorite(db, user_id=current_user.id)
    return success_response(message="清空收藏成功")
