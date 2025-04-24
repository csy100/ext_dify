from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    """数据库配置"""

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
