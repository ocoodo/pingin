from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.messages.models import Message


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, chat_id: int, sender_id: int, text: str) -> Message:
        new_message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text
        )
        self.session.add(new_message)
        await self.session.commit()
        return new_message

    async def get_by_chat_id(self, chat_id: int, limit: int, before: int = None) -> list[Message]:
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.id.desc())
        )
        if before:
            query = query.where(Message.id < before)
        query = query.limit(limit)
        
        result  = await self.session.execute(query)
        messages = list(result.scalars())
        messages.reverse()
        return messages
    
