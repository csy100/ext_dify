from loguru import logger
from sqlalchemy import select, update, func
from extensions.ext_db import get_session
from models.poll import Poll
from models.option import Option
from models.vote import Vote


class PollService:
    # 存储所有 WebSocket 订阅者
    subscribers = set()

    @classmethod
    async def get_current_poll(cls):
        """获取当前问卷"""
        try:
            async with get_session() as session:
                # 获取最新的问卷
                poll = await session.scalar(
                    select(Poll).order_by(Poll.created_at.desc())
                )

                if not poll:
                    return {"code": 404, "message": "没有可用的问卷"}

                # 获取问卷的所有选项
                options = await session.scalars(
                    select(Option).filter(Option.poll_id == poll.id)
                )
                options_list = []

                # 获取每个选项的投票数
                for option in options:
                    vote_count = await session.scalar(
                        select(func.count())
                        .select_from(Vote)
                        .filter(Vote.option_id == option.id)
                    )
                    option_data = option.to_dict()
                    option_data["votes_count"] = vote_count
                    options_list.append(option_data)

                return {
                    "code": 200,
                    "message": "获取成功",
                    "data": {
                        "poll": poll.to_dict(),
                        "options": options_list,
                    },
                }
        except Exception as e:
            logger.error(f"获取问卷失败: {str(e)}")
            return {"code": 500, "message": f"获取问卷失败: {str(e)}"}

    @classmethod
    async def submit_vote(cls, option_id: int, client_id: str):
        """提交投票"""
        try:
            async with get_session() as session:
                # 检查是否已投票
                existing_vote = await session.scalar(
                    select(Vote).filter(Vote.client_id == client_id)
                )
                if existing_vote:
                    return {"code": 203, "message": "您已经投过票了", "data": None}

                # 检查选项是否存在
                option = await session.scalar(
                    select(Option).filter(Option.id == option_id)
                )
                if not option:
                    return {"code": 404, "message": "选项不存在", "data": None}

                # 创建新的投票记录
                new_vote = Vote(option_id=option_id, client_id=client_id)
                session.add(new_vote)

                # 更新选项票数
                await session.execute(
                    update(Option)
                    .where(Option.id == option_id)
                    .values(votes_count=Option.votes_count + 1)
                )

                # 获取更新后的数据
                poll_data = await cls.get_current_poll()
                if poll_data["code"] == 200:
                    # 通知所有订阅者
                    await cls.notify_subscribers(poll_data["data"])

                return {
                    "code": 200,
                    "message": "投票成功",
                    "data": poll_data.get("data"),
                }

        except Exception as e:
            logger.error(f"投票失败: {str(e)}")
            return {"code": 500, "message": f"投票失败: {str(e)}"}

    @classmethod
    def add_subscriber(cls, websocket):
        """添加 WebSocket 订阅者"""
        cls.subscribers.add(websocket)

    @classmethod
    def remove_subscriber(cls, websocket):
        """移除 WebSocket 订阅者"""
        cls.subscribers.discard(websocket)

    @classmethod
    async def notify_subscribers(cls, data):
        """通知所有订阅者"""
        dead_subscribers = set()

        for subscriber in cls.subscribers.copy():
            try:
                await subscriber.send_json(data)
            except Exception as e:
                logger.error(f"通知订阅者失败: {str(e)}")
                dead_subscribers.add(subscriber)

        # 清理断开的连接
        for subscriber in dead_subscribers:
            cls.remove_subscriber(subscriber)
