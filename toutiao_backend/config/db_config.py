"""
数据库配置模块
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 数据库连接配置
DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 打印SQL语句，生产环境建议关闭
    pool_pre_ping=True,  # 连接池预检查
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
)

# 创建异步会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 获取数据库会话的依赖函数
async def get_db():
    """
    获取数据库会话

    Yields:
        AsyncSession: 异步数据库会话
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()