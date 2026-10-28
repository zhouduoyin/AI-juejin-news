"""
收藏模块 Pydantic Schema
"""
from typing import List
from pydantic import BaseModel, ConfigDict, Field
from schemas.news import NewsItemResponse


class FavoriteCheckResponse(BaseModel):
    """收藏检查响应"""
    model_config = ConfigDict(populate_by_name=True)

    isFavorite: bool = Field(..., alias="isFavorite", description="是否已收藏")


class FavoriteRequest(BaseModel):
    """收藏请求体"""
    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(..., alias="newsId", description="新闻ID")


class FavoriteListData(BaseModel):
    """收藏列表数据"""
    model_config = ConfigDict(populate_by_name=True)

    list: List[NewsItemResponse] = Field(default_factory=list, description="收藏新闻列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., alias="pageSize", description="每页条数")
