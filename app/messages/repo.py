from sqlalchemy.ext.asyncio import AsyncSession

from app.messages.models import Message


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, chat_id: int, text: str) -> Message:
        new_message = Message(
            chat_id=chat_id,
            text=text
        )
        self.session.add(new_message)
        await self.session.commit()
        return new_message

    
