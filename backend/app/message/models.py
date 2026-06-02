from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database import Model


class Message(Model):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey('channels.id'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    