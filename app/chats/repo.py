from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.chats.models import Chat, ChatType, ChatMember


class ChatRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, chat_type: ChatType) -> Chat:
        new_chat = Chat(type=chat_type)
        self.session.add(new_chat)
        await self.session.commit()
        return new_chat
    
    async def add_member(self, chat_id: int, member_id: int) -> ChatMember:
        new_member = ChatMember(
            chat_id=chat_id,
            user_id=member_id
        )
        self.session.add(new_member)
        await self.session.commit()
        return new_member
    
    async def get_by_members(self, user_ids: list[int], chat_type: Optional[ChatType] = None) -> list[Chat]:
        unique_user_ids = list(set(user_ids))
        target_count = len(unique_user_ids)
        
        query = (
            select(Chat)
            .join(ChatMember.chat)
            .where(ChatMember.user_id.in_(unique_user_ids))
        )
        
        if chat_type:
            query = query.where(Chat.type == chat_type)
        
        query = (
            query
            .group_by(Chat.id)
            .having(func.count(func.distinct(ChatMember.user_id)) == target_count)
        )
        
        chats = await self.session.execute(query)
        return list(chats.scalars().unique())
    
    async def get_user_chats(self, user_id: int, limit: int, offset: int) -> list[Chat]:
        chats = await self.session.execute(
            select(Chat)
            .join(ChatMember.chat)
            .where(ChatMember.user_id == user_id)
            .order_by(Chat.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(chats.scalars().unique())