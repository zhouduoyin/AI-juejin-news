"""
新闻模块路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.news import get_news_list, get_news_detail, get_related_news
from schemas.news import NewsItemResponse, NewsListData, NewsDetailData
from utils.response import success_response
from utils.exception import raise_not_found

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/list")
async def get_news_list_endpoint(
    categoryId: int = None,
    page: int = 1,
    pageSize: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """分页查询新闻列表"""
    news_list, total = await get_news_list(db, category_id=categoryId, page=page, page_size=pageSize)

    list_data = NewsListData(
        list=[NewsItemResponse.model_validate(n) for n in news_list],
        total=total,
        page=page,
        page_size=pageSize,
    )
    return success_response(message="查询成功", data=list_data)


@router.get("/detail")
async def get_news_detail_endpoint(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    """查询新闻详情"""
    news = await get_news_detail(db, news_id=id)

    if not news:
        raise_not_found("新闻不存在")

    # 浏览量 +1
    news.views += 1

    # 查询相关新闻（同分类）
    related = await get_related_news(db, news_id=id, category_id=news.category_id)

    detail_data = NewsDetailData(
        id=news.id,
        title=news.title,
        content=news.content,
        image=news.image,
        author=news.author,
        category_id=news.category_id,
        views=news.views,
        publish_time=news.publish_time,
        related_news=[NewsItemResponse.model_validate(r) for r in related],
    )
    return success_response(message="查询成功", data=detail_data)
