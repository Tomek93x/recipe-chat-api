from beanie import Document, PydanticObjectId
from datetime import datetime, timezone


class Message(Document):
    conversation_id: PydanticObjectId
    role: str
    content: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "messages"