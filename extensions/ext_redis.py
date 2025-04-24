from loguru import logger
import redis

from configs import vote_config
from doc_app import VoteApp

redis_client = redis.Redis(
    host=vote_config.REDIS_HOST,
    port=vote_config.REDIS_PORT,
    username=vote_config.REDIS_USERNAME,
    password=vote_config.REDIS_PASSWORD,
    db=vote_config.REDIS_DB,
    ssl=vote_config.REDIS_USE_SSL,
    decode_responses=True,  # 自动将响应解码为字符串
)


def init_app(app: VoteApp):
    global redis_client

    # 测试连接
    try:
        redis_client.ping()
        logger.debug("Redis connection established")
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {str(e)}")

    app.extensions["redis"] = redis_client
