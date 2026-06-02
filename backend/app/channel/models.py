from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Model


class Channel(Model):
    __tablename__ = 'channels'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    server_id: Mapped[int] = mapped_column(ForeignKey('servers.id'))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
