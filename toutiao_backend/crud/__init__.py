"""
CRUD操作模块
"""
from crud.news import get_news_list
from crud.category import (
    create_category,
    get_category,
    get_categories,
    update_category,
    delete_category
)

__all__ = [
    "get_news_list",
    "create_category",
    "get_category",
    "get_categories",
    "update_category",
    "delete_category"
]