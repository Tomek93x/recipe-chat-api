from pydantic import BaseModel
from typing import Optional, Literal


class ChatMessageRequest(BaseModel):
    user_id: str
    category: str
    message: str
    conversation_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    conversation_id: str
    user_message: str
    ai_message: str


class MessageOut(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: str