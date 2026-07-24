from app.messages.schemas import MessageOut
from app.messages.repo import MessageRepo
from app.chats.repo import ChatRepo
from app.exceptions import NotFoundError, ForbiddenError


class MessageService:
    def __init__(self, chat_repo: ChatRepo, message_repo: MessageRepo):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def send(self, chat_id: int, user_id: int, text: str) -> MessageOut:
        is_member = await self.chat_repo.is_member(chat_id, user_id)
        if not is_member:
            raise ForbiddenError

        exists = await self.chat_repo.get_by_id(chat_id)
        if not exists:
            raise NotFoundError
        
        message = await self.message_repo.add(chat_id, user_id, text)
        return MessageOut(
            id=message.id,
            chat_id=message.chat_id,
            sender_id=message.sender_id,
            text=message.text
        )

    async def get_messages(self, chat_id: int, user_id: int, limit: int, before: int) -> list[MessageOut]:
        is_member = await self.chat_repo.is_member(chat_id, user_id)
        if not is_member:
            raise ForbiddenError

        messages = await self.message_repo.get_by_chat_id(chat_id, limit, before)
        
        return [
            MessageOut(
                id=m.id,
                chat_id=m.chat_id,
                sender_id=m.sender_id,
                text=m.text
            ) for m in messages
        ]
