from beanie import Document, PydanticObjectId
from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import Field

Category = Literal["sniadanie", "obiad", "kolacja"]


class Conversation(Document):
    user_id: PydanticObjectId
    category: Category
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "conversations"