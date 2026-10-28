"""
新闻模块 Pydantic Schema
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class NewsItemResponse(BaseModel):
    """新闻列表项响应"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    description: Optional[str] = Field(default=None, description="新闻简介")
    content: str = Field(..., description="新闻内容")
    image: Optional[str] = Field(default=None, description="封面图片URL")
    author: Optional[str] = Field(default=None, description="作者")
    category_id: int = Field(..., alias="categoryId", description="分类ID")
    views: int = Field(default=0, description="浏览量")
    publish_time: Optional[datetime] = Field(default=None, alias="publishTime", description="发布时间")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt", description="创建时间")


class NewsListData(BaseModel):
    """新闻列表数据"""
    model_config = ConfigDict(populate_by_name=True)

    list: List[NewsItemResponse] = Field(default_factory=list, description="新闻列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., alias="pageSize", description="每页条数")


class NewsDetailData(BaseModel):
    """新闻详情数据"""
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    content: str = Field(..., description="新闻内容")
    image: Optional[str] = Field(default=None, description="封面图片URL")
    author: Optional[str] = Field(default=None, description="作者")
    category_id: int = Field(..., alias="categoryId", description="分类ID")
    views: int = Field(default=0, description="浏览量")
    publish_time: Optional[datetime] = Field(default=None, alias="publishTime", description="发布时间")
    related_news: List[NewsItemResponse] = Field(default_factory=list, alias="relatedNews", description="相关新闻")
