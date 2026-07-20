from enum import Enum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SQLEnum

from app.database import Model


class ChatType(str, Enum):
    DIRECT = 'direct'
    GROUP = 'group'
    CHANNEL = 'channel'


class Chat(Model):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[ChatType] = mapped_column(
        SQLEnum(ChatType, name='chat_type')
    )
    
    members: Mapped[list["ChatMember"]] = relationship(back_populates='chat')


class ChatMember(Model):
    __tablename__ = 'chat_members'
    
    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    
    chat: Mapped["Chat"] = relationship(back_populates='members')