"""
新闻分类 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    """创建分类请求体"""
    name: str = Field(..., description="分类名称")
    sort_order: int = Field(default=0, alias="sortOrder", description="排序顺序")


class CategoryUpdate(BaseModel):
    """更新分类请求体"""
    name: Optional[str] = Field(default=None, description="分类名称")
    sort_order: Optional[int] = Field(default=None, alias="sortOrder", description="排序顺序")


class CategoryResponse(BaseModel):
    """分类响应"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(..., description="分类ID")
    name: str = Field(..., description="分类名称")
    sort_order: int = Field(..., alias="sortOrder", description="排序顺序")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt", description="创建时间")
