from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime

from extensions.ext_db import db
from .types import StringUUID


class Vote(db.Model):
    """投票表"""

    __tablename__ = "votes"

    id: Mapped[str] = mapped_column(
        StringUUID, primary_key=True, server_default=db.text("uuid_generate_v4()")
    )
    option_id: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "option_id": self.option_id,
            "client_id": self.client_id,
            "created_at": self.created_at.isoformat(),
        }
