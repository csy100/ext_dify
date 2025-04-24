from flask_sock import Sock

# 创建 WebSocket 实例
sock = Sock()


def init_app(app):
    """初始化 WebSocket"""
    sock.init_app(app)
