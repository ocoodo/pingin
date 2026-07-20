from app.chats.schemas import ChatOut
from app.chats.models import ChatType
from app.chats.repo import ChatRepo
from app.users.repo import UserRepo
from app.exceptions import NotFoundError

class ChatService:
    def __init__(self, user_repo: UserRepo, chat_repo: ChatRepo):
        self.user_repo = user_repo
        self.chat_repo = chat_repo
    
    async def get_direct_chat(self, current_user_id: int, target_user_id: int):
        if (
            not await self.user_repo.get_by_id(current_user_id)
            or not await self.user_repo.get_by_id(target_user_id)
        ):
            raise NotFoundError
        
        chat = await self.chat_repo.get_by_members(
            [current_user_id, target_user_id],
            ChatType.DIRECT
        )
        
        if chat:
            return ChatOut(id=chat[0].id, type=chat[0].type)
        
        chat = await self.chat_repo.add(ChatType.DIRECT)
        await self.chat_repo.add_member(chat.id, current_user_id)
        await self.chat_repo.add_member(chat.id, target_user_id)
        return ChatOut(id=chat.id, type=chat.type)
        