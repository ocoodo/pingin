from pydantic import BaseModel

from app.chats.models import ChatType


class GetDirect(BaseModel):
    user_id: int


class ChatOut(BaseModel):
    id: int
    type: ChatType
