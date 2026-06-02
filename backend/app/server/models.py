from datetime import datetime, timezone
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database import Model


class Server(Model):
    __tablename__ = 'servers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class ServerMemberRole(str, Enum):
    owner = 'owner'
    admin = 'admin'
    member = 'member'


class ServerMember(Model):
    __tablename__ = 'server_members'
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'), primary_key=True)
    server_id: Mapped[int] = mapped_column(ForeignKey('servers.id'), primary_key=True)
    role: Mapped[str] = mapped_column(default=ServerMemberRole.member)

