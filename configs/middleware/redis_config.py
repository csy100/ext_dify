from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    """Redis配置"""

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_USE_SSL: bool = False
    REDIS_DB: int
