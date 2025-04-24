from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from configs import vote_config
from doc_app import VoteApp

# 创建异步数据库实例
db = SQLAlchemy()

# 创建异步会话工厂
_async_session_factory = None


@asynccontextmanager
async def get_session():
    """获取异步数据库会话的上下文管理器"""
    if _async_session_factory is None:
        raise RuntimeError("Database not initialized")

    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def init_app(app: VoteApp):
    """初始化数据库"""
    global _async_session_factory

    # 配置数据库 URL
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{vote_config.DB_USERNAME}:{vote_config.DB_PASSWORD}"
        f"@{vote_config.DB_HOST}:{vote_config.DB_PORT}/{vote_config.DB_DATABASE}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化数据库
    db.init_app(app)

    # 创建异步引擎
    engine = create_async_engine(
        app.config["SQLALCHEMY_DATABASE_URI"].replace(
            "postgresql://", "postgresql+asyncpg://"
        ),
        echo=app.config["SQLALCHEMY_ECHO"],
    )

    # 创建异步会话工厂
    _async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 设置 Model 的 query 属性（仅用于兼容性，不建议在异步环境中使用）
    db.session = _async_session_factory()
