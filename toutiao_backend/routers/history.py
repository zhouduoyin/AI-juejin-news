"""
历史模块路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.history import add_history, get_history_list, clear_history, remove_history
from schemas.history import HistoryRequest, HistoryListData
from schemas.news import NewsItemResponse
from utils.response import success_response
from utils.exception import raise_not_found
from utils.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history_endpoint(
    req: HistoryRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """添加浏览历史"""
    await add_history(db, user_id=current_user.id, news_id=req.news_id)
    return success_response(message="添加成功")


@router.get("/list")
async def get_history_list_endpoint(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, alias="pageSize", description="每页条数"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """分页查询浏览历史"""
    news_list, total = await get_history_list(db, user_id=current_user.id, page=page, page_size=pageSize)
    list_data = HistoryListData(
        list=[NewsItemResponse.model_validate(n) for n in news_list],
        total=total,
        page=page,
        page_size=pageSize,
    )
    return success_response(message="查询成功", data=list_data)


@router.delete("/clear")
async def clear_history_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """清空浏览历史"""
    await clear_history(db, user_id=current_user.id)
    return success_response(message="清空历史成功")


@router.delete("/delete/{newsId}")
async def remove_history_endpoint(
    newsId: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """删除单条浏览历史——按文章ID"""
    ok = await remove_history(db, news_id=newsId, user_id=current_user.id)
    if not ok:
        raise_not_found("该记录不存在")
    return success_response(message="删除成功")
