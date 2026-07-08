from pydantic import BaseModel, Field
from typing import Optional, Literal


Category = Literal["sniadanie", "obiad", "kolacja"]


class ChatMessageRequest(BaseModel):
    category: Category
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    conversation_id: str
    user_message: str
    ai_message: str


class MessageOut(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: str
