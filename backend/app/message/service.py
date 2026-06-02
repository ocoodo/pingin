from typing import List, Optional

from app.message.repository import MessageRepo
from app.message.schemas import MessageOut

class MessageService:
    def __init__(self, repo: MessageRepo):
        self.repo = repo
    
    async def send_message(
        self,
        sender_id: int,
        channel_id: int,
        text: str
    ):
        message = await self.repo.add(
            sender_id=sender_id,
            channel_id=channel_id,
            text=text
        )
        return MessageOut(
            id=message.id,
            sender_id=message.sender_id,
            channel_id=message.channel_id,
            text=message.text
        )
    
    async def get_history(
        self,
        channel_id: int,
        before: Optional[int]
    ) -> List[MessageOut]:
        messages = await self.repo.get_paginated(
            channel_id=channel_id, before=before
        )
        return [MessageOut(
            id=m.id,
            sender_id=m.sender_id,
            channel_id=m.channel_id,
            text=m.text
        ) for m in messages]