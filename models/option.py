from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, Integer, Text

from extensions.ext_db import db
from .types import StringUUID


class Option(db.Model):
    """选项表"""

    __tablename__ = "options"

    id: Mapped[str] = mapped_column(
        StringUUID, primary_key=True, server_default=db.text("uuid_generate_v4()")
    )
    poll_id: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    votes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "poll_id": self.poll_id,
            "content": self.content,
            "votes_count": self.votes_count,
        }
