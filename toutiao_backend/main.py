import asyncio
import sys

# Windows 上必须使用 SelectorEventLoop，否则 asyncio 会死锁
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.news import router as news_router
from routers.category import router as category_router
from routers.user import router as user_router
from routers.favorite import router as favorite_router
from routers.history import router as history_router
from utils.exception import register_exception_handlers
from config import close_redis

app = FastAPI()

# 注册全局异常处理器
register_exception_handlers(app)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)

# 注册路由
app.include_router(news_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(favorite_router)
app.include_router(history_router)


@app.on_event("shutdown")
async def shutdown():
    """应用关闭时清理资源"""
    await close_redis()


@app.get("/")
async def root():
    return {"message": "Hello World"}
