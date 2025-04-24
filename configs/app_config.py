from pydantic_settings import SettingsConfigDict

from configs.middleware.redis_config import RedisConfig
from configs.middleware.db_config import PostgresConfig


class DocConfig(
    PostgresConfig,
    RedisConfig,
):
    """应用配置类"""

    model_config = SettingsConfigDict(
        # 从.env文件读取配置
        env_file=".env",
        env_file_encoding="utf-8",
        # 忽略额外属性
        extra="ignore",
    )
