from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.message.models import Message

class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(
        self,
        channel_id: int,
        sender_id: int,
        text: str
    ) -> Message:
        message = Message(
            channel_id=channel_id,
            sender_id=sender_id,
            text=text
        )
        self.session.add(message)
        await self.session.commit()
        return message
    
    async def get_paginated(
        self,
        channel_id: int,
        before: Optional[int],
        limit: int = 50
    ) -> List[Message]:
        query = (
            select(Message)
            .where(Message.channel_id == channel_id)
            .order_by(Message.id)
            .limit(limit)
        )
        if before:
            query = query.where(Message.id < before)
            
        messages = await self.session.execute(query)
        return messages.scalars()
    