from beanie import Document, PydanticObjectId
from datetime import datetime, timezone
from typing import Optional


class Conversation(Document):
    user_id: PydanticObjectId
    category: str
    title: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "conversations"