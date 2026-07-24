from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database import Model


class Message(Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str]
