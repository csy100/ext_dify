from configs import doc_config
from doc_app import DocApp
from extensions import ext_db, ext_redis, ext_blueprints, ext_websocket


def create_flask_app_with_configs() -> DocApp:
    app = DocApp(__name__)

    # 从环境变量加载配置
    app.config.from_mapping(doc_config.model_dump())

    return app


def create_app() -> DocApp:
    # 创建Flask应用
    app = create_flask_app_with_configs()

    # 初始化扩展
    initialize_extensions(app)

    return app


def initialize_extensions(app: DocApp):
    """初始化扩展"""
    extensions = [
        ext_db,
        ext_redis,
        ext_websocket,  # 添加 WebSocket 扩展
        ext_blueprints,
    ]

    for ext in extensions:
        ext.init_app(app)
