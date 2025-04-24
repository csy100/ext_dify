from typing import Dict, Any

from models.poll import Poll
from models.option import Option
from extensions.ext_db import db


class OptionsService:
    """选项服务"""

    @staticmethod
    def create_options(received_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建问卷和选项

        Args:
            received_data: {
                "title": "问卷标题",
                "description": "问卷描述",
                "options": [
                    {"content": "选项1", "votes_count": 0},
                    {"content": "选项2", "votes_count": 0},
                    ...
                ]
            }
        """
        title = received_data.get("title")
        description = received_data.get("description")
        options_data = received_data.get("options", [])

        if not title or not options_data:
            return {
                "code": 400,
                "message": "标题和选项不能为空！",
            }

        if len(options_data) < 2:
            return {
                "code": 400,
                "message": "至少需要2个选项！",
            }

        try:
            # 创建问卷
            poll = Poll(title=title, description=description)
            db.session.add(poll)
            db.session.flush()  # 获取生成的ID

            # 创建所有选项
            options = []
            for opt_data in options_data:
                option = Option(
                    poll_id=poll.id, content=opt_data["content"], votes_count=0
                )
                db.session.add(option)
                options.append(option)

            db.session.commit()

            # 构建返回数据
            result = poll.to_dict()
            result["options"] = [opt.to_dict() for opt in options]

            return {"code": 200, "message": "创建成功！", "data": result}

        except Exception as e:
            db.session.rollback()
            return {
                "code": 500,
                "message": f"创建失败：{str(e)}",
            }
